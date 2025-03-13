import pandas as pd
import numpy as np

# Dictionary containing information about different crops
crop_info = {
    'Rice': {
        'scientific_name': 'Oryza sativa',
        'growing_season': 'Wet season',
        'growing_period': '120-150',
        'temperature_range': [20, 35],
        'rainfall_range': [1000, 2000],
        'humidity_range': [60, 90],
        'ph_range': [5.5, 6.5],
        'suitable_soil_types': ['Loamy', 'Clay'],
        'description': """
            Rice is a staple food crop for more than half of the world's population. 
            It is grown in flooded fields called paddies and requires a significant amount of water. 
            Rice is particularly important in Asian countries, where it has been cultivated for thousands of years.
        """,
        'nutritional_value': {
            'Calories': 130,
            'Protein (g)': 2.7,
            'Carbohydrates (g)': 28,
            'Fiber (g)': 0.4,
            'Iron (mg)': 0.2
        },
        'farming_tips': [
            'Maintain 5-10 cm of water in the field during the growing season',
            'Transplant seedlings when they are 20-30 days old',
            'Control weeds early in the growing season',
            'Use integrated pest management to control insects and diseases',
            'Drain the field 10-15 days before harvesting'
        ]
    },
    'Wheat': {
        'scientific_name': 'Triticum aestivum',
        'growing_season': 'Winter/Spring',
        'growing_period': '100-130',
        'temperature_range': [15, 24],
        'rainfall_range': [500, 900],
        'humidity_range': [40, 60],
        'ph_range': [6.0, 7.5],
        'suitable_soil_types': ['Loamy', 'Clay', 'Silt'],
        'description': """
            Wheat is one of the world's most important cereal crops and a staple food used to make flour for bread, pasta, 
            and pastry. There are many varieties of wheat grown around the world, with different types suited to different 
            climates and soil conditions.
        """,
        'nutritional_value': {
            'Calories': 340,
            'Protein (g)': 13.2,
            'Carbohydrates (g)': 72,
            'Fiber (g)': 10.7,
            'Iron (mg)': 3.6
        },
        'farming_tips': [
            'Plant winter wheat in the fall for harvest in early summer',
            'Plant spring wheat in early spring for summer harvest',
            'Ensure proper seed depth of 3-5 cm',
            'Apply nitrogen fertilizer at the appropriate growth stages',
            'Monitor for rust and fungal diseases, especially in humid conditions'
        ]
    },
    'Corn (Maize)': {
        'scientific_name': 'Zea mays',
        'growing_season': 'Summer',
        'growing_period': '90-120',
        'temperature_range': [18, 32],
        'rainfall_range': [600, 1200],
        'humidity_range': [50, 80],
        'ph_range': [5.8, 7.0],
        'suitable_soil_types': ['Loamy', 'Sandy Loam'],
        'description': """
            Corn (maize) is one of the most versatile crops, used for human consumption, livestock feed, and industrial products. 
            It is a tall annual plant with large, narrow leaves and ears that contain the kernels. Corn requires warm temperatures 
            and ample water to thrive.
        """,
        'nutritional_value': {
            'Calories': 365,
            'Protein (g)': 9.4,
            'Carbohydrates (g)': 74,
            'Fiber (g)': 7.3,
            'Iron (mg)': 2.7
        },
        'farming_tips': [
            'Plant when soil temperatures reach at least 10°C (50°F)',
            'Space plants appropriately (15-20 cm in rows, 75-100 cm between rows)',
            'Apply nitrogen fertilizer when plants are knee-high',
            'Ensure consistent moisture, especially during silking and ear development',
            'Control weeds during the first 4-6 weeks after planting'
        ]
    },
    'Potato': {
        'scientific_name': 'Solanum tuberosum',
        'growing_season': 'Spring/Summer',
        'growing_period': '90-120',
        'temperature_range': [15, 25],
        'rainfall_range': [500, 700],
        'humidity_range': [60, 85],
        'ph_range': [5.0, 6.5],
        'suitable_soil_types': ['Loamy', 'Sandy Loam'],
        'description': """
            Potatoes are one of the world's most important food crops, grown for their starchy tubers. 
            They are versatile and can be prepared in many ways. Potatoes are grown from "seed potatoes" 
            which are small tubers or pieces of tubers with at least one "eye" (bud).
        """,
        'nutritional_value': {
            'Calories': 77,
            'Protein (g)': 2.0,
            'Carbohydrates (g)': 17,
            'Fiber (g)': 2.2,
            'Vitamin C (mg)': 19.7
        },
        'farming_tips': [
            'Plant seed potatoes 10-15 cm deep and 30 cm apart',
            'Hill the soil around plants as they grow to protect tubers from light',
            'Maintain even soil moisture to prevent growth cracks',
            'Watch for signs of late blight, especially in humid conditions',
            'Harvest after vines have died back for storage potatoes'
        ]
    },
    'Tomato': {
        'scientific_name': 'Solanum lycopersicum',
        'growing_season': 'Summer',
        'growing_period': '60-100',
        'temperature_range': [20, 30],
        'rainfall_range': [400, 600],
        'humidity_range': [50, 70],
        'ph_range': [6.0, 7.0],
        'suitable_soil_types': ['Loamy', 'Sandy Loam'],
        'description': """
            Tomatoes are a popular warm-season crop grown for their flavorful fruits. 
            They come in many varieties, from small cherry tomatoes to large beefsteak types. 
            Tomatoes can be determinate (bush) or indeterminate (vining) in growth habit.
        """,
        'nutritional_value': {
            'Calories': 18,
            'Protein (g)': 0.9,
            'Carbohydrates (g)': 3.9,
            'Fiber (g)': 1.2,
            'Vitamin C (mg)': 13.7
        },
        'farming_tips': [
            'Plant after all danger of frost has passed',
            'Provide support for indeterminate varieties',
            'Prune suckers for better air circulation',
            'Water at the base of plants to prevent leaf diseases',
            'Harvest when fruits are firm and fully colored'
        ]
    },
    'Cotton': {
        'scientific_name': 'Gossypium hirsutum',
        'growing_season': 'Summer',
        'growing_period': '150-180',
        'temperature_range': [21, 35],
        'rainfall_range': [700, 1300],
        'humidity_range': [40, 70],
        'ph_range': [5.5, 8.0],
        'suitable_soil_types': ['Loamy', 'Sandy', 'Black'],
        'description': """
            Cotton is a soft, fluffy staple fiber that grows in a protective case around the seeds of cotton plants. 
            It is one of the most important textile fibers in the world. Cotton requires a long frost-free period, 
            plenty of sunshine, and moderate rainfall to thrive.
        """,
        'nutritional_value': {
            'Calories': 0,
            'Protein (g)': 0,
            'Carbohydrates (g)': 0,
            'Fiber (g)': 0,
            'Iron (mg)': 0
        },
        'farming_tips': [
            'Plant when soil temperatures are consistently above 15°C (60°F)',
            'Control early season weeds to reduce competition',
            'Monitor for bollworms and other pests regularly',
            'Defoliate before harvest to reduce leaf trash',
            'Harvest when bolls are fully open but before weathering affects quality'
        ]
    },
    'Sugarcane': {
        'scientific_name': 'Saccharum officinarum',
        'growing_season': 'Year-round in tropical areas',
        'growing_period': '270-365',
        'temperature_range': [24, 38],
        'rainfall_range': [1100, 1500],
        'humidity_range': [60, 80],
        'ph_range': [6.0, 7.5],
        'suitable_soil_types': ['Loamy', 'Clay', 'Black'],
        'description': """
            Sugarcane is a tall perennial grass grown for its sweet sap, which is processed into sugar. 
            It is one of the most efficient photosynthesizers in the plant kingdom and can grow up to 4-5 
            meters tall. Sugarcane is primarily grown in tropical and subtropical regions.
        """,
        'nutritional_value': {
            'Calories': 50,
            'Protein (g)': 0,
            'Carbohydrates (g)': 13,
            'Fiber (g)': 0.2,
            'Iron (mg)': 0.1
        },
        'farming_tips': [
            'Plant stem cuttings with 2-3 buds',
            'Maintain adequate soil moisture during establishment',
            'Apply potassium fertilizer for better sugar content',
            'Control weeds during the first 3-4 months',
            'Harvest when the crop is mature (usually 10-12 months after planting)'
        ]
    },
    'Coffee': {
        'scientific_name': 'Coffea arabica',
        'growing_season': 'Year-round in tropical areas',
        'growing_period': '3-4 years to first harvest',
        'temperature_range': [15, 24],
        'rainfall_range': [1500, 2500],
        'humidity_range': [60, 80],
        'ph_range': [5.5, 6.5],
        'suitable_soil_types': ['Loamy', 'Sandy Loam'],
        'description': """
            Coffee is a brewed drink prepared from roasted coffee beans, the seeds of berries from the Coffea plant. 
            Coffee plants are cultivated in over 70 countries, primarily in equatorial regions of the Americas, 
            Southeast Asia, the Indian subcontinent, and Africa.
        """,
        'nutritional_value': {
            'Calories': 2,
            'Protein (g)': 0.3,
            'Carbohydrates (g)': 0,
            'Fiber (g)': 0,
            'Potassium (mg)': 116
        },
        'farming_tips': [
            'Grow under 35-45% shade for best quality',
            'Plant at elevations between 600-1200 meters for Arabica varieties',
            'Prune to maintain productive height and remove old branches',
            'Harvest only ripe, red cherries for best quality',
            'Process cherries within 24 hours of harvest'
        ]
    },
    'Soybean': {
        'scientific_name': 'Glycine max',
        'growing_season': 'Summer',
        'growing_period': '80-120',
        'temperature_range': [18, 30],
        'rainfall_range': [450, 700],
        'humidity_range': [50, 75],
        'ph_range': [6.0, 7.0],
        'suitable_soil_types': ['Loamy', 'Clay Loam'],
        'description': """
            Soybeans are a legume species native to East Asia, widely grown for its edible bean which has numerous uses. 
            The plant is a valuable crop that provides vegetable protein for millions of people and is a major ingredient 
            in many food products.
        """,
        'nutritional_value': {
            'Calories': 446,
            'Protein (g)': 36.5,
            'Carbohydrates (g)': 30.2,
            'Fiber (g)': 9.3,
            'Iron (mg)': 15.7
        },
        'farming_tips': [
            'Plant when soil temperatures reach 12-14°C (54-57°F)',
            'Inoculate seeds with Rhizobium bacteria for nitrogen fixation',
            'Control weeds early as soybeans are sensitive to competition',
            'Scout regularly for pests, especially spider mites in dry conditions',
            'Harvest when pods are brown and seeds rattle inside'
        ]
    },
    'Orange': {
        'scientific_name': 'Citrus sinensis',
        'growing_season': 'Year-round in tropical areas',
        'growing_period': '3-5 years to first harvest',
        'temperature_range': [15, 35],
        'rainfall_range': [850, 1200],
        'humidity_range': [50, 80],
        'ph_range': [5.5, 7.0],
        'suitable_soil_types': ['Loamy', 'Sandy Loam'],
        'description': """
            Oranges are round citrus fruits with a sweet-tart flavor and juicy pulp. They are grown on flowering trees and 
            are an excellent source of vitamin C. Orange trees are evergreen and can produce fruit for many years when 
            properly maintained.
        """,
        'nutritional_value': {
            'Calories': 47,
            'Protein (g)': 0.9,
            'Carbohydrates (g)': 11.8,
            'Fiber (g)': 2.4,
            'Vitamin C (mg)': 53.2
        },
        'farming_tips': [
            'Plant trees with proper spacing (4-6 meters between trees)',
            'Provide wind protection for young trees',
            'Prune to maintain airflow and tree health',
            'Monitor for citrus greening disease and control psyllids',
            'Harvest when fruits are firm, heavy, and have developed full color'
        ]
    }
}

