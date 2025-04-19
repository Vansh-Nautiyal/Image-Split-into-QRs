import cv2
import base64
from PIL import Image
import io
import os

def decode_qr(qr):
    img = cv2.imread(qr)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if not data:
        raise ValueError(f"No QR code found or data is invalid in {qr}")

    # Decode base64 back to image
    image_data = base64.b64decode(data)
    img_io = io.BytesIO(image_data)
    return Image.open(img_io)

def reconstruct_image(qr_files):
    print("Decoding QR codes...")
    images = [decode_qr(qr_file) for qr_file in qr_files]
    print(f"Displaying decoded images :\n ")
    for i in images :
        i.show()
    width, height = images[0].size
    print(f"Each quadrant size: {width}x{height}")

    # Create a blank image to stitch 4 parts
    new_img = Image.new('RGB', (width * 2, height * 2))

    new_img.paste(images[0], (0, 0))               # Top-left
    new_img.paste(images[1], (width, 0))           # Top-right
    new_img.paste(images[2], (0, height))          # Bottom-left
    new_img.paste(images[3], (width, height))      # Bottom-right

    new_img.save("reconstructed_image.png")
    print(f"\nReconstructed image saved as  'reconstructed_image.png' ")
    new_img.show()

qr_files = [
"part_1.png",
"part_2.png",
"part_3.png",
"part_4.png"
]

missing = [f for f in qr_files if not os.path.exists(f)]
if missing:
    print(f"Missing QR files: {missing}")
else:
    reconstruct_image(qr_files)
