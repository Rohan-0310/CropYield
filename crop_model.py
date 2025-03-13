import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from crop_data import generate_training_data

# Initialize the model once at module level
model = None
preprocessor = None
RANDOM_STATE = 42

def train_model():
    """
    Trains a machine learning model for crop yield prediction
    """
    global model, preprocessor
    
    # Generate training data
    data = generate_training_data()
    
    # Split features and target
    X = data.drop(columns=['yield'])
    y = data['yield']
    
    # Identify categorical and numerical columns
    categorical_features = ['crop_type', 'soil_type']
    numerical_features = ['temperature', 'rainfall', 'humidity', 'ph', 'nitrogen', 'phosphorus', 'potassium']
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Create and train model pipeline
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE))
    ])
    
    # Train the model
    model.fit(X, y)
    
    return model

def predict_crop_yield(input_data):
    """
    Makes a yield prediction based on input data
    
    Args:
        input_data (dict): Dictionary containing input features
        
    Returns:
        tuple: (predicted_yield, confidence_level)
    """
    global model
    
    # Initialize model if it doesn't exist
    if model is None:
        model = train_model()
    
    # Convert input_data to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Make prediction
    prediction = model.predict(input_df)[0]
    
    # Calculate confidence (mock implementation based on prediction variability)
    # For a real application, you might use prediction intervals or model's confidence scores
    confidence = calculate_confidence(input_data, prediction)
    
    return prediction, confidence

def calculate_confidence(input_data, prediction):
    """
    Calculate a confidence level for the prediction based on input proximity to training data
    
    Args:
        input_data (dict): Dictionary containing input features
        prediction (float): The predicted yield value
        
    Returns:
        float: Confidence level (0-100)
    """
    # This is a simplified mock implementation
    # In a real scenario, you would use prediction intervals, model variance, or distance to training data
    
    # Generate a base confidence
    base_confidence = 85.0
    
    # Adjust confidence based on extreme values
    temperature = input_data['temperature']
    rainfall = input_data['rainfall']
    ph = input_data['ph']
    
    # Penalize confidence for extreme temperatures
    if temperature < 5 or temperature > 35:
        base_confidence -= 10
    
    # Penalize confidence for extreme rainfall
    if rainfall < 200 or rainfall > 2500:
        base_confidence -= 8
    
    # Penalize confidence for extreme pH
    if ph < 4 or ph > 9:
        base_confidence -= 12
    
    # Add a small random variation - using only numeric values for seed
    # Filter out non-numeric values to avoid the type error
    numeric_values = [v for v in input_data.values() if isinstance(v, (int, float))]
    seed_value = int(sum(numeric_values) * 100) % 10000
    np.random.seed(seed_value)
    random_adjustment = np.random.uniform(-5, 5)
    
    # Ensure confidence stays within reasonable bounds
    confidence = max(min(base_confidence + random_adjustment, 98), 50)
    
    return confidence
