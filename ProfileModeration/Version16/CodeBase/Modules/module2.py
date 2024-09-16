# Module for NSFW

import cv2
import torch
import numpy as np
from transformers import AutoModelForImageClassification, ViTImageProcessor

def detect_nsfw(image):
    try:
        print("(85) NSFW Try")
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
        processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')
        with torch.no_grad():
            inputs = processor(images=img, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits
        predicted_label = logits.argmax(-1).item()
        label = model.config.id2label[predicted_label]
        confidence = torch.softmax(logits, dim=-1)[0][predicted_label].item()

        print(f"\nNSFW: {label} Confidence: {confidence}\n")

        if label == 'nsfw':
            return 'Image contains NSFW content', confidence
        else:
            return None, confidence
    except Exception as e:
        print("(104) NSFW Except")
        return str(e), None