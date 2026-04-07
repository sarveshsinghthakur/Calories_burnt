# Calories Burnt Prediction App

This is a Streamlit web application that predicts the number of calories burnt during exercise based on various input parameters.

## Features
- Interactive input form for user details (Gender, Age, Height, Weight, Duration, Heart Rate, Body Temperature).
- Real-time prediction of calories burnt.
- Simple and intuitive user interface.

## Setup and Installation

1.  **Navigate to the project directory:**

    ```bash
    cd "c:\Users\Dell\OneDrive\Desktop\Projects\AI & ML\Machine Learning\Calories_burnt"
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

    The application will open in your default web browser at `http://localhost:8501`.

## Model Information

The prediction model (`best_model.pkl`) is a pre-trained machine learning model that takes the following features as input:
-   `Gender` (encoded: 0 for Female, 1 for Male)
-   `Age`
-   `Height`
-   `Weight`
-   `Duration`
-   `Heart_Rate`
-   `Body_Temp`

The model outputs the predicted `Calories` burnt.