import functions_framework

import base64

import cv2
import numpy as np
from helper_functions import gaussian_blurring, convert_to_black_and_white

from encoder import png_to_base64

from PIL import Image
import io

def base64_to_png(base64_string, output_file_path):
    # Decode the base64 string into bytes
    image_data = base64.b64decode(base64_string)
    
    # Create an image from the binary data
    image = Image.open(io.BytesIO(image_data))
    
    # Save the image as a PNG file
    image.save(output_file_path, 'PNG')


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "action" in request_json:
      if request_json['action'] == "help":
        return "There are 2 image processing options you can apply to your image:\nOption 1: You can blur the image by selecting option 1 (Please write \"!bot blur\" for option 1)\nOption 2: You can convert the image background to black and white (Please write \"!bot bw\" for option 2)\nif you send a help command, this help documentation emerges :)\n"

    image_received = True

    if request_json and 'image' in request_json:
      encoded_image = request_json['image']
      action = request_json['action']
    elif request_args and 'image' in request_args:
      encoded_image = request_args['image']
      action = request_json['action']
    else:
      print("Image cannot be received")
      image_received = False

    encoded_string = ""
    if(image_received):
      # Decode the base64 string into binary data
      base64_to_png(encoded_image, "out.png")

      img = cv2.imread("out.png")

      # Convert the binary data to a numpy array
      image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

      #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      if(action == "blurring"):
        image = gaussian_blurring(image_rgb)
        cv2.imwrite("blurred_image.png", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))  # Convert back to BGR before saving
        encoded_string = png_to_base64("./blurred_image.png")
      elif(action == "bw"):
        image = convert_to_black_and_white(image_rgb)
        cv2.imwrite("bw_image.png", image)
        encoded_string = png_to_base64("./bw_image.png")
        
      return encoded_string

    return ("Please give valid arguments", 200) #change this with encoded image
