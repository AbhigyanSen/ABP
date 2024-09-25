
from PIL import Image, ExifTags
from io import BytesIO
import base64
import time
import numpy as np

class Base64conversion:

    def __init__(self):
        pass

    def base64_to_image(self,base64_str):
        start_time = time.time()  # Start time measurement

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
 