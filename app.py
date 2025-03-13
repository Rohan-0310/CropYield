import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from crop_model import train_model, predict_crop_yield
from data_utils import validate_input, normalize_input
from crop_data import crop_info, get_crop_factors

# Set page configuration
st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌱",
    layout="wide"
)

# Application title and description
st.title("Crop Yield Prediction")
st.markdown("""
    This application predicts the potential yield of various crops based on environmental 
    and agricultural factors using machine learning. Enter the details below to get a prediction.
""")

# Sidebar with information
with st.sidebar:
    st.header("About This App")
    st.info("""
        This application uses machine learning models to predict 
        crop yields based on various environmental and soil factors.
        
        The model has been trained on historical crop production data 
        and takes into account multiple parameters that affect crop growth.
    """)
    
    st.header("How to Use")
    st.markdown("""
        1. Select the crop you're interested in
        2. Enter the environmental parameters
        3. Click 'Predict Yield' to get results
        4. View the prediction and visualizations
    """)

# Main content
tab1, tab2 = st.tabs(["Prediction", "Crop Information"])

with tab1:
    # Form for user input
    with st.form("prediction_form"):
        st.subheader("Enter Crop and Environmental Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Crop selection
            crop_type = st.selectbox(
                "Select Crop Type",
                options=list(crop_info.keys())
            )
            
            # Temperature inputs
            temperature = st.slider(
                "Average Temperature (°C)",
                min_value=0.0,
                max_value=40.0,
                value=25.0,
                step=0.5,
                help="Average temperature during the growing season"
            )
            
            rainfall = st.slider(
                "Annual Rainfall (mm)",
                min_value=0,
                max_value=3000,
                value=1000,
                step=50,
                help="Total annual rainfall in millimeters"
            )
            
            humidity = st.slider(
                "Humidity (%)",
                min_value=0,
                max_value=100,
                value=60,
                step=1,
                help="Average humidity percentage"
            )
        
        with col2:
            # Soil related inputs
            ph = st.slider(
                "Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=6.5,
                step=0.1,
                help="pH level of the soil"
            )
            
            soil_type = st.selectbox(
                "Soil Type",
                options=["Loamy", "Clay", "Sandy", "Silt", "Black"]
            )
            
            nitrogen = st.slider(
                "Nitrogen Content (kg/ha)",
                min_value=0,
                max_value=200,
                value=80,
                step=5,
                help="Nitrogen content in soil"
            )
            
            phosphorus = st.slider(
                "Phosphorus Content (kg/ha)",
                min_value=0,
                max_value=200,
                value=50,
                step=5,
                help="Phosphorus content in soil"
            )
            
            potassium = st.slider(
                "Potassium Content (kg/ha)",
                min_value=0,
                max_value=200,
                value=40,
                step=5,
                help="Potassium content in soil"
            )
        
        # Area input
        area = st.number_input(
            "Area (hectares)",
            min_value=0.1,
            max_value=1000.0,
            value=10.0,
            step=0.1,
            help="Area of land for cultivation in hectares"
        )
        
        st.markdown("---")
        submitted = st.form_submit_button("Predict Yield")
    
    # Process prediction when form is submitted
    if submitted:
        # Check if inputs are valid
        input_data = {
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
        
        is_valid, error_msg = validate_input(input_data)
        
        if is_valid:
            with st.spinner("Computing prediction..."):
                # Normalize inputs for the model
                normalized_input = normalize_input(input_data)
                
                # Get prediction
                predicted_yield, confidence = predict_crop_yield(normalized_input)
                total_yield = predicted_yield * area  # Total yield based on area
                
                # Display prediction results
                st.success("Prediction completed!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Predicted Yield (ton/ha)", 
                        f"{predicted_yield:.2f}"
                    )
                
                with col2:
                    st.metric(
                        "Total Expected Yield (tons)", 
                        f"{total_yield:.2f}"
                    )
                
                with col3:
                    st.metric(
                        "Prediction Confidence", 
                        f"{confidence:.1f}%"
                    )
                
                # Visualization section
                st.subheader("Yield Visualization")
                
                # Create a dataframe for factors affecting the yield
                factors = get_crop_factors(crop_type)
                
                # Factor importance bar chart
                fig1 = px.bar(
                    factors,
                    x='importance',
                    y='factor',
                    orientation='h',
                    title=f'Factors Affecting {crop_type} Yield',
                    labels={'importance': 'Importance Score', 'factor': 'Factor'},
                    color='importance',
                    color_continuous_scale='Viridis'
                )
                
                st.plotly_chart(fig1, use_container_width=True)
                
                # Yield prediction gauge
                fig2 = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=predicted_yield,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Predicted Yield (ton/ha)"},
                    gauge={
                        'axis': {'range': [None, factors['max_yield'].iloc[0] * 1.2]},
                        'steps': [
                            {'range': [0, factors['max_yield'].iloc[0] * 0.4], 'color': "lightgray"},
                            {'range': [factors['max_yield'].iloc[0] * 0.4, factors['max_yield'].iloc[0] * 0.8], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': factors['max_yield'].iloc[0]
                        }
                    }
                ))
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Optimized conditions for the crop
                st.subheader(f"Optimized Growing Conditions for {crop_type}")
                
                # Create a comparison dataframe
                comparison_data = {
                    'Factor': ['Temperature (°C)', 'Rainfall (mm)', 'Humidity (%)', 'pH', 'Nitrogen (kg/ha)', 'Phosphorus (kg/ha)', 'Potassium (kg/ha)'],
                    'Your Values': [temperature, rainfall, humidity, ph, nitrogen, phosphorus, potassium],
                    'Optimal Values': [
                        factors['optimal_temperature'].iloc[0],
                        factors['optimal_rainfall'].iloc[0],
                        factors['optimal_humidity'].iloc[0],
                        factors['optimal_ph'].iloc[0],
                        factors['optimal_nitrogen'].iloc[0],
                        factors['optimal_phosphorus'].iloc[0],
                        factors['optimal_potassium'].iloc[0]
                    ]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                
                # Radar chart for comparison
                fig3 = go.Figure()
                
                # Normalize values for radar chart
                factors_max = [40, 3000, 100, 14, 200, 200, 200]
                
                normalized_user = [val/max_val for val, max_val in zip(comparison_data['Your Values'], factors_max)]
                normalized_optimal = [val/max_val for val, max_val in zip(comparison_data['Optimal Values'], factors_max)]
                
                fig3.add_trace(go.Scatterpolar(
                    r=normalized_user,
                    theta=comparison_data['Factor'],
                    fill='toself',
                    name='Your Values'
                ))
                
                fig3.add_trace(go.Scatterpolar(
                    r=normalized_optimal,
                    theta=comparison_data['Factor'],
                    fill='toself',
                    name='Optimal Values'
                ))
                
                fig3.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )),
                    showlegend=True,
                    title="Current vs. Optimal Conditions"
                )
                
                st.plotly_chart(fig3, use_container_width=True)
                
                # Display the comparison table
                st.subheader("Current vs. Optimal Conditions")
                st.dataframe(comparison_df, use_container_width=True)
                
                # Recommendations
                st.subheader("Recommendations")
                
                recommendations = []
                
                # Temperature recommendations
                if abs(temperature - factors['optimal_temperature'].iloc[0]) > 5:
                    if temperature < factors['optimal_temperature'].iloc[0]:
                        recommendations.append(f"The current temperature is lower than optimal. Consider greenhouse cultivation or season adjustment.")
                    else:
                        recommendations.append(f"The current temperature is higher than optimal. Consider shade structures or irrigation cooling systems.")
                
                # Rainfall recommendations
                if abs(rainfall - factors['optimal_rainfall'].iloc[0]) > 300:
                    if rainfall < factors['optimal_rainfall'].iloc[0]:
                        recommendations.append(f"The current rainfall is lower than optimal. Consider irrigation systems or drought-resistant varieties.")
                    else:
                        recommendations.append(f"The current rainfall is higher than optimal. Consider improved drainage or raised beds.")
                
                # pH recommendations
                if abs(ph - factors['optimal_ph'].iloc[0]) > 1:
                    if ph < factors['optimal_ph'].iloc[0]:
                        recommendations.append(f"The soil pH is lower than optimal. Consider adding lime to increase pH.")
                    else:
                        recommendations.append(f"The soil pH is higher than optimal. Consider adding sulfur or organic matter to decrease pH.")
                
                # NPK recommendations
                if nitrogen < factors['optimal_nitrogen'].iloc[0] * 0.8:
                    recommendations.append(f"Nitrogen levels are below optimal. Consider nitrogen fertilizers or legume cover crops.")
                
                if phosphorus < factors['optimal_phosphorus'].iloc[0] * 0.8:
                    recommendations.append(f"Phosphorus levels are below optimal. Consider phosphate fertilizers or bone meal supplements.")
                
                if potassium < factors['optimal_potassium'].iloc[0] * 0.8:
                    recommendations.append(f"Potassium levels are below optimal. Consider potassium fertilizers or wood ash supplements.")
                
                # Display recommendations
                if recommendations:
                    for rec in recommendations:
                        st.info(rec)
                else:
                    st.success("Your current conditions are close to optimal for this crop. No major adjustments needed.")
                
        else:
            st.error(f"Invalid input: {error_msg}")

with tab2:
    st.subheader("Crop Information Database")
    
    # Create two columns
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Select crop to display information
        selected_crop = st.selectbox(
            "Select a crop to learn more",
            options=list(crop_info.keys()),
            key="info_crop_select"
        )
    
    with col2:
        # Display crop information
        st.subheader(selected_crop)
        
        # Get the crop information
        info = crop_info[selected_crop]
        
        # Display basic information
        st.markdown(f"**Scientific Name:** {info['scientific_name']}")
        st.markdown(f"**Growing Season:** {info['growing_season']}")
        st.markdown(f"**Average Growing Period:** {info['growing_period']} days")
        
        # Display the description
        st.markdown("### Description")
        st.markdown(info['description'])
        
        # Display optimal conditions
        st.markdown("### Optimal Growing Conditions")
        
        # Create a dataframe for optimal conditions
        conditions_data = {
            'Condition': ['Temperature (°C)', 'Rainfall (mm)', 'Humidity (%)', 'Soil pH', 'Soil Type'],
            'Optimal Range': [
                f"{info['temperature_range'][0]} - {info['temperature_range'][1]}",
                f"{info['rainfall_range'][0]} - {info['rainfall_range'][1]}",
                f"{info['humidity_range'][0]} - {info['humidity_range'][1]}",
                f"{info['ph_range'][0]} - {info['ph_range'][1]}",
                ", ".join(info['suitable_soil_types'])
            ]
        }
        
        conditions_df = pd.DataFrame(conditions_data)
        st.dataframe(conditions_df, use_container_width=True)
        
        # Display nutritional content
        st.markdown("### Nutritional Value (per 100g)")
        
        # Create a dataframe for nutritional value
        nutrition_data = {
            'Nutrient': list(info['nutritional_value'].keys()),
            'Amount': list(info['nutritional_value'].values())
        }
        
        nutrition_df = pd.DataFrame(nutrition_data)
        
        # Create bar chart for nutritional value
        fig = px.bar(
            nutrition_df,
            x='Nutrient',
            y='Amount',
            title=f'Nutritional Content of {selected_crop} (per 100g)',
            color='Amount',
            color_continuous_scale='Viridis'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display farming tips
        st.markdown("### Farming Tips")
        for tip in info['farming_tips']:
            st.markdown(f"- {tip}")

# Footer
st.markdown("---")
st.markdown("""
    **Disclaimer:** Predictions are based on historical data and machine learning models. 
    Actual yields may vary due to numerous factors including weather variations, pests, diseases, 
    and farming practices. This tool should be used for guidance purposes only.
""")
