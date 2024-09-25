import os
import sys
import time
from datetime import datetime
import cv2
from PIL import Image, ExifTags
from insightface.app import FaceAnalysis
import numpy as np
import face_recognition
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Constant.constant import OUTPUT_TEMP_FOLDER_PATH

class Facedetecttion:

    def __init__(self):
        pass

    def check_image(self,image_path,app):
        start_time = time.time()  # Start time measurement
        
        # Create a dynamic output directory based on the current time
        current_time = datetime.now().strftime("%H%M%S")
        #output_dir = f'{OUTPUT_TEMP_FOLDER_PATH}Temp{current_time}'
        output_dir = os.path.join(OUTPUT_TEMP_FOLDER_PATH, f'Temp{current_time}')
        
        try:
            print("(196) Insight Face Processing Try",image_path)
            img = cv2.imread(image_path)
            
            faces = app.get(img)  # Assuming 'app' is a pre-initialized face detection model
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if len(faces) == 1:
                print("img1",output_dir)
                success, error = self.crop_faces(Image.open(image_path), output_dir)
                print("img2")
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
                    success, error = self.save_face(largestface, Image.open(image_path), output_dir)
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
    

    def crop_faces(self,image, output_dir, expansion_factor=0.3):
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
    def save_face(self,largestface, image, output_dir, expansion_factor=0.3):
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
