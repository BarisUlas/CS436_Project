import base64
from PIL import Image
import io

def png_to_base64(image_path):
    # Open the image file
    with Image.open(image_path) as image:
        # Convert image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()
        
        # Encode bytes to base64 string
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        
    return base64_string
