from PIL import Image
import qrcode
import base64
import os
import io 

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG", optimize=True)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def split_image(image):
    width, height = image.size
    return [
        image.crop((0, 0, width // 2, height // 2)),         # top-left
        image.crop((width // 2, 0, width, height // 2)),     # top-right
        image.crop((0, height // 2, width // 2, height)),    # bottom-left
        image.crop((width // 2, height // 2, width, height)) # bottom-right
    ]

def create_qr(data, filename):
    qr = qrcode.QRCode(
        version=40, 
        error_correction=qrcode.constants.ERROR_CORRECT_Q, 
        box_size=8,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white")
    img_qr.save(filename)

original_image="landscape.png"
if not os.path.exists(original_image):
    print(f"Image file '{original_image}' not found.")

image = Image.open(original_image)
quadrants = split_image(image)

for i, quadrant in enumerate(quadrants):
    b64_data = image_to_base64(quadrant)
    filename = f"part_{i+1}.png"
    create_qr(b64_data, filename)
    print(f"QR Code saved: {filename}")

