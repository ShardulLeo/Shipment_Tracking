import joblib
import pandas as pd

def predict_cancellation(data):
    model = joblib.load('models/cancellation_model.pkl')
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return int(prediction[0])