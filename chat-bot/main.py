import functions_framework

import base64

import cv2
import numpy as np
from helper_functions import gaussian_blurring, convert_to_black_and_white, help_func

from encoder import encode_image_to_base64

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

    if request_json and 'action' in request_json:
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
      image_data = base64.b64decode(encoded_image)

      # Convert the binary data to a numpy array
      image = cv2.imdecode(np.frombuffer(image_data,dtype=np.uint8), cv2.IMREAD_COLOR)
      print(image)

      previous_image = image
      #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      if(action == "blurring"):
        image = gaussian_blurring(image)
        # if not np.array_equal(previous_image, image):
        #   print("Image is blurred")
      elif(action == "bw"):
        image = convert_to_black_and_white(image)

      encoded_string = encode_image_to_base64(image)
      return encoded_string

    #print("Encoded String: ", encoded_string)

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'

    return name #change this with encoded image
