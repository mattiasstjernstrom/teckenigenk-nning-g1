import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from PIL import Image


def load_mnist_data():
    # Load MNIST dataset
    df_mnist_train = pd.read_csv("data/mnist_train_sample.csv")
    df_mnist_test = pd.read_csv("data/mnist_test_sample.csv")
    return df_mnist_train, df_mnist_test

# Mappning av modellens utgångar till tecken (0-9)
labels = '0123456789'

# Träna modellen
def train_rf_mnist():
    df_mnist_train, df_mnist_test = load_mnist_data()

    X_train = df_mnist_train.drop(columns=['label'])
    y_train = df_mnist_train['label']
    X_test = df_mnist_test.drop(columns=['label'])
    y_test = df_mnist_test['label']
    
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    
    accuracy = rf.score(X_test, y_test)
    print(f"MNIST Model Accuracy: {accuracy}")
    return rf

# Predict the digit based on user input
def predict_digit(model, input_image):
    # Convert input image to the same format as the training data
    input_image = input_image.convert("L")  # Convert to grayscale
    input_image = input_image.resize((28, 28))  # Resize to 28x28
    input_array = np.array(input_image).reshape(1, -1)  # Flatten to a 1D array
    input_array = 255 - input_array  # Invert colors (if necessary)

    # Ensure the input data is a DataFrame with the same columns as the training data
    input_df = pd.DataFrame(input_array, columns=[f'pixel{i}' for i in range(784)])
    
    prediction = model.predict(input_df)
    return prediction[0]