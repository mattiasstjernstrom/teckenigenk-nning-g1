import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from PIL import Image, ImageOps
import time


def load_emnist_data():
    df_emnist_train = pd.read_csv("data/emnist-balanced-train.csv")
    df_emnist_test = pd.read_csv("data/emnist-balanced-test.csv")
    return df_emnist_train, df_emnist_test

# Tränar modellen, bästa värde på k == 5.
def train_KNN_EMNIST():
    df_emnist_train, df_emnist_test = load_emnist_data()
    
    X_train = df_emnist_train.drop(columns=['label'])
    y_train = df_emnist_train['label']
    X_test = df_emnist_test.drop(columns=['label'])
    y_test = df_emnist_test['label']
    
    # Normalisera datan
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    start_time = time.time()  # Starta tidtagningen
    clf_EMINST = KNeighborsClassifier(n_neighbors=5)
    clf_EMINST.fit(X_train, y_train)
    y_pred = clf_EMINST.predict(X_test)
    end_time = time.time()  # Stoppa tidtagningen
    training_time = end_time - start_time  # Beräkna tiden för träning

    accuracy = accuracy_score(y_test, y_pred)
    print(f'KNN EMNIST Model Accuracy: {accuracy:.3f}')
    print(f'Training Time: {training_time:.2f} seconds')
    return clf_EMINST



def train_RF():
    df_emnist_train, df_emnist_test = load_emnist_data()

    X_train = df_emnist_train.drop(columns=['label'])
    y_train = df_emnist_train['label']
    X_test = df_emnist_test.drop(columns=['label'])
    y_test = df_emnist_test['label']

    start_time = time.time()  # Starta tidtagningen
    rf = RandomForestClassifier(n_estimators=50) # Satt 50 för att hålla nere träningstid, men 200 gav bäst resultat.(skiljer bara 1.7%)
    rf.fit(X_train, y_train)
    end_time = time.time()  # Stoppa tidtagningen
    training_time = end_time - start_time  # Beräkna tiden för träning
    accuracy = rf.score(X_test, y_test)
    print(f"RF Model Accuracy: {accuracy:.3f}")
    print(f'Training Time: {training_time:.2f} seconds')
    return rf

def train_ANN():
    df_emnist_train, df_emnist_test = load_emnist_data()

    X_train = df_emnist_train.drop(columns=['label']).values / 255.0
    y_train = df_emnist_train['label']
    X_test = df_emnist_test.drop(columns=['label']).values / 255.0
    y_test = df_emnist_test['label']

    X_train_small, _, y_train_small, _ = train_test_split(X_train, y_train, train_size=0.1, random_state=42)

    ann = MLPClassifier(hidden_layer_sizes=(256,128,64), max_iter=600, learning_rate='constant', learning_rate_init=0.01, random_state=42, activation="relu")
    start_time = time.time()  # Starta tidtagningen
    ann.fit(X_train_small, y_train_small)
    end_time = time.time()  # Stoppa tidtagningen
    training_time = end_time - start_time  # Beräkna tiden för träning
    accuracy = ann.score(X_test, y_test)
    
    print(f"ANN Model Accuracy: {accuracy:.3f}")
    print(f'Training Time: {training_time:.2f} seconds')
    return ann


def predict_EMNIST(model, input_image):

    # Format Image
    input_image = input_image.convert("L")  # Konverterar till gråskala
    
    input_image = input_image.rotate(270, expand=True) #Roterar 270 grader
    input_image = ImageOps.mirror(input_image) #spegelvänder

    input_image = input_image.resize((28, 28))  # Skala om till 28x28

    input_array = np.array(input_image) # Bilden konverteras till en np-array
    input_array = 255 - input_array  # Inverterar färger.

    input_flattened = input_array.reshape(1, -1) #gör om X från 28 till 784

    y_pred = model.predict(input_flattened)
    
    label_map = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 
    11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 
    21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 
    31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: 'a', 37: 'b', 38: 'd', 39: 'e', 40: 'f', 
    41: 'g', 42: 'h', 43: 'n', 44: 'q', 45: 'r', 46: 't'
    }
    
    prediction = label_map[y_pred[0]]
    return prediction

