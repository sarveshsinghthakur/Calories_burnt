from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Literal
from pydantic import BaseModel
import pickle
import numpy as np
import os


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "best_model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)


class UserInput(BaseModel):
    gender: Literal["1", "0"]
    age: int
    height: float
    weight: float
    duration: float
    heart_rate: float
    body_temp: float


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calories Burnt Predictor</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px;
            }
            .container {
                background: white; border-radius: 20px; padding: 40px; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.3); max-width: 600px; width: 100%;
            }
            h1 { color: #333; text-align: center; margin-bottom: 10px; }
            .subtitle { text-align: center; color: #666; margin-bottom: 30px; }
            .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: 600; color: #333; }
            select, input { 
                width: 100%; padding: 12px; border: 2px solid #ddd; 
                border-radius: 10px; font-size: 16px; transition: border-color 0.3s;
            }
            select:focus, input:focus { outline: none; border-color: #667eea; }
            button {
                width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; border: none; border-radius: 10px; font-size: 18px; 
                font-weight: bold; cursor: pointer; margin-top: 20px; transition: transform 0.2s;
            }
            button:hover { transform: scale(1.02); }
            #result {
                margin-top: 25px; padding: 20px; border-radius: 10px; text-align: center;
                display: none; font-size: 24px; font-weight: bold;
            }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
            @media (max-width: 500px) { .form-grid { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Calories Burnt Predictor</h1>
            <p class="subtitle">Enter your details to predict calories burned</p>
            <div class="form-grid">
                <div class="form-group">
                    <label>Gender</label>
                    <select id="gender">
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" id="age" min="1" max="100" value="25">
                </div>
                <div class="form-group">
                    <label>Height (cm)</label>
                    <input type="number" id="height" min="50" max="250" value="170" step="0.1">
                </div>
                <div class="form-group">
                    <label>Weight (kg)</label>
                    <input type="number" id="weight" min="20" max="300" value="70" step="0.1">
                </div>
                <div class="form-group">
                    <label>Duration (minutes)</label>
                    <input type="number" id="duration" min="1" max="300" value="30" step="0.1">
                </div>
                <div class="form-group">
                    <label>Heart Rate (bpm)</label>
                    <input type="number" id="heart_rate" min="40" max="220" value="120" step="0.1">
                </div>
                <div class="form-group" style="grid-column: span 2;">
                    <label>Body Temperature (°C)</label>
                    <input type="number" id="body_temp" min="35" max="42" value="37" step="0.1">
                </div>
            </div>
            <button onclick="predict()">Predict Calories</button>
            <div id="result"></div>
        </div>
        <script>
            async function predict() {
                const data = {
                    gender: document.getElementById('gender').value,
                    age: parseInt(document.getElementById('age').value),
                    height: parseFloat(document.getElementById('height').value),
                    weight: parseFloat(document.getElementById('weight').value),
                    duration: parseFloat(document.getElementById('duration').value),
                    heart_rate: parseFloat(document.getElementById('heart_rate').value),
                    body_temp: parseFloat(document.getElementById('body_temp').value)
                };
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'none';
                resultDiv.className = '';
                resultDiv.innerHTML = 'Predicting...';
                resultDiv.style.display = 'block';
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    });
                    const result = await response.json();
                    if (response.ok) {
                        resultDiv.className = 'success';
                        resultDiv.innerHTML = '🔥 Predicted Calories: ' + result.prediction.toFixed(2);
                    } else {
                        resultDiv.className = 'error';
                        resultDiv.innerHTML = 'Error: ' + (result.detail || 'Unknown error');
                    }
                } catch (e) {
                    resultDiv.className = 'error';
                    resultDiv.innerHTML = 'Error: Could not connect to server';
                }
            }
        </script>
    </body>
    </html>
    """


@app.post("/predict")
def predict(user_input: UserInput):
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
    return {"prediction": float(prediction), "unit": "calories"}