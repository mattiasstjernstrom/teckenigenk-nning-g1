from flask import Flask, request, jsonify
from PIL import Image
import base64
import io
from models import train_RF, predict_EMNIST, train_KNN_EMNIST, train_ANN

app = Flask(__name__)

# Blueprint for main routes:
from main import main as main_routes

app.register_blueprint(main_routes)

print('Training Random Forest....')
rf_mnist_model = train_RF()
print('Training K Nearest Neighbors....')
KNN_EMNIST_model = train_KNN_EMNIST()
print('Training ANN....')
ANN_model = train_ANN()

@app.route('/upload-drawing', methods=['POST'])
def upload_drawing():
    data = request.get_json()
    image_data = data['image']
    
    # Decode the base64 image
    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)
    
    # Create an image object from the decoded bytes
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert image to white background and grayscale
    img = img.convert("RGBA")
    white_bg = Image.new("RGBA", img.size, "WHITE")
    img = Image.alpha_composite(white_bg, img).convert("L")
    
    # Predict the digit using the model
    prediction_RF = predict_EMNIST(rf_mnist_model, img)
    prediction_EMNIST_KNN = predict_EMNIST(KNN_EMNIST_model, img)
    prediction_ANN = predict_EMNIST(ANN_model, img)

    
    # Print the prediction to check if it's correct
    print("Prediction RF:", prediction_RF)
    print("Prediction KNN:", prediction_EMNIST_KNN)
    print('prediction ANN:', prediction_ANN)
    
    # Return a success message with the prediction
    return jsonify({'status': 'success',
                    'prediction_RF': prediction_RF,
                    'prediction_KNN_EMNIST': prediction_EMNIST_KNN,
                    'prediction_ANN': prediction_ANN})

if __name__ == "__main__":
    app.run(port=5000)
