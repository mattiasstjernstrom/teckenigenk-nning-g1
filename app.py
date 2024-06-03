from flask import Flask, request, jsonify, redirect, url_for, render_template
from PIL import Image
import base64
import os
from datetime import datetime
from models import train_rf_mnist
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
    
    # Öppna den sparade bilden med Pillow
    img = Image.open(image_filename)
    
    # Konvertera till svartvit
    bw_img = img.convert('L')
    
    # Ändra storlek till 28x28
    resized_img = bw_img.resize((28, 28))
    
    # Spara den bearbetade bilden
    resized_image_filename = os.path.join(IMAGES_FOLDER, f"{timestamp}_resized.png")
    resized_img.save(resized_image_filename)
    
    # Omvandla bilden till en array av numeriska värden
    image_array = np.array(resized_img)
    
    # Omvandla 2D-arrayen till en 1D-array för att passa in i modellen
    image_data = image_array.flatten()
    
    # Gör förutsägelser med modellen
    prediction = rf_mnist_model.predict([image_data])
    
    # Returnera en framgångsmeddelande
    return jsonify({'status': 'success', 'filename': image_filename, 'resized_filename': resized_image_filename, 'prediction': int(prediction[0])})

@app.route('/clear', methods=['GET'])
def clear_and_redirect():
    # Om det finns en specifik funktion för att rensa något på servern kan du kalla på den här.
    # clearCanvasFunction()  # Om du har en sådan funktion

    # Omdirigera till startsidan
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)