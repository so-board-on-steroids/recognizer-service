import re
import base64
from io import BytesIO
import cv2
import numpy as np
import pytesseract
from PIL import Image
import unicodedata

def base64_to_image(data):
    b64_img = re.sub('^data:image/png;base64,', '', data)
    decoded_img = base64.b64decode(b64_img)
    pil_img = Image.open(BytesIO(decoded_img))
    return pil_img

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def image_preprocessing(img : Image):
    cv2_img = np.array(img.convert('RGB'))
    #invert to negative
    img_not = cv2.bitwise_not(cv2_img)
    #scale x3
    scale_factor = 3
    larger_img = cv2.resize(img_not, dsize=(0,0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR_EXACT)
    #convert to gray
    gray_img = cv2.cvtColor(larger_img, cv2.COLOR_RGB2GRAY)
    # convert to black-white
    black_white_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 3)
    return black_white_img

def extract_part_text(img: Image, lang='eng'):
    prepared = image_preprocessing(img)
    text = pytesseract.image_to_string(prepared, lang=lang)
    return remove_control_characters(text)
    
def extract_part_number(img: Image):
    prepared = image_preprocessing(img)
    text = pytesseract.image_to_string(prepared, lang='eng', 
        config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return remove_control_characters(text)

def extract_row_data(img : Image):
    item_name_image = img.crop((0, 0, 499, 27))
    item_price_image = img.crop((567, 12, 866, 35))
    item_count_image = img.crop((450, 30, 535, 52))
    trader_image = img.crop((937, 0, 1305, 21))
    time_remain_image = img.crop((937, 18, 970, 33))
    location_image = img.crop((937, 30, 1200, 48))
    
    item_name_text = extract_part_text(item_name_image)    
    item_price_text = extract_part_number(item_price_image)
    item_count_text = extract_part_number(item_count_image)
    trader_text_eng = extract_part_text(trader_image)
    trader_text_rus = extract_part_text(trader_image, lang='rus')
    time_remain_text = extract_part_number(time_remain_image)
    location_text = extract_part_text(location_image)
    
    key_value = dict(item_name=item_name_text,
        item_price=item_price_text,
        item_count=item_count_text,
        trader_eng=trader_text_eng,
        trader_rus=trader_text_rus,
        time_remain=time_remain_text,
        location=location_text)
        
    return key_value

def recognize_row(row_image : Image):
    row_data = extract_row_data(row_image)
    return row_data
       
