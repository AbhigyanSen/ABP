import os
import sys
from insightface.app import FaceAnalysis

import warnings
warnings.filterwarnings("ignore")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Constant.constant import BASE_FOLDER

from Classes.base64conversion import Base64conversion           #base64_to_image
from Classes.saveimage import SaveImage                         #save_image
from Classes.detectnsfw import Detectnsfw                       #detect_nsfw
from Classes.facedetection import Facedetecttion                #check_image
from Classes.animatedimage import Animatedimage                 #check_if_cartoon
from Classes.mediaclipyolo import Clipyolo                         #process_single_image,process_image_clip,process_yolo
from Classes.cleanup import CleanUp 
from Classes.pocr import Pocr 


# Creating the BASE FOLDER
if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

# INSIGHT-FACE
try:
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=-1)
except Exception as e:
    print(f"(33) Error Loading InsightFace Model: {e}")
    app = None


def return_status(status,idresult=[],confidence_score={},confidence=None):

    ID_1=None
    ID_2=None
    ID_3=None
    ID_4=None
    ID_5=None
    ID_6=None
    ID_7=None

    if 'ID_1' in idresult:
        ID_1=1.0 if confidence==None else confidence
    if 'ID_2' in idresult:
        ID_2=1.0 if confidence==None else confidence
    if 'ID_3' in idresult:
        ID_3=1.0 if confidence==None else confidence
    if 'ID_4' in idresult:
        ID_4=1.0 if confidence==None else confidence
    if 'ID_5' in idresult:
        ID_5=1.0 if confidence==None else confidence
    if 'ID_6' in idresult:
        ID_6=1.0 if confidence==None else confidence
    if 'ID_7' in idresult:
        ID_7=1.0 if confidence==None else confidence

    
    return {
            "status": status,
            "DetectedClass": {
                "ID_1": ID_1,                        # Invalid Image
                "ID_2": ID_2,                       # NSFW
                "ID_3": ID_3,                       # No Face
                "ID_4": ID_4,                       # Multiple Faces                       
                "ID_5": ID_5,                       # Eye
                "ID_6": ID_6,                       # Cap
                "ID_7": ID_7                        # Phone Number
            },
            "confidence_scores":confidence_score
        }



def get_result(base64_image):

    final_result = ""
    confidence_scores = {}
    status = 0 

    Base64_conversion = Base64conversion()
    # Convert base64 to image and save it as image.jpg
    image, error = Base64_conversion.base64_to_image(base64_image)

    # Error in Base64
    if error:
        return return_status(status,['ID_1'],{})
    
    Save_Image = SaveImage()
    # image_path, error = save_image(image, 'image.jpg')
    image_path, error = Save_Image.save_image(image, None) 

    if error:
        return return_status(status,['ID_1'],{})
    
    Detect_Nsfw = Detectnsfw()
    # Processing NSFW
    NSFW_String, NSFW_Confidence = Detect_Nsfw.detect_nsfw(image)

    if NSFW_String == "Image contains NSFW content":
        return return_status(status,['ID_2'],{},NSFW_Confidence)
    
    Face_detecttion = Facedetecttion()
    # No Face
    Face_Result, Error_Code = Face_detecttion.check_image(image_path,app)

    if Face_Result == "Rejected":    
        if Error_Code == 0:
            return return_status(status,['ID_3'],{})
        elif Error_Code == 1:
            return return_status(status,['ID_4'],{})
        else:
            return return_status(status,['ID_1'],{})    
    
    # POCR    
    P_Ocr = Pocr()
    Phone_Number_Result = P_Ocr.pocr(image_path)
    if Phone_Number_Result == "Rejected":
        return return_status(status,['ID_7'],{})    
    
    #  ANIMATED IMAGES
    Animated_image = Animatedimage()
    Cartoon_Face_Result, Error_Code = Animated_image.check_if_cartoon(image_path)
    
    if Error_Code != None:                          # Exception in Animated
        return return_status(status,['ID_3'],{})        
    if Cartoon_Face_Result == "Cartoon":
        return return_status(status,['ID_3'],{})  
    
    # CLIP YOLO
    Clip_yolo = Clipyolo()
    Result2, errormedia = Clip_yolo.process_single_image(image)
    Result3, errorclip, clip_confidence, detected_class = Clip_yolo.process_image_clip(image)
    Result4, erroryolo, yolo_confidence, yolo_class = Clip_yolo.process_yolo(image)

    clip_confidence = float(clip_confidence) if clip_confidence is not None else 0.0
    yolo_confidence = float(yolo_confidence) if yolo_confidence is not None else 0.0

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
        final_result= return_status(1)  

    elif errorclip is None and erroryolo == "sunglasses":
        final_result= return_status(1)
    else:
        final_result= return_status(0,['ID_5','ID_6'],confidence_scores)
    

    # Combined Result
    print("\n\nCOMBINED RESULT:")
    print(f" \n Insight Face Result: {Face_Result}, \n Media pipe Result: {Result2}, \n Clip B/32 Result: {Result3}, \n yolo Result: {Result4}, \n")
    print(f"------------------------------------------------------------------------------------------------------------------------------------")
    
    # CleanUp
    Clean_Up = CleanUp.clear_temp_folders()

    return final_result