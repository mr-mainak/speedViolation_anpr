import cv2
import pandas as pd
import numpy as np
from tracker import *
from speed import *
import pytesseract
import imutils
import easyocr

class utils:
    def __init__(self):
        self.count = 0

    def yolobbox2bbox(self, boxes):
        x, y, w, h, _, _ = boxes
        x1, y1 = x, y
        x2, y2 = x+w, y+h
        return x1, y1, x2, y2

    def cleanup_text(self, text):
        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV
        return "".join([c if ord(c) < 128 else "" for c in text]).strip()

    def build_tesseract_options(self, psm):
        # tell Tesseract to only OCR alphanumeric characters
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        # set the PSM mode
        options += " --psm {}".format(psm)
        # return the built options string
        return options
    
    def get_number(self,image):
        # OCR the license plate
        reader = easyocr.Reader(['en'], gpu=False)
        # options = self.build_tesseract_options(psm=6)
        resize = cv2.resize(image, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
        lpText = reader.readtext(resize, detail = 0)
        return lpText

    def isbelow(self, boxes, config, image):
        y1 = config[0]["trigger_line"]["line"][0][1]
        y2 = config[0]["trigger_line"]["line"][1][1]
        for box in boxes:
            # print(box)
            xa, ya, xb, yb = self.yolobbox2bbox(boxes=box)
            # print(xa,ya,xb,yb)
            _, _, _, _, cls, _ = box
            if cls in [0, 9, 10, 11, 16, 17, 18]:
                centre = yb
                if (centre > y1) and (centre > y2):
                    cropped_image = image[ya:yb, xa:xb]
                    return cropped_image
    
    def convert2labels(self,cls_id):
        if cls_id == 0:
            return "CAR"
        elif cls_id == 9:
            return "CAR"
        elif cls_id == 10:
            return "CAR"
        elif cls_id == 11:
            return "CAR"
        elif cls_id == 16:
            return "CAR"
        elif cls_id == 17:
            return "CAR"
        elif cls_id == 18:
            return "TWO_WHELLER"
        
