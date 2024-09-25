
import os
import time
import cv2
import numpy as np
# from transformers import AutoModelForImageClassification, ViTImageProcessor
from Constant.constant import NSFWModel, NSFWProcessor
import torch

class Detectnsfw :

    def __init__(self):
        pass
    
    def detect_nsfw(self,image):
        start_time = time.time()  # Start time measurement
        
        try:
            print("(114) NSFW Try")
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
            # processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')
            with torch.no_grad():
                inputs = NSFWProcessor(images=img, return_tensors="pt")
                outputs = NSFWModel(**inputs)
                logits = outputs.logits
            predicted_label = logits.argmax(-1).item()
            label = NSFWModel.config.id2label[predicted_label]
            confidence = torch.softmax(logits, dim=-1)[0][predicted_label].item()

            print(f"\nNSFW: {label} Confidence: {confidence}\n")

            if label == 'nsfw':
                return 'Image contains NSFW content', confidence
            else:
                return None, confidence
        except Exception as e:
            print("(133) NSFW Except")
            return str(e), None
        finally:
            end_time = time.time()  # End time measurement
            elapsed_time = end_time - start_time
            print(f"(detect_nsfw) Time taken: {elapsed_time:.4f} seconds")
