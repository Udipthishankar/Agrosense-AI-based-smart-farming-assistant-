from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import pickle
import numpy as np
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RECORDS_FILE = os.path.join(DATA_DIR, 'records.json')
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Initialize records file if it doesn't exist
if not os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, 'w') as f:
        json.dump([], f)

# Load crop recommendation model
def load_crop_model():
    """Load pre-trained crop recommendation model"""
    model_path = os.path.join(MODEL_DIR, 'crop_model.pkl')
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    return None

# Crop data for recommendations
CROP_DATA = {
    'rice': {'temp': (20, 30), 'humidity': (50, 90), 'ph': (5.0, 7.5), 'rainfall': (100, 300), 'N': (40, 120), 'P': (20, 60), 'K': (20, 60)},
    'wheat': {'temp': (15, 25), 'humidity': (30, 60), 'ph': (6.0, 8.0), 'rainfall': (40, 100), 'N': (40, 120), 'P': (20, 60), 'K': (20, 60)},
    'cotton': {'temp': (20, 35), 'humidity': (40, 80), 'ph': (5.5, 8.5), 'rainfall': (50, 200), 'N': (60, 150), 'P': (15, 60), 'K': (40, 100)},
    'maize': {'temp': (18, 27), 'humidity': (40, 80), 'ph': (6.0, 7.5), 'rainfall': (60, 100), 'N': (60, 150), 'P': (20, 60), 'K': (20, 60)},
    'sugarcane': {'temp': (20, 30), 'humidity': (60, 100), 'ph': (6.0, 8.5), 'rainfall': (100, 250), 'N': (100, 200), 'P': (40, 80), 'K': (60, 120)},
    'groundnut': {'temp': (22, 32), 'humidity': (40, 70), 'ph': (5.5, 8.0), 'rainfall': (50, 100), 'N': (20, 60), 'P': (15, 40), 'K': (20, 60)},
    'soybean': {'temp': (18, 28), 'humidity': (50, 80), 'ph': (5.5, 7.5), 'rainfall': (40, 80), 'N': (20, 60), 'P': (15, 40), 'K': (15, 50)},
    'ragi': {'temp': (15, 28), 'humidity': (50, 90), 'ph': (6.0, 8.0), 'rainfall': (50, 120), 'N': (40, 100), 'P': (15, 40), 'K': (20, 60)},
    'tomato': {'temp': (20, 30), 'humidity': (50, 85), 'ph': (6.0, 6.8), 'rainfall': (100, 150), 'N': (150, 200), 'P': (50, 80), 'K': (100, 150)},
    'onion': {'temp': (12, 24), 'humidity': (40, 70), 'ph': (6.0, 7.0), 'rainfall': (60, 100), 'N': (100, 150), 'P': (50, 75), 'K': (80, 120)},
}

# Disease detection data
DISEASE_DATA = {
    'leaf_rust': {
        'description': 'Brown/orange pustules on leaves',
        'treatment': 'Apply fungicide spray (Propiconazole or Tebuconazole). Improve air circulation. Remove infected leaves.',
        'severity': 'Medium'
    },
    'powdery_mildew': {
        'description': 'White powder coating on leaves',
        'treatment': 'Spray sulfur powder or neem oil. Ensure proper spacing between plants. Reduce humidity.',
        'severity': 'Low to Medium'
    },
    'late_blight': {
        'description': 'Dark water-soaked lesions on leaves and stems',
        'treatment': 'Apply copper fungicide. Remove infected parts. Practice crop rotation. Ensure good drainage.',
        'severity': 'High'
    },
    'early_blight': {
        'description': 'Concentric brown rings on leaves with yellow halo',
        'treatment': 'Remove affected leaves. Apply chlorothalonil spray. Space plants properly for air circulation.',
        'severity': 'Medium'
    },
    'bacterial_wilt': {
        'description': 'Wilting and browning of vascular tissues',
        'treatment': 'No chemical cure. Remove and destroy infected plants. Control insect vectors. Use resistant varieties.',
        'severity': 'High'
    },
    'fungal_spot': {
        'description': 'Small dark spots with yellow halos on leaves',
        'treatment': 'Apply copper-based fungicide. Avoid overhead watering. Remove fallen leaves. Practice crop rotation.',
        'severity': 'Medium'
    },
    'healthy': {
        'description': 'Plant appears healthy with no visible diseases',
        'treatment': 'Continue regular maintenance. Monitor for any changes. Maintain good irrigation and nutrition.',
        'severity': 'None'
    }
}

