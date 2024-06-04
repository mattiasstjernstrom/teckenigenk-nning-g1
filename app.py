from flask import Flask, request, jsonify, redirect, url_for, render_template
from PIL import Image
import base64
import os
from datetime import datetime
from models import train_rf_mnist, predict_digit
import numpy as np

app = Flask(__name__)

# Blueprint for main routes:
from main import main as main_routes

app.register_blueprint(main_routes)

# Set the path for the drawn images folder
IMAGES_FOLDER = 'drawn_images'
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

rf_mnist_model = train_rf_mnist()

@app.route('/upload-drawing', methods=['POST'])
def upload_drawing():
    data = request.get_json()
    image_data = data['image']
    
    # Decode the base64 image
    image_data = image_data.split(",")[1]
    
    # Create a unique filename using the current date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    image_filename = os.path.join(IMAGES_FOLDER, f"{timestamp}.png")
    
    with open(image_filename, "wb") as fh:
        fh.write(base64.b64decode(image_data))
    
    # Open the saved image with Pillow
    img = Image.open(image_filename)
    
    # Predict the digit using the model
    prediction = predict_digit(rf_mnist_model, img)
    
    # Return a success message with the prediction and filenames
    return jsonify({'status': 'success', 'filename': image_filename, 'prediction': int(prediction)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)