import cv2
from PIL import Image

import random


class colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


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

def convert_text_color(text):
    options = [
     colors.RED + text + colors.RESET,
     colors.GREEN + text + colors.RESET,
     colors.YELLOW + text + colors.RESET,
     colors.BLUE + text + colors.RESET,
     colors.MAGENTA + text + colors.RESET,
     colors.CYAN + text + colors.RESET,
     colors.WHITE + text + colors.RESET
    ]

    new_text = options[random.randint(0, len(options) - 1)]
    return new_text

