import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
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

def train_KNN():
    df_mnist_train, df_mnist_test = load_mnist_data()
    
    X_train = df_mnist_train.drop(columns=['label'])
    y_train = df_mnist_train['label']
    X_test = df_mnist_test.drop(columns=['label'])
    y_test = df_mnist_test['label']

    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X_train,y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'KNN Model Accuracy: {accuracy}')
    return clf



# Träna modellen
def train_RF():
    df_mnist_train, df_mnist_test = load_mnist_data()

    X_train = df_mnist_train.drop(columns=['label'])
    y_train = df_mnist_train['label']
    X_test = df_mnist_test.drop(columns=['label'])
    y_test = df_mnist_test['label']
    
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train, y_train)
    
    accuracy = rf.score(X_test, y_test)
    print(f"RF Model Accuracy: {accuracy}")
    return rf


def predict_digit(model, input_image):

    input_image = input_image.convert("L")  # Konverterar till gråskala
    input_image = input_image.resize((28, 28))  # Skala om till 28x28

    input_array = np.array(input_image) # Bilden konverteras till en np-array
    input_array = 255 - input_array  # Inverterar färger.
    input_array = input_array.reshape(1, -1)  # Omvandlas till en 1D array
    
    # Gör om datan till Dataframe med samma antal Kolumner som tränings datan.
    input_df = pd.DataFrame(input_array, columns=[f'pixel{i}' for i in range(784)])
        
    prediction = model.predict(input_df)
    return prediction[0]