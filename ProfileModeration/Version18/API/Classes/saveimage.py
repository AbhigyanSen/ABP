import sys
import os
import time
import uuid
from datetime import datetime
from PIL import Image, ExifTags
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Constant.constant import BASE_FOLDER

class SaveImage:

    def __init__(self):
        pass

    def save_image(self,image, image_name=None):
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
