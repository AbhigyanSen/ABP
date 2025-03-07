import os
import shutil
import base64
import cv2
import torch
from PIL import Image, ExifTags
from io import BytesIO
import requests
from transformers import AutoModelForImageClassification, ViTImageProcessor
import clip
from ultralytics import YOLO
import mediapipe as mp
import face_recognition
from insightface.app import FaceAnalysis
import numpy as np
from transformers import CLIPProcessor, CLIPModel
import time

# Unique ID
import uuid
from datetime import datetime

# Warnings Ignore
import warnings
warnings.filterwarnings("ignore")

BASE_FOLDER = "/home/abp/Documents/ABPProduction/ABP/ProfileModeration/Version17/API2/Demo" 
YOLO_FOLDER = "/home/abp/Documents/ABPProduction/ABP/ProfileModeration/Version17/API2/best.pt"

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

# MEDIAPIPE
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.0,
    min_tracking_confidence=0.90
)

# CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"

clip_model, preprocess = clip.load("ViT-B/32", device=device)
text = ["a cap", "a hat", "a sunglass", "a helmet", "a reading glass", "a mask"]
text_tokens = clip.tokenize(text).to(device)

# CLIP RN101 Model
RNmodel, RNpreprocess = clip.load("RN101", device=device)
rn101textlist = ["a sunglass", "a reading glass"]
rn101text = clip.tokenize(rn101textlist).to(device)

# CLIP ANIME
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# YOLO
yolo_model = YOLO(YOLO_FOLDER)
mapping = {0 : "sunglasses", 1 : "sunglasses", 2 : "eyeglasses", 3 : "headware", 4 : "headware", 5 : "headware"}

# Coversion to Image
def base64_to_image(base64_str):
    start_time = time.time()  # Start time measurement
    
    # print(f"BASE64: \n\n{base64_str}")
    # print("\n\n")

    try:
        # Decode Base64 string
        image_data = base64.b64decode(base64_str)
        
        # Open image using PIL
        image = Image.open(BytesIO(image_data))
        
        # Check and correct image orientation based on EXIF metadata
        try:
            # If the image has EXIF data, correct orientation
            exif = image._getexif()
            if exif:
                for tag, value in exif.items():
                    if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'Orientation':
                        if value == 3:
                            image = image.rotate(180, expand=True)
                        elif value == 6:
                            image = image.rotate(270, expand=True)
                        elif value == 8:
                            image = image.rotate(90, expand=True)
                        break
        except Exception as exif_error:
            print(f"(87) EXIF correction failed: {exif_error}")
        
        # Convert image to RGB and then to NumPy array
        image = image.convert("RGB")
        image = np.array(image)
        
        print("(93) Base64 Try")
        return image, None
    
    except Exception as e:
        print("(96) Base64 Except")
        return None, str(e)
    
    finally:
        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time
        print(f"(base64_to_image) Time taken: {elapsed_time:.4f} seconds")
    

# Saving the Converted Image
def save_image(image, image_name=None):
    start_time = time.time()  # Start time measurement
    
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
    finally:
        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time
        print(f"(save_image) Time taken: {elapsed_time:.4f} seconds")

# NSFW Detection
def detect_nsfw(image):
    start_time = time.time()  # Start time measurement
    
    try:
        print("(114) NSFW Try")
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
        print("(133) NSFW Except")
        return str(e), None
    finally:
        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time
        print(f"(detect_nsfw) Time taken: {elapsed_time:.4f} seconds")

# Cropping the Face from the Image (If Face Exists {Face Recognition})
def crop_faces(image, output_dir, expansion_factor=0.3):
    start_time = time.time()  # Start time measurement
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        print("(141) Face Recognition Try")
        image = np.array(image)
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) != 1:
            return False, 'Multiple faces detected' if len(face_locations) > 1 else 'No Face Detected'
        
        pil_image = Image.fromarray(image)
        base_name = 'face.jpg'
        name, ext = os.path.splitext(base_name)
        top, right, bottom, left = face_locations[0]
        height, width, _ = image.shape
        expansion_width = int((right - left) * expansion_factor)
        expansion_height = int((bottom - top) * expansion_factor)
        new_top = max(0, top - expansion_height)
        new_bottom = min(height, bottom + expansion_height)
        new_left = max(0, left - expansion_width)
        new_right = min(width, right + expansion_width)
        face_image = pil_image.crop((new_left, new_top, new_right, new_bottom))
        face_path = os.path.join(output_dir, f"{name}{ext}")
        face_image.save(face_path)
        return True, None
    except Exception as e:
        print("(164) Face Recognition Exception")
        return False, str(e)
    finally:
        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time
        print(f"(crop_faces) Time taken: {elapsed_time:.4f} seconds")

