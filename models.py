import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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