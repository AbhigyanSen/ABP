# Module for Face-Verification (InsightFace and FaceRecognition)

import os
import numpy as np
import cv2
from PIL import Image
import face_recognition
from insightface.app import FaceAnalysis


BASE_FOLDER = "/home/abp/Documents/ABPProduction/ABP/ProfileModeration/Version13/CodeBase/Modules/Demo"

# Creating the BASE FOLDER
if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

# INSIGHT-FACE
try:
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=-1)
except Exception as e:
    print(f"(30) Error Loading InsightFace Model: {e}")
    app = None


# Cropping the Face from the Image (If Face Exists {Face Recognition})
def crop_faces(image, output_dir, expansion_factor=0.3):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        print("(112) Face Recognition Try")
        image = np.array(image)
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) != 1:
            return False, 'Multiple faces detected' if len(face_locations) > 1 else 'No Face Detected'
        
        pil_image = Image.fromarray(image)
        base_name = 'face.png'
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
        print("(135) Face Recognition Exception")
        return False, str(e)

# Saving the Largest Face (Multiple Faces)
def save_face(largestface, image, output_dir, expansion_factor=0.3):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        print("(143) Largest Face Try")
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
        print("(161) Largest Face Except")
        return False, str(e)

# Insight Face Processing
def check_image(image_path):
    try:
        print("(167) Insight Face Processing Try")
        img = cv2.imread(image_path)
        faces = app.get(img)
        
        if len(faces) == 1:
            success, error = crop_faces(Image.open(image_path), 'TempFaces')
            if success:
                return 'Accepted', None
            else:
                if error == "No Face Detected":
                    return "Rejected", 0
                elif error == "Multiple faces detected":
                    return 'Rejected', 1
                else:
                    return "Rejected", 2        #Face cropping failed'
                
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
                success, error = save_face(largestface, Image.open(image_path), "TempFaces")
                if success:
                    return 'Accepted', None
                else:
                    return 'Rejected', 2
                    # return 'Rejected', error if error else 'Face cropping failed'
            else:
                return 'Rejected', 1
                # return 'Rejected', 'Multiple faces detected'
        else:
            confidence_scores = [face.det_score for face in faces] if faces else []
            error_msg = f"No Face Detected. Face Confidence Score: {confidence_scores[0]}" if confidence_scores else "No Face Detected"
            return 'Rejected', 0
            # return 'Rejected', error_msg
    except Exception as e:
        print("(204) Insight Face Processing Exception")
        return 'Rejected', 2
        # return 'Rejected', str(e)