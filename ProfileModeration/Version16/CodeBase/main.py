from Modules.module1 import check_image             # Part1: InsightFace and FaceRecognition
from Modules.module2 import detect_nsfw             # Part2: NSFW
from Modules.module3 import process_single_image    # Part3: Mediapipe
from Modules.module4 import process_image_clip      # Part4: CLIP
from Modules.module5 import process_yolo            # Part5: YOLO
from Modules.module4 import check_if_cartoon

import os
import shutil
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# Unique ID
import uuid
from datetime import datetime

BASE_FOLDER = "/home/abp/Documents/ABPProduction/ABP/ProfileModeration/Version16/CodeBase/Modules/Demo"

# Coversion to Image
def base64_to_image(base64_str):
    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image = np.array(image)
        print("(64) Base64 Try")
        return image, None
    except Exception as e:
        print("(67) Base64 Except")
        return None, str(e)
    
# Saving the Converted Image
def save_image(image, image_name=None):
    try:
        # Generate a unique filename if none is provided
        if image_name is None:
            unique_id = uuid.uuid4().hex
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_name = f"{timestamp}_{unique_id}.jpg"
            print(f"IMAGE NAME: {image_name}")
        
        image_path = os.path.join(BASE_FOLDER, image_name)
        Image.fromarray(image).save(image_path)
        print(f"(105) Image Saving Successful: {image_name}")
        return image_path, None
    except Exception as e:
        print("(108) Image Saving Failed")
        return None, str(e)

def get_result(base64_image):
    final_result = ""
    errstring = ""
    confidence_scores = {}
    detected_classes = {}
    status = 0                                    # Default status being 0 (Rejected)

    # Convert base64 to image and save it as image.jpg
    image, error = base64_to_image(base64_image)
    
    # Error in Base64
    if error:
        return {
            "status": status,
            "DetectedClass": {
                "ID_1": 1.0,                        # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }
    
    # image_path, error = save_image(image, 'image.jpg')
    image_path, error = save_image(image, None) 

    
    # Error in Saving
    if error:
        return {
            "status": status,
            "Detected Class": {
                "ID_1": 1.0,                        # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }
    
    # Processing NSFW
    NSFW_String, NSFW_Confidence = detect_nsfw(image)
    if NSFW_String == "Image contains NSFW content":
        return {
            "status": status,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": NSFW_Confidence,            # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }
    
    # No Face
    Face_Result, Error_Code = check_image(image_path)
    if Face_Result == "Rejected":    
        if Error_Code == 0:
            return {
            "status": status,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": 1.0,                        # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }

        elif Error_Code == 1:
            return {
            "status": status,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": 1.0,                        # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }

        else:
            return {
            "status": status,
            "DetectedClass": {
                "ID_1": 1.0,                        # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }

    
    # ANIMATED IMAGES
    Cartoon_Face_Result, Error_Code = check_if_cartoon(image_path)
    if Error_Code != None:                          # Exception in Animated
        return {
            "status": 0,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": 1.0,                        # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            }}
        
    if Cartoon_Face_Result == "Cartoon":
        return {
            "status": 0,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": 1.0,                        # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            }}
    
    # CLIP YOLO    
    else:
        Result2, errormedia = process_single_image(image)
        Result3, errorclip, clip_confidence, detected_class = process_image_clip(image)
        Result4, erroryolo, yolo_confidence, yolo_class = process_yolo(image)
        # errornsfw, nsfw_confidence = detect_nsfw(image)
        
        clip_confidence = float(clip_confidence) if clip_confidence is not None else 0.0
        yolo_confidence = float(yolo_confidence) if yolo_confidence is not None else 0.0
        # nsfw_confidence = float(nsfw_confidence) if nsfw_confidence is not None else 0.0

        confidence_scores['CLIP B32'] = {
            "Confidence": clip_confidence,
            "Detected Class": detected_class
        }
        
        confidence_scores['YOLO'] = {
            "Confidence": yolo_confidence,
            "Detected Class": yolo_class
        }

        accepted_count = sum([Result2 == 'Accepted', Result3 == 'Accepted', Result4 == 'Accepted'])
        
        if accepted_count >= 2:
            final_result= {
            "status": 1,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }

        elif errorclip is None and erroryolo == "sunglasses":
            final_result= {
            "status": 1,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": None,                       # Eye
                "ID_6": None,                       # Cap
            },
            "confidence_scores":{}
        }
            
        else:
            final_result= {
            "status": 0,
            "DetectedClass": {
                "ID_1": None,                       # Invalid Image
                "ID_2": None,                       # NSFW
                "ID_3": None,                       # No Face
                "ID_4": None,                       # Multiple Faces                       
                "ID_5": 1.0,                       # Eye
                "ID_6": 1.0,                       # Cap
            },
            "confidence_scores": confidence_scores
        }
    
    # Combined Result
    print("\n\nCOMBINED RESULT:")
    print(f" \n Insight Face Result: {Face_Result}, \n Media pipe Result: {Result2}, \n Clip B/32 Result: {Result3}, \n yolo Result: {Result4}, \n")
    print(f"------------------------------------------------------------------------------------------------------------------------------------")
    # print(f"\n Insight Face Error: {error1}, \n Media pipe Error: {errormedia}, \n Clip B/32 Error: {errorclip}, \n yolo error: {erroryolo}, \n NSFW error: {errornsfw}.\n")

    # Clean up temporary folders
    for folder in ['/home/abp/Documents/ABPProduction/ABP/ProfileModeration/Version16/CodeBase/TempFaces']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # Returning Final Result
    return final_result