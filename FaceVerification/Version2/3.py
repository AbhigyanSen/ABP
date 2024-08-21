import os
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from PIL import Image 
from io import BytesIO
import pandas as pd
import requests
# Path to your XLSX file
xlsx_file = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/DataRequirement.xlsx'
# Sheet from which to extract images
sheet_name = 'Driving License Front'
# Directory where images will be saved
output_folder = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version2/DrivingFront'

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the workbook and select the sheet
workbook = pd.read_excel(xlsx_file,sheet_name = sheet_name)
print(workbook.shape)
# Iterate over all the images in the specified sheet
for _,image in workbook.iterrows():
    url = image[0]
    img_name = url.split('/')[-1][:-5]
    try:
        response = requests.get(url)
        pil_image = Image.open(BytesIO(response.content)).convert("RGB")
        image_filename = f'{sheet_name}_{img_name}.png'
        image_path = os.path.join(output_folder, image_filename)
        pil_image.save(image_path)
        print(f'Saved image to {image_path}')
    except:
        print("Error Processing Image")

print('Image extraction completed.')