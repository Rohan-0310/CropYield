import numpy as np
from crop_data import crop_info

def validate_input(input_data):
    """
    Validates the input data for the prediction model
    
    Args:
        input_data (dict): Dictionary containing input features
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if crop type is valid
    if input_data['crop_type'] not in crop_info:
        return False, f"Invalid crop type: {input_data['crop_type']}"
    
    # Check temperature range
    if input_data['temperature'] < 0 or input_data['temperature'] > 40:
        return False, "Temperature must be between 0°C and 40°C"
    
    # Check rainfall range
    if input_data['rainfall'] < 0 or input_data['rainfall'] > 3000:
        return False, "Rainfall must be between 0mm and 3000mm"
    
    # Check humidity range
    if input_data['humidity'] < 0 or input_data['humidity'] > 100:
        return False, "Humidity must be between 0% and 100%"
    
    # Check pH range
    if input_data['ph'] < 0 or input_data['ph'] > 14:
        return False, "pH must be between 0 and 14"
    
    # Check soil type
    valid_soil_types = ["Loamy", "Clay", "Sandy", "Silt", "Black"]
    if input_data['soil_type'] not in valid_soil_types:
        return False, f"Invalid soil type. Must be one of: {', '.join(valid_soil_types)}"
    
    # Check NPK values
    if any(input_data[nutrient] < 0 or input_data[nutrient] > 200 
           for nutrient in ['nitrogen', 'phosphorus', 'potassium']):
        return False, "Nutrient values (N, P, K) must be between 0 and 200 kg/ha"
    
    # Check area
    if input_data['area'] <= 0 or input_data['area'] > 1000:
        return False, "Area must be between 0.1 and 1000 hectares"
    
    return True, ""

def normalize_input(input_data):
    """
    Normalizes and prepares input data for the prediction model
    
    Args:
        input_data (dict): Dictionary containing raw input features
        
    Returns:
        dict: Normalized input features ready for model prediction
    """
    # Create a copy to avoid modifying the original
    normalized = input_data.copy()
    
    # For this simplified model, we just pass through the values
    # In a real application, you might normalize values to specific ranges
    # or apply more complex transformations
    
    return normalized

def generate_sample_input():
    """
    Generates a sample input for testing
    
    Returns:
        dict: Sample input data
    """
    # Get a random crop
    crop_types = list(crop_info.keys())
    crop_type = np.random.choice(crop_types)
    
    # Get optimal conditions for the crop
    crop = crop_info[crop_type]
    
    # Generate values within optimal ranges with some variation
    temp_min, temp_max = crop['temperature_range']
    rain_min, rain_max = crop['rainfall_range']
    hum_min, hum_max = crop['humidity_range']
    ph_min, ph_max = crop['ph_range']
    
    # Add some random variation around optimal values
    temperature = np.random.uniform(temp_min, temp_max)
    rainfall = np.random.uniform(rain_min, rain_max)
    humidity = np.random.uniform(hum_min, hum_max)
    ph = np.random.uniform(ph_min, ph_max)
    
    # Random soil type from suitable types
    soil_type = np.random.choice(crop['suitable_soil_types'])
    
    # Random NPK values
    nitrogen = np.random.uniform(60, 120)
    phosphorus = np.random.uniform(40, 80)
    potassium = np.random.uniform(30, 60)
    
    # Random area
    area = np.random.uniform(1, 50)
    
    # Create the input dictionary
    sample_input = {
        'crop_type': crop_type,
        'temperature': temperature,
        'rainfall': rainfall,
        'humidity': humidity,
        'ph': ph,
        'soil_type': soil_type,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'area': area
    }
    
    return sample_input