# Saving the Largest Face (Multiple Faces)
def save_face(largestface, image, output_dir, expansion_factor=0.3):
    start_time = time.time()  # Start time measurement
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        print("(172) Largest Face Try")
        image = np.array(image)
        pil_image = Image.fromarray(image)
        base_name = 'face.png'
        name, ext = os.path.splitext(base_name)
        left, top, right, bottom = largestface.bbox
        height, width, _ = image.shape
        expansion_width = int((right - left) * expansion_factor)
        expansion_height = int((bottom - top) * expansion_factor)
        new_top = max(0, top - expansion_height)
        new_bottom = min(height, bottom + expansion_height)
        new_left = max(0, left - expansion_width)
        new_right = min(width, right + expansion_width)
        face_image = pil_image.crop((new_left, new_top, new_right, new_bottom))
        face_path = os.path.join(output_dir, f"{name}{ext}")
        face_image.save(face_path)
        return True, None
    except Exception as e:
        print("(190) Largest Face Except")
        return False, str(e)
    finally:
        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time
        print(f"(save_face) Time taken: {elapsed_time:.4f} seconds")

# Insight Face Processing
def check_image(image_path):
    start_time = time.time()  # Start time measurement
    
    # Create a dynamic output directory based on the current time
    current_time = datetime.now().strftime("%H%M%S")
    output_dir = f'Temp{current_time}'
    
    try:
        print("(196) Insight Face Processing Try")
        img = cv2.imread(image_path)
        faces = app.get(img)  # Assuming 'app' is a pre-initialized face detection model
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if len(faces) == 1:
            success, error = crop_faces(Image.open(image_path), output_dir)
            if success:
                return 'Accepted', None
            else:
                if error == "No Face Detected":
                    print("No Face Detected")
                    return "Rejected", 0
                elif error == "Multiple faces detected":
                    print("(210) Multiple Faces")
                    return 'Rejected', 1
                else:
                    print("Face Cropping Failed")
                    return "Rejected", 2
                
        elif len(faces) > 1:
            areas = []
            largestfacearea = 0
            largestfaceindex = None
            for index, face in enumerate(faces):
                bbox = face.bbox
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                areas.append(area)
                if area > largestfacearea:
                    largestfaceindex = index
                    largestfacearea = area
            areas.sort(reverse=True)
            area_difference = (areas[0] - areas[1]) / areas[0]
            if area_difference > 0.80:
                largestface = faces[largestfaceindex]
                success, error = save_face(largestface, Image.open(image_path), output_dir)
                if success:
                    return 'Accepted', None
                else:
                    print("Face Cropping Failed for Largest Face")
                    return 'Rejected', 2
            else:
                print("Multiple Faces found for Largest Face")
                return 'Rejected', 1
        else:
            confidence_scores = [face.det_score for face in faces] if faces else []
            error_msg = f"No Face Detected. Face Confidence Score: {confidence_scores[0]}" if confidence_scores else "No Face Detected"
            return 'Rejected', 0
    except Exception as e:
        print("(243) Insight Face Processing Exception")
        return 'Rejected', 2
    finally:
        end_time = time.time()  # End time measurement
        elapsed_time = end_time - start_time
        print(f"(check_image) Time taken: {elapsed_time:.4f} seconds")
        
# ANIMATED IMAGE
def check_if_cartoon(image_path):
    start_time = time.time()
    try:
        image = Image.open(image_path)
        inputs = processor(text=["image of a real person", "animated image or image of cartoon image"], images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1)
        result_index = torch.argmax(probs)
        if result_index == 1:
            print("Animated Image Detected")
            return "Cartoon", None
        else:
            return "Real", None
    except Exception as e:
        print("Animated Image Exception")
        return None, str(e)
    finally:
        end_time = time.time()
        print(f"(check_if_cartoon) Time taken: {end_time - start_time:.4f} seconds")