def generate_training_data():
    """
    Generates synthetic training data for the ML model based on crop information
    
    Returns:
        pandas.DataFrame: DataFrame containing synthetic training data
    """
    # Initialize empty lists to store data
    data_rows = []
    
    # For each crop, generate multiple data points with variations
    for crop_name, info in crop_info.items():
        # Get the optimal ranges
        temp_min, temp_max = info['temperature_range']
        rain_min, rain_max = info['rainfall_range']
        hum_min, hum_max = info['humidity_range']
        ph_min, ph_max = info['ph_range']
        soil_types = info['suitable_soil_types']
        
        # Determine yield range based on optimal conditions
        # This is a simplified model - in real life, yield would depend on many more factors
        base_yield_min = 3.0  # tons per hectare
        base_yield_max = 8.0  # tons per hectare
        
        # Adjust base yield by crop type (some crops naturally yield more/less)
        if crop_name in ['Rice', 'Wheat', 'Corn (Maize)']:
            base_yield_min *= 1.2
            base_yield_max *= 1.3
        elif crop_name in ['Potato', 'Sugarcane']:
            base_yield_min *= 2.0
            base_yield_max *= 2.5
        elif crop_name in ['Cotton', 'Coffee']:
            base_yield_min *= 0.5
            base_yield_max *= 0.7
        
        # Generate 50-100 samples per crop with variations
        num_samples = np.random.randint(50, 101)
        
        for _ in range(num_samples):
            # Generate random values within and slightly outside optimal ranges
            expand_range = np.random.choice([True, False], p=[0.3, 0.7])
            
            if expand_range:
                # Generate some values outside optimal range
                temperature = np.random.uniform(temp_min - 5, temp_max + 5)
                rainfall = np.random.uniform(rain_min - 200, rain_max + 200)
                humidity = np.random.uniform(max(0, hum_min - 15), min(100, hum_max + 15))
                ph = np.random.uniform(max(0, ph_min - 1), min(14, ph_max + 1))
            else:
                # Generate values within optimal range
                temperature = np.random.uniform(temp_min, temp_max)
                rainfall = np.random.uniform(rain_min, rain_max)
                humidity = np.random.uniform(hum_min, hum_max)
                ph = np.random.uniform(ph_min, ph_max)
            
            # Sometimes use non-optimal soil
            if np.random.random() < 0.2:
                all_soil_types = ["Loamy", "Clay", "Sandy", "Silt", "Black"]
                non_optimal_soils = [s for s in all_soil_types if s not in soil_types]
                if non_optimal_soils:
                    soil_type = np.random.choice(non_optimal_soils)
                else:
                    soil_type = np.random.choice(soil_types)
            else:
                soil_type = np.random.choice(soil_types)
            
            # Random NPK values
            nitrogen = np.random.uniform(30, 150)
            phosphorus = np.random.uniform(20, 100)
            potassium = np.random.uniform(20, 100)
            
            # Calculate yield based on how close to optimal conditions
            # This is a simplified model for demonstration
            
            # Calculate distance from optimal for each parameter
            temp_optimal = (temp_min + temp_max) / 2
            rain_optimal = (rain_min + rain_max) / 2
            hum_optimal = (hum_min + hum_max) / 2
            ph_optimal = (ph_min + ph_max) / 2
            
            temp_dist = abs(temperature - temp_optimal) / (temp_max - temp_min) if (temp_max - temp_min) > 0 else 0
            rain_dist = abs(rainfall - rain_optimal) / (rain_max - rain_min) if (rain_max - rain_min) > 0 else 0
            hum_dist = abs(humidity - hum_optimal) / (hum_max - hum_min) if (hum_max - hum_min) > 0 else 0
            ph_dist = abs(ph - ph_optimal) / (ph_max - ph_min) if (ph_max - ph_min) > 0 else 0
            
            # Soil type impact
            soil_optimal = 1.0 if soil_type in soil_types else 0.7
            
            # NPK impact (simplified)
            npk_optimal = (nitrogen / 100 + phosphorus / 80 + potassium / 80) / 3
            npk_optimal = min(max(npk_optimal, 0.5), 1.2)  # Limit impact
            
            # Calculate overall optimality (0-1 scale)
            optimality = 1.0 - (temp_dist * 0.2 + rain_dist * 0.25 + hum_dist * 0.15 + ph_dist * 0.15)
            optimality = optimality * soil_optimal * npk_optimal
            
            # Calculate yield with some randomness
            yield_range = base_yield_max - base_yield_min
            yield_value = base_yield_min + (yield_range * optimality)
            
            # Add some random noise
            yield_value *= np.random.uniform(0.85, 1.15)
            
            # Create data row
            data_row = {
                'crop_type': crop_name,
                'temperature': temperature,
                'rainfall': rainfall,
                'humidity': humidity,
                'ph': ph,
                'soil_type': soil_type,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'yield': yield_value
            }
            
            data_rows.append(data_row)
    
    # Convert to DataFrame
    df = pd.DataFrame(data_rows)
    
    return df

