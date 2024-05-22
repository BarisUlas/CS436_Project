import cv2
from PIL import Image


def gaussian_blurring(img):
    blurred_image = cv2.GaussianBlur(img, (15, 15), 0)
    image = Image.fromarray(blurred_image)
    #image.save("saved_image.png")
    return blurred_image


def convert_to_black_and_white(img):
    bw_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #cv2.imwrite("bw_image.png", bw_image)
    return bw_image