# MediaPipe Processing
def detect_landmarks(image):
    start_time = time.time()
    print("(249) Mediapipe Processing")
    results = mp_face_mesh.process(cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return None
    end_time = time.time()
    print(f"(detect_landmarks) Time taken: {end_time - start_time:.4f} seconds")
    return results.multi_face_landmarks[0]

# Mediapipe Face Processing
def process_single_image(image):
    start_time = time.time()
    try:
        print("(258) Mediapipe Single Image Processing")
        image_top = image[:image.shape[0] // 2, :]
        image_bottom = image[image.shape[0] // 2:, :]
        landmarks_top = detect_landmarks(image_top)
        landmarks_bottom = detect_landmarks(image_bottom)
        top_face_detected = landmarks_top is not None
        bottom_face_detected = landmarks_bottom is not None
        Result2 = 'Accepted' if top_face_detected and bottom_face_detected else 'Rejected'
        error_message = ""
        if Result2 == 'Rejected':
            if not top_face_detected:
                error_message += "Top Face Error; "
            if not bottom_face_detected:
                error_message += "Bottom Face Error; "
            error_message = error_message.rstrip("; ")
            
        end_time = time.time()
        print(f"(process_single_image) Time taken: {end_time - start_time:.4f} seconds")
        return Result2, error_message
    except Exception as e:
        print("(276) Mediapipe Single Image Exception")
        end_time = time.time()
        print(f"(process_single_image) Time taken: {end_time - start_time:.4f} seconds")
        return 'Rejected', str(e)

# CLIP Processing
def process_image_clip(image):
    start_time = time.time()
    try:
        print("(243) CLIP B32 Processing Try")
        image = Image.fromarray(image)  # Converts NumPy array to PIL Image
        B32image = preprocess(image).unsqueeze(0).to(device)  # Converts PIL Image to Tensor
        
        with torch.no_grad():
            logits_per_image, logits_per_text = clip_model(B32image, text_tokens)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        
        predicted_index = probs.argmax()
        confidence = probs[0][predicted_index]
        detected_class = text[predicted_index]
        print(f"\nB32 Detected Class: {detected_class} and Confidence: {confidence}\n")
        
        if confidence > 0.5 and (detected_class == "a sunglass" or detected_class == "a reading glass"):            
            if detected_class in ["a sunglass", "a reading glass"]:
                print("(298) CLIP RN101 Processing Try")

                with torch.no_grad():
                    rn101_logits_per_image, rn101_logits_per_text = RNmodel(B32image, rn101text)
                    rn101_probs = rn101_logits_per_image.softmax(dim=-1).cpu().numpy()
                rn101_predicted_index = rn101_probs.argmax()
                rn101_confidence = rn101_probs[0][rn101_predicted_index]
                RNdetected_class = rn101textlist[rn101_predicted_index]
                print(f"\nRN101 Confidence: {rn101_confidence} Predicted Class RN101: {RNdetected_class}\n")

                if rn101_confidence > 0.5 and rn101textlist[rn101_predicted_index] == "a reading glass":
                    print("Accepted by RN101 for Eyeglasses")
                    end_time = time.time()
                    print(f"(process_image_clip) Time taken: {end_time - start_time:.4f} seconds")
                    return "Accepted", None, confidence, detected_class
                else:
                    end_time = time.time()
                    print(f"(process_image_clip) Time taken: {end_time - start_time:.4f} seconds")
                    return "Rejected", f"Error: {detected_class}", confidence, detected_class
            else:
                end_time = time.time()
                print(f"(process_image_clip) Time taken: {end_time - start_time:.4f} seconds")
                return "Rejected", f"Error: {detected_class}", confidence, detected_class
        
        elif confidence > 0.8:                                                              # Rejection for Headware
            end_time = time.time()
            print(f"(process_image_clip) Time taken: {end_time - start_time:.4f} seconds")
            return "Rejected", f"Error: {detected_class}", confidence, detected_class
        
        else:
            end_time = time.time()
            print(f"(process_image_clip) Time taken: {end_time - start_time:.4f} seconds")
            return "Accepted", None, confidence, detected_class
        
    except Exception as e:
        print("(323) CLIP Processing Exception")
        end_time = time.time()
        print(f"(process_image_clip) Time taken: {end_time - start_time:.4f} seconds")
        return 'Rejected', str(e), 0, None

# YOLO Processing
def process_yolo(image):
    start_time = time.time()
    try:
        print("(329) YOLO Processing Try")
        image = Image.fromarray(image)
        results = yolo_model(image)
        
        if len(results[0].boxes) == 0:
            end_time = time.time()
            print(f"(process_yolo) Time taken: {end_time - start_time:.4f} seconds")
            return "Accepted", None, None, None
        
        conf = torch.max(results[0].boxes.conf).item()
        
        if conf < 0.8:
            end_time = time.time()
            print(f"(process_yolo) Time taken: {end_time - start_time:.4f} seconds")
            return "Accepted", None, conf, None
        
        z = torch.argmax(results[0].boxes.conf).item()
        a = int(results[0].boxes.cls[z].item())
        detected_class = mapping[a]
        print(f"YOLO Class: {detected_class} and Confidence: {conf}")
        
        if a == 2:                                          # Eyeglasses
            print("(347) YOLO Eyeglass Acceptance")
            end_time = time.time()
            print(f"(process_yolo) Time taken: {end_time - start_time:.4f} seconds")
            return "Accepted", None, conf, detected_class
        end_time = time.time()
        print(f"(process_yolo) Time taken: {end_time - start_time:.4f} seconds")
        return "Rejected", detected_class, conf, detected_class
    
    except Exception as e:
        print("(352) YOLO Exception")
        end_time = time.time()
        print(f"(process_yolo) Time taken: {end_time - start_time:.4f} seconds")
        return "Rejected", f"{e}", None, None
        
# Clean-Up        
def clear_temp_folders(directory):
    # Iterate through all items in the specified directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Check if the item is a directory and starts with 'Temp'
        if os.path.isdir(item_path) and item.startswith('Temp'):
            try:
                shutil.rmtree(item_path)  # Remove the directory and its contents
                print(f"Removed: {item_path}")
            except Exception as e:
                print(f"Error removing {item_path}: {e}")

# Specify the directory to check
# target_directory = 'D:\ABP'
        
    
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

    # Clean up temporary folder
    # if os.path.exists(output_dir):
        # shutil.rmtree(output_dir)
        
    clear_temp_folders("/home/dcsadmin/Documents/ABP_FaceOcclusion/ABP/ProfileModeration/Version17/")
    
    # Returning Final Result
    return final_result