def get_crop_factors(crop_name):
    """
    Returns a DataFrame with importance factors for different parameters for a specific crop
    
    Args:
        crop_name (str): Name of the crop
        
    Returns:
        pandas.DataFrame: DataFrame with factor information
    """
    # Get crop information
    info = crop_info[crop_name]
    
    # Create factors based on crop info
    factors_data = {
        'factor': [
            'Temperature', 
            'Rainfall', 
            'Soil pH', 
            'Humidity', 
            'Nitrogen', 
            'Phosphorus', 
            'Potassium'
        ],
        'importance': [
            0.85,  # Temperature
            0.90,  # Rainfall
            0.75,  # Soil pH
            0.60,  # Humidity
            0.70,  # Nitrogen
            0.65,  # Phosphorus
            0.60   # Potassium
        ],
        'optimal_temperature': [info['temperature_range'][0] + (info['temperature_range'][1] - info['temperature_range'][0])/2] * 7,
        'optimal_rainfall': [info['rainfall_range'][0] + (info['rainfall_range'][1] - info['rainfall_range'][0])/2] * 7,
        'optimal_humidity': [info['humidity_range'][0] + (info['humidity_range'][1] - info['humidity_range'][0])/2] * 7,
        'optimal_ph': [info['ph_range'][0] + (info['ph_range'][1] - info['ph_range'][0])/2] * 7,
        'optimal_nitrogen': [90] * 7,  # Assuming optimal nitrogen is around 90 kg/ha
        'optimal_phosphorus': [60] * 7,  # Assuming optimal phosphorus is around 60 kg/ha
        'optimal_potassium': [40] * 7,  # Assuming optimal potassium is around 40 kg/ha
        'max_yield': [12] * 7  # Maximum theoretical yield in tons/ha
    }
    
    # Adjust importance based on crop type
    if crop_name == 'Rice':
        factors_data['importance'][1] = 0.95  # Rainfall more important
        factors_data['max_yield'] = [9] * 7
    elif crop_name == 'Wheat':
        factors_data['importance'][0] = 0.80  # Temperature importance
        factors_data['max_yield'] = [8] * 7
    elif crop_name == 'Corn (Maize)':
        factors_data['importance'][4] = 0.85  # Nitrogen more important
        factors_data['max_yield'] = [12] * 7
    elif crop_name == 'Potato':
        factors_data['importance'][3] = 0.75  # Humidity more important
        factors_data['max_yield'] = [25] * 7  # Higher yield potential
    elif crop_name == 'Sugarcane':
        factors_data['importance'][1] = 0.95  # Rainfall more important
        factors_data['max_yield'] = [80] * 7  # Very high yield potential
    elif crop_name == 'Cotton':
        factors_data['importance'][0] = 0.90  # Temperature more important
        factors_data['max_yield'] = [3] * 7  # Lower yield
    
    # Add some random variation to make the chart more interesting
    factors_data['importance'] = [i * np.random.uniform(0.9, 1.1) for i in factors_data['importance']]
    
    # Normalize importance to 0-1 scale
    max_importance = max(factors_data['importance'])
    factors_data['importance'] = [i / max_importance for i in factors_data['importance']]
    
    return pd.DataFrame(factors_data)
