import base64

def encode_image_to_base64(img):
    encoded_string = base64.b64encode(img)
    return encoded_string

