# AgroSense Backend API

A comprehensive backend for the AgroSense smart farming assistant application, providing APIs for crop recommendation, disease detection, weather intelligence, and farmer records management.

## Features

- **Crop Recommendation**: AI-powered crop suggestions based on soil nutrients and climate data
- **Disease Detection**: Identify plant diseases from leaf images and get treatment recommendations
- **Weather Intelligence**: Real-time weather data with agricultural advisory
- **Farmer Records**: Store and manage farming records with location and crop information
- **RESTful API**: Clean, well-documented REST API endpoints
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone/Extract the project**
```bash
cd Agrosense-AI-based-smart-farming-assistant-/backend
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenWeatherMap API key (optional)
# OPENWEATHER_API_KEY=your_api_key_here
```

5. **Run the backend**
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health` - Check API status

### Crop Recommendation
- **POST** `/api/crop/recommend` - Get crop recommendations
  
  Request body:
  ```json
  {
    "nitrogen": 78,
    "phosphorus": 41,
    "potassium": 43,
    "temperature": 20.0,
    "humidity": 56,
    "ph": 6.5,
    "rainfall": 356
  }
  ```
  
  Response:
  ```json
  {
    "recommended_crop": "Cotton",
    "confidence_score": 92.5,
    "all_recommendations": [
      {"crop": "Cotton", "score": 92.5},
      {"crop": "Sugarcane", "score": 88.3}
    ]
  }
  ```

### Disease Detection
- **POST** `/api/disease/detect` - Analyze leaf image for diseases
  
  Form data:
  - `image` (file) - Leaf image file (JPG, PNG)
  
  Response:
  ```json
  {
    "disease": "Leaf Rust",
    "description": "Brown/orange pustules on leaves",
    "treatment": "Apply fungicide spray...",
    "severity": "Medium",
    "confidence": 0.87
  }
  ```

### Weather Intelligence
- **GET** `/api/weather/<location>` - Get weather data and advisory
  
  Example: `/api/weather/Bengaluru`
  
  Response:
  ```json
  {
    "location": "Bengaluru",
    "temperature": 28.5,
    "humidity": 65,
    "rainfall_chance": 12,
    "wind_speed": 8.5,
    "description": "Clear Sky",
    "pressure": 1013,
    "feels_like": 30.2,
    "advisory": "✓ Temperature optimal... ✓ Humidity levels favorable..."
  }
  ```

### Farmer Records
- **GET** `/api/records` - Get all farmer records
  
  Response:
  ```json
  [
    {
      "id": 1,
      "location": "Bengaluru",
      "crop": "Ragi",
      "timestamp": "2026-08-31T10:30:00",
      "details": {}
    }
  ]
  ```

- **POST** `/api/records/save` - Save a new record
  
  Request body:
  ```json
  {
    "location": "Pune",
    "crop": "Sugarcane",
    "details": {"area": "2 acres", "irrigation": "drip"}
  }
  ```
  
  Response: (201 Created)
  ```json
  {
    "message": "Record saved successfully",
    "record": { ... }
  }
  ```

- **DELETE** `/api/records/<id>` - Delete a record
  
  Response:
  ```json
  {
    "message": "Record deleted successfully"
  }
  ```

## Integration with Frontend

### Update Frontend Files

Update your frontend to call the backend APIs. Here's an example for the crop recommendation:

**In crop.html, update the form handler:**
```javascript
document.getElementById('crop-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nitrogen: parseFloat(document.getElementById('nitrogen').value),
        phosphorus: parseFloat(document.getElementById('phosphorus').value),
        potassium: parseFloat(document.getElementById('potassium').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        ph: parseFloat(document.getElementById('ph').value),
        rainfall: parseFloat(document.getElementById('rainfall').value)
    };
    
    try {
        const response = await fetch('http://localhost:5000/api/crop/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        document.getElementById('recommended-crop-element').textContent = result.recommended_crop;
    } catch (error) {
        console.error('Error:', error);
    }
});
```

## Environment Variables

Create a `.env` file in the backend directory:

```
OPENWEATHER_API_KEY=your_openweathermap_api_key
FLASK_ENV=development
FLASK_DEBUG=True
```

To get a free OpenWeatherMap API key:
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
├── .env                  # Environment variables (create this)
├── data/                 # Data storage
│   └── records.json      # Farmer records
└── models/               # ML models (optional)
    └── crop_model.pkl    # Pre-trained model (optional)
```

## Development

### Running in Development Mode

```bash
python app.py
```

The API will be available at `http://localhost:5000` with auto-reload on file changes.

### Testing Endpoints

Use Postman, cURL, or any REST client:

```bash
# Test health check
curl http://localhost:5000/api/health

# Test crop recommendation
curl -X POST http://localhost:5000/api/crop/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 78,
    "phosphorus": 41,
    "potassium": 43,
    "temperature": 20.0,
    "humidity": 56,
    "ph": 6.5,
    "rainfall": 356
  }'
```

## Production Deployment

### Using Gunicorn (Production WSGI Server)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t agrosense-backend .
docker run -p 5000:5000 agrosense-backend
```

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py:
# app.run(port=5001)
```

### CORS Issues
The app includes CORS support. If you still encounter CORS errors, update the CORS configuration in `app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://your-frontend-url"],
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Module Not Found
Ensure your virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Future Enhancements

- [ ] Integrate ML model for disease detection (TensorFlow/PyTorch)
- [ ] Add user authentication and JWT tokens
- [ ] Implement database (PostgreSQL/MongoDB)
- [ ] Add caching with Redis
- [ ] Integrate real weather APIs
- [ ] Add analytics and reporting
- [ ] Mobile app API support
- [ ] Implement WebSockets for real-time updates

## License

MIT License

## Support

For issues, questions, or suggestions, please contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: 2026-08-31
