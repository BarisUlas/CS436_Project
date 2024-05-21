import cv2
from PIL import Image

import random


def gaussian_blurring(img):
    blurred_image = cv2.GaussianBlur(img, (15, 15), 0)
    image = Image.fromarray(blurred_image)
    #image.save("saved_image.png")
    return blurred_image


def convert_to_black_and_white(img):
    bw_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #cv2.imwrite("bw_image.png", bw_image)
    return bw_image

def help_func():
  print("There are 2 image processing options you can apply to your image:\nOption 1: You can blur the image by selecting option 1 (Please write \"!bot blur\" for option 1)\nOption 2: You can convert the image background to black and white (Please write \"!bot bw\" for option 2)\nif you send a help command, this help documentation emerges :)\n")
