import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "model.pkl")
model = None

def load_model():
    global model
    model = joblib.load(MODEL_PATH)
    return model

def get_model():
    global model
    if model is None:
        return load_model()
    return model 