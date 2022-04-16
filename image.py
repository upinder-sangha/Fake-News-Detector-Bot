import os
from dotenv import load_dotenv
import pytesseract
from skimage import io
import cv2


pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# noise removal
def remove_noise_img(image):
    return cv2.GaussianBlur(image,(1,1),cv2.BORDER_DEFAULT) 



def extract_text(message,bot):
	file_id = message.json['photo'][-1]['file_id']
	image_location_info = bot.get_file(file_id)
	# print(TELEGRAM_API_KEY)
	image_url = 'https://api.telegram.org/file/bot'+TELEGRAM_API_KEY+'/'+image_location_info.file_path
	# print(image_url)
	img = io.imread(image_url)
	# gray_img = get_grayscale(img)
	# thresh_img = thresholding(gray_img)
	# clean_img = remove_noise_img(gray_img)
	extracted_text = pytesseract.image_to_string(img)
	return extracted_text