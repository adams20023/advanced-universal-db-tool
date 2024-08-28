# db_tool/ml_models.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

def train_model(file_path, model_type, target_column):
    df = pd.read_csv(file_path)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    if model_type == "linear_regression":
        model = LinearRegression()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    
    model_filename = f"{model_type}_model.pkl"
    joblib.dump(model, model_filename)
    print(f"Model trained and saved as {model_filename}. Mean Squared Error on test data: {mse}")

def predict(model_path, data_path):
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    predictions = model.predict(df)
    print(f"Predictions: {predictions}")

