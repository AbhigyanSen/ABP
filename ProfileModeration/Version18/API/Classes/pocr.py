# import os
# import time
# import cv2
# import numpy as np
from paddleocr import PaddleOCR
from Constant.constant import ocr, PATTERN
# import torch

class Pocr :

    def __init__(self):
        pass
    
    def pocr(img_path):
        # img_path = 'PaddleOCR/doc/imgs_en/img_12.jpg'
        result = ""
        try:
            result = ocr.ocr(img_path, cls=True)
        except:
            ocr = PaddleOCR(use_angle_cls=True, lang='en',show_log=False)
            result = ocr.ocr(img_path, cls=True)

        if result[0] == None:
            return "Accepted"      
        rsltstr = ""    
        print(f"Result: {result}\n")
        for idx in range(len(result[0])):
            res = result[0][idx]
            rsltstr += res[1][0]
        mobile_numbers_ocr = re.findall(PATTERN, rsltstr)
        if(len(mobile_numbers_ocr)>=1):
            return "Rejected"
        return "Accepted"