from fastapi import FastAPI
from typing import Annotated , Literal
from pydantic import BaseModel
import pickle
from pickle import load
import numpy as np
import os


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class UserInput(BaseModel):
    gender: Literal["1", "0"]
    age: int
    height: float
    weight: float
    duration: float
    heart_rate: float
    body_temp: float

model_path = os.path.join(BASE_DIR, "best_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)
    
@app.get("/")
def read_root():
    return {"message": "Calories Burnt Prediction API"}

@app.post("/predict")
def predict(user_input:UserInput):
    input_data = np.array([[
        int(user_input.gender),
        user_input.age,
        user_input.height,
        user_input.weight,
        user_input.duration,
        user_input.heart_rate,
        user_input.body_temp
    ]])
    prediction = model.predict(input_data)[0]
    return {"prediction": float(prediction), "unit":"calories burnt"}