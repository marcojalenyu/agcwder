from flask import Flask, render_template, request, send_file
import cv2
import os
import numpy as np
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# AGCWD algorithm function
def agcwd(image, w=0.5):
    is_colorful = len(image.shape) >= 3
    img = extract_value_channel(image) if is_colorful else image
    img_pdf = get_pdf(img)
    max_intensity = np.max(img_pdf)
    min_intensity = np.min(img_pdf)
    w_img_pdf = max_intensity * (((img_pdf - min_intensity) / (max_intensity - min_intensity)) ** w)
    w_img_cdf = np.cumsum(w_img_pdf) / np.sum(w_img_pdf)
    l_intensity = np.arange(0, 256)
    l_intensity = np.array([255 * (e / 255) ** (1 - w_img_cdf[e]) for e in l_intensity], dtype=np.uint8)
    enhanced_image = np.copy(img)
    height, width = img.shape
    for i in range(0, height):
        for j in range(0, width):
            intensity = enhanced_image[i, j]
            enhanced_image[i, j] = l_intensity[intensity]
    enhanced_image = set_value_channel(image, enhanced_image) if is_colorful else enhanced_image
    return enhanced_image

# Utility functions for AGCWD algorithm
def extract_value_channel(color_image):
    color_image = color_image.astype(np.float32) / 255.
    hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    return np.uint8(v * 255)

def get_pdf(gray_image):
    height, width = gray_image.shape
    pixel_count = height * width
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    return hist / pixel_count

def set_value_channel(color_image, value_channel):
    value_channel = value_channel.astype(np.float32) / 255
    color_image = color_image.astype(np.float32) / 255.
    color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    color_image[:, :, 2] = value_channel
    color_image = np.array(cv2.cvtColor(color_image, cv2.COLOR_HSV2BGR) * 255, dtype=np.uint8)
    return color_image

# Define route for homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    input_image_b64 = None
    enhanced_image_b64 = None
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')

        file = request.files['file']

        # Check if the file is an image
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            # Read the uploaded image
            nparr = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Apply AGCWD enhancement
            enhanced_image = agcwd(img)

            # Save the enhanced image temporarily
            _, input_image_b64 = cv2.imencode('.png', img)
            _, enhanced_image_b64 = cv2.imencode('.png', enhanced_image)

            input_image_b64 = base64.b64encode(input_image_b64).decode('utf-8')
            enhanced_image_b64 = base64.b64encode(enhanced_image_b64).decode('utf-8')
            
    return render_template('index.html', input_image=input_image_b64, enhanced_image=enhanced_image_b64)

if __name__ == '__main__':
     app.run(debug=True)

