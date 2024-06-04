from flask import Flask, request, jsonify, redirect, url_for, render_template
from PIL import Image
import base64
import os
from datetime import datetime
from models import train_RF, predict_digit, train_KNN
import numpy as np

app = Flask(__name__)

# Blueprint for main routes:
from main import main as main_routes

app.register_blueprint(main_routes)

# Set the path for the drawn images folder
IMAGES_FOLDER = 'drawn_images'
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

rf_mnist_model = train_RF()
KNN_mnist_model = train_KNN()

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
    
    # Convert image to white background
    img = img.convert("RGBA")
    white_bg = Image.new("RGBA", img.size, "WHITE")
    img = Image.alpha_composite(white_bg, img).convert("L")
    
    # Save the image with a white background
    img.save(image_filename)
    
    # Print the image filename to ensure it was saved correctly
    print("Saved image filename:", image_filename)
    
    # Predict the digit using the model
    prediction_RF = predict_digit(rf_mnist_model, img)
    prediction_KNN = predict_digit(KNN_mnist_model, img)
    
    # Print the prediction to check if it's correct
    print("Prediction:", prediction_RF)
    print("Prediction:", prediction_KNN)
    
    # Return a success message with the prediction and filenames
    return jsonify({'status': 'success',
                     'filename': image_filename,
                       'prediction_RF': int(prediction_RF),
                       'prediction_KNN': int(prediction_KNN)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)