from ultralytics import YOLO
from PIL import Image
import torch

YOLO_FOLDER = "/home/abp/Documents/ABPProduction/ABP/ProfileModeration/Version12/best.pt"

# YOLO
yolo_model = YOLO(YOLO_FOLDER)
mapping = {0 : "sunglasses", 1 : "sunglasses", 2 : "eyeglasses", 3 : "headware", 4 : "headware", 5 : "headware"}


# YOLO Processing
def process_yolo(image):
    try:
        print("(288) YOLO Processing Try")
        image = Image.fromarray(image)
        results = yolo_model(image)
        
        if len(results[0].boxes) == 0:
            return "Accepted", None, None, None
        
        conf = torch.max(results[0].boxes.conf).item()
        
        if conf < 0.8:
            return "Accepted", None, conf, None
        
        z = torch.argmax(results[0].boxes.conf).item()
        a = int(results[0].boxes.cls[z].item())
        detected_class = mapping[a]
        print(f"YOLO Class: {detected_class} and Confidence: {conf}")
        
        if a == 2:                                          # Eyeglasses
            print("(306) YOLO Eyeglass Acceptance")
            return "Accepted", None, conf, detected_class
        return "Rejected", detected_class, conf, detected_class
    
    except Exception as e:
        print("(311) YOLO Exception")
        return "Rejected", f"{e}", None, None