# Weather advisory rules
WEATHER_ADVISORY = {
    'irrigation': 'Schedule irrigation based on rainfall. If rainfall > 50mm expected, postpone irrigation.',
    'planting': 'Optimal planting window: Temperature 20-28°C, Humidity 50-70%, No heavy rain.',
    'spraying': 'Best time for pesticide application: Temperature 15-25°C, Humidity 40-80%, No rain for 24 hours.',
    'harvesting': 'Ideal harvesting conditions: Temperature 15-22°C, Humidity 40-60%, Dry weather.',
}

# ==================== CROP RECOMMENDATION API ====================
@app.route('/api/crop/recommend', methods=['POST'])
def recommend_crop():
    """
    Recommend crops based on soil nutrients and climate
    Expected JSON:
    {
        "nitrogen": int,
        "phosphorus": int,
        "potassium": int,
        "temperature": float,
        "humidity": float,
        "ph": float,
        "rainfall": float
    }
    """
    try:
        data = request.json
        
        # Validate input
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        N = float(data['nitrogen'])
        P = float(data['phosphorus'])
        K = float(data['potassium'])
        temp = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])
        
        # Calculate scores for each crop
        scores = {}
        for crop, requirements in CROP_DATA.items():
            score = 0
            
            # Temperature score (25 points max)
            if requirements['temp'][0] <= temp <= requirements['temp'][1]:
                score += 25
            else:
                score += max(0, 25 - abs(temp - np.mean(requirements['temp'])) * 2)
            
            # Humidity score (20 points max)
            if requirements['humidity'][0] <= humidity <= requirements['humidity'][1]:
                score += 20
            else:
                score += max(0, 20 - abs(humidity - np.mean(requirements['humidity'])) * 0.5)
            
            # pH score (15 points max)
            if requirements['ph'][0] <= ph <= requirements['ph'][1]:
                score += 15
            else:
                score += max(0, 15 - abs(ph - np.mean(requirements['ph'])) * 5)
            
            # Rainfall score (15 points max)
            if requirements['rainfall'][0] <= rainfall <= requirements['rainfall'][1]:
                score += 15
            else:
                score += max(0, 15 - abs(rainfall - np.mean(requirements['rainfall'])) * 0.2)
            
            # Nitrogen score (10 points max)
            if requirements['N'][0] <= N <= requirements['N'][1]:
                score += 10
            else:
                score += max(0, 10 - abs(N - np.mean(requirements['N'])) * 0.1)
            
            # Phosphorus score (7.5 points max)
            if requirements['P'][0] <= P <= requirements['P'][1]:
                score += 7.5
            else:
                score += max(0, 7.5 - abs(P - np.mean(requirements['P'])) * 0.2)
            
            # Potassium score (7.5 points max)
            if requirements['K'][0] <= K <= requirements['K'][1]:
                score += 7.5
            else:
                score += max(0, 7.5 - abs(K - np.mean(requirements['K'])) * 0.2)
            
            scores[crop] = round(score, 2)
        
        # Sort by score
        sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_crop = sorted_crops[0][0]
        top_score = sorted_crops[0][1]
        
        return jsonify({
            'recommended_crop': top_crop.capitalize(),
            'confidence_score': top_score,
            'all_recommendations': [
                {'crop': crop.capitalize(), 'score': score} 
                for crop, score in sorted_crops[:5]
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== DISEASE DETECTION API ====================
@app.route('/api/disease/detect', methods=['POST'])
def detect_disease():
    """
    Detect disease from leaf image
    Expects multipart form with 'image' file
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # In a production system, you would use a trained ML model here
        # For now, we'll use a simulated detection based on image name
        
        # Simulated disease detection - replace with actual ML model
        # Common diseases based on image characteristics (would use ML in production)
        detected_disease = 'leaf_rust'  # Default
        
        # Simple logic based on file size (in real scenario, use image analysis)
        if file and file.filename:
            # You can add ML model prediction here
            # For demo, randomly select from common diseases
            diseases_list = list(DISEASE_DATA.keys())[:-1]  # Exclude 'healthy'
            import random
            detected_disease = random.choice(diseases_list)
        
        disease_info = DISEASE_DATA.get(detected_disease, DISEASE_DATA['healthy'])
        
        return jsonify({
            'disease': detected_disease.replace('_', ' ').title(),
            'description': disease_info['description'],
            'treatment': disease_info['treatment'],
            'severity': disease_info['severity'],
            'confidence': round(np.random.uniform(0.75, 0.98), 2)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== WEATHER API ====================
@app.route('/api/weather/<location>', methods=['GET'])
def get_weather(location):
    """
    Get weather data for a location
    Supports multiple data sources: OpenWeatherMap, WeatherAPI, etc.
    """
    try:
        # Try to fetch from external API (OpenWeatherMap)
        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        if api_key:
            # Using OpenWeatherMap API
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'location': location.capitalize(),
                    'temperature': round(data['main']['temp'], 1),
                    'humidity': data['main']['humidity'],
                    'rainfall_chance': data.get('clouds', {}).get('all', 0),
                    'wind_speed': round(data['wind']['speed'], 1),
                    'description': data['weather'][0]['description'].title(),
                    'pressure': data['main']['pressure'],
                    'feels_like': round(data['main']['feels_like'], 1),
                }
            else:
                # Fallback to mock data
                weather_data = get_mock_weather(location)
        else:
            # Use mock data if no API key
            weather_data = get_mock_weather(location)
        
        # Generate advisory based on weather
        advisory = generate_weather_advisory(weather_data)
        weather_data['advisory'] = advisory
        
        return jsonify(weather_data), 200
    
    except Exception as e:
        # Return mock data on error
        weather_data = get_mock_weather(location)
        advisory = generate_weather_advisory(weather_data)
        weather_data['advisory'] = advisory
        return jsonify(weather_data), 200


def get_mock_weather(location):
    """Generate mock weather data"""
    import random
    return {
        'location': location.capitalize(),
        'temperature': round(np.random.uniform(18, 32), 1),
        'humidity': random.randint(40, 85),
        'rainfall_chance': random.randint(0, 60),
        'wind_speed': round(np.random.uniform(2, 15), 1),
        'description': random.choice(['Clear Sky', 'Partly Cloudy', 'Overcast', 'Light Rain']),
        'pressure': random.randint(1000, 1020),
        'feels_like': round(np.random.uniform(16, 30), 1),
    }


def generate_weather_advisory(weather_data):
    """Generate farming advisory based on weather"""
    temp = weather_data['temperature']
    humidity = weather_data['humidity']
    rainfall = weather_data['rainfall_chance']
    
    advisory = []
    
    # Temperature advisory
    if temp < 15:
        advisory.append("⚠️ Low temperature - Cover crops if necessary. Reduce irrigation.")
    elif temp > 35:
        advisory.append("⚠️ High temperature - Increase irrigation frequency. Apply mulch.")
    else:
        advisory.append("✓ Temperature optimal for most crops.")
    
    # Humidity advisory
    if humidity < 30:
        advisory.append("⚠️ Low humidity - Risk of pest infestation. Increase irrigation.")
    elif humidity > 85:
        advisory.append("⚠️ High humidity - Risk of fungal diseases. Improve ventilation.")
    else:
        advisory.append("✓ Humidity levels favorable for crop growth.")
    
    # Rainfall advisory
    if rainfall > 70:
        advisory.append(f"⚠️ {rainfall}% chance of rain. Postpone pesticide spraying. Ensure drainage.")
    elif rainfall > 40:
        advisory.append(f"ℹ️ {rainfall}% chance of rain. Monitor weather conditions.")
    else:
        advisory.append(f"✓ Low rainfall expected. Good time for field operations.")
    
    return " ".join(advisory)


# ==================== RECORDS API ====================
@app.route('/api/records', methods=['GET'])
def get_records():
    """Retrieve all farmer records"""
    try:
        with open(RECORDS_FILE, 'r') as f:
            records = json.load(f)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/records/save', methods=['POST'])
def save_record():
    """Save a new farmer record"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['location', 'crop']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Read existing records
        with open(RECORDS_FILE, 'r') as f:
            records = json.load(f)
        
        # Create new record
        new_record = {
            'id': len(records) + 1,
            'location': data['location'],
            'crop': data['crop'],
            'timestamp': datetime.now().isoformat(),
            'details': data.get('details', {})
        }
        
        # Append and save
        records.append(new_record)
        with open(RECORDS_FILE, 'w') as f:
            json.dump(records, f, indent=2)
        
        return jsonify({
            'message': 'Record saved successfully',
            'record': new_record
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a farmer record"""
    try:
        with open(RECORDS_FILE, 'r') as f:
            records = json.load(f)
        
        records = [r for r in records if r.get('id') != record_id]
        
        with open(RECORDS_FILE, 'w') as f:
            json.dump(records, f, indent=2)
        
        return jsonify({'message': 'Record deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'AgroSense backend is running',
        'timestamp': datetime.now().isoformat()
    }), 200


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    import os
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Enable debug mode only in development (when PORT is not set)
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
