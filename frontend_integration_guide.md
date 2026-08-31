# AgroSense Frontend-Backend Integration Guide

This guide helps you integrate the backend API with your existing frontend files.

## Quick Start

### 1. Start the Backend Server

```bash
cd backend
python app.py
```

The server will run at `http://localhost:5000`

### 2. Update Your Frontend Files

#### A. Crop Recommendation Page (crop.html)

Replace or add this script at the end of crop.html:

```html
<script>
// Fetch crop recommendations from backend
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
        document.querySelector('.result-container p:last-child').textContent = 
            `Confidence Score: ${result.confidence_score}%`;
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get recommendation. Make sure backend is running!');
    }
});
</script>
```

#### B. Disease Detection Page (disease.html)

Replace or add this script at the end of disease.html:

```html
<script>
// ... existing image preview code ...

// Handle form submission for disease detection
const diseaseForm = document.getElementById('diseaseForm');
const leafInput = document.getElementById('leafImage');
const diseaseResultCard = document.getElementById('diseaseResultCard');

diseaseForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!leafInput.files[0]) {
        alert('Please select an image');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', leafInput.files[0]);
    
    try {
        document.getElementById('analyzeBtn').textContent = 'Analyzing...';
        document.getElementById('analyzeBtn').disabled = true;
        
        const response = await fetch('http://localhost:5000/api/disease/detect', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        // Display results
        document.getElementById('diseaseName').textContent = result.disease;
        document.getElementById('treatmentText').innerHTML = 
            `<strong>Condition:</strong> ${result.description}<br><br>
             <strong>Treatment:</strong> ${result.treatment}<br><br>
             <strong>Severity:</strong> ${result.severity}<br>
             <strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%`;
        
        diseaseResultCard.style.display = 'block';
        diseaseResultCard.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze image. Make sure backend is running!');
    } finally {
        document.getElementById('analyzeBtn').textContent = 'Analyze Plant Health';
        document.getElementById('analyzeBtn').disabled = false;
    }
});
</script>
```

#### C. Weather Page (weather.html)

Replace or add this script at the end of weather.html:

```html
<script>
// Fetch weather data from backend
function fetchWeather() {
    const location = document.getElementById('locationInput').value || 'Bengaluru';
    
    fetch(`http://localhost:5000/api/weather/${location}`)
        .then(response => response.json())
        .then(data => {
            // Update weather cards
            document.getElementById('tempVal').textContent = data.temperature + '°C';
            document.getElementById('humVal').textContent = data.humidity + '%';
            document.getElementById('rainVal').textContent = data.rainfall_chance + '%';
            
            // Update advisory
            document.getElementById('advisoryText').textContent = data.advisory;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to fetch weather. Make sure backend is running!');
        });
}

// Allow Enter key to trigger search
document.getElementById('locationInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        fetchWeather();
    }
});

// Load initial weather on page load
window.addEventListener('load', () => {
    fetchWeather();
});
</script>
```

## Configuration

### For Local Development

Your frontend should use:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### For Production

Update to your production URL:
```javascript
const API_BASE_URL = 'https://your-production-domain.com/api';
```

## Complete Updated Files

Here are the complete updated HTML files with backend integration:

### Updated crop.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroSense - Crop AI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="logo">🌿 AgroSense</div>
        <nav>
            <a href="index.html">Home</a>
            <a href="crop.html" class="active">Crop AI</a>
            <a href="disease.html">Disease Detection</a>
            <a href="weather.html">Weather</a>
            <a href="about.html">About</a>
        </nav>
    </header>

    <div class="container">
        <h2 class="page-title">Smart Crop Recommendation</h2>
        <p style="text-align: center; color: #666; margin-bottom: 20px;">
            Enter your soil nutrients and climate details to find the best crop.
        </p>

        <form id="crop-form">
            <label>Nitrogen (N):</label>
            <input type="number" id="nitrogen" value="78" required>

            <label>Phosphorus (P):</label>
            <input type="number" id="phosphorus" value="41" required>

            <label>Potassium (K):</label>
            <input type="number" id="potassium" value="43" required>

            <label>Temperature (°C):</label>
            <input type="number" step="0.1" id="temperature" value="20.0" required>

            <label>Humidity (%):</label>
            <input type="number" id="humidity" value="56" required>

            <label>Soil pH:</label>
            <input type="number" step="0.1" id="ph" value="6.5" required>

            <label>Rainfall (mm):</label>
            <input type="number" step="0.1" id="rainfall" value="356" required>

            <button type="submit" id="recommend-btn">Get Crop Recommendation</button>
        </form>

        <div class="result-container" style="margin-top: 20px; padding: 15px; background: #eef9ee; border-left: 5px solid #28a745;">
            <p style="margin: 0; font-weight: bold;">🌾 Recommended Crop:</p>
            <h3 id="recommended-crop-element" style="margin: 5px 0 0 0; color: #28a745;">-</h3>
            <p id="confidence-score" style="margin: 8px 0 0 0; color: #666; font-size: 0.9rem;">-</p>
        </div>
    </div>

    <script>
        const API_BASE_URL = 'http://localhost:5000/api';

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
                const btn = document.getElementById('recommend-btn');
                btn.textContent = 'Analyzing...';
                btn.disabled = true;
                
                const response = await fetch(`${API_BASE_URL}/crop/recommend`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) throw new Error('API error');
                
                const result = await response.json();
                document.getElementById('recommended-crop-element').textContent = result.recommended_crop;
                document.getElementById('confidence-score').textContent = 
                    `Confidence Score: ${result.confidence_score.toFixed(1)}/100`;
                
                btn.textContent = 'Get Crop Recommendation';
                btn.disabled = false;
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to get recommendation. Make sure the backend is running on http://localhost:5000');
                document.getElementById('recommend-btn').textContent = 'Get Crop Recommendation';
                document.getElementById('recommend-btn').disabled = false;
            }
        });
    </script>
</body>
</html>
```

### Updated weather.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgroSense - Weather & Advisory</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .weather-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
            margin-bottom: 25px;
        }
        .weather-card {
            background: #e8f5e9;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-top: 4px solid #2e7d32;
        }
        .weather-card h4 {
            color: #1b5e20;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        .weather-card p {
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
        }
        .advisory-box {
            background: #fff8e1;
            border-left: 6px solid #ffb300;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo">🌿 AgroSense</div>
        <nav>
            <a href="index.html">Home</a>
            <a href="crop.html">Crop AI</a>
            <a href="disease.html">Disease Detection</a>
            <a href="weather.html" class="active">Weather</a>
            <a href="about.html">About</a>
        </nav>
    </header>

    <div class="container">
        <h2 class="page-title">Agricultural Weather Intelligence</h2>
        <p style="text-align: center; margin-bottom: 20px; color: #666;">
            Real-time localized climate data to assist with irrigation and field operations.
        </p>

        <div class="form-group" style="margin-bottom: 20px;">
            <label>Enter Location / Region:</label>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="locationInput" placeholder="e.g., Bengaluru" 
                       style="flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px;">
                <button type="button" class="btn" style="width: auto; padding: 10px 20px;" onclick="fetchWeather()">
                    Check Weather
                </button>
            </div>
        </div>

        <div class="weather-grid">
            <div class="weather-card">
                <h4>Temperature</h4>
                <p id="tempVal">--°C</p>
            </div>
            <div class="weather-card">
                <h4>Humidity</h4>
                <p id="humVal">--%</p>
            </div>
            <div class="weather-card">
                <h4>Rainfall Chance</h4>
                <p id="rainVal">--%</p>
            </div>
        </div>

        <div class="advisory-box">
            <h3 style="color: #ff8f00; margin-bottom: 5px;">🚜 Farming Advisory:</h3>
            <p id="advisoryText">Loading weather data...</p>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 AgroSense. Empowering modern agriculture.</p>
    </footer>

    <script>
        const API_BASE_URL = 'http://localhost:5000/api';

        function fetchWeather() {
            const location = document.getElementById('locationInput').value.trim() || 'Bengaluru';
            
            fetch(`${API_BASE_URL}/weather/${encodeURIComponent(location)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('tempVal').textContent = data.temperature + '°C';
                    document.getElementById('humVal').textContent = data.humidity + '%';
                    document.getElementById('rainVal').textContent = data.rainfall_chance + '%';
                    document.getElementById('advisoryText').textContent = data.advisory;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('advisoryText').textContent = 
                        'Failed to fetch weather. Make sure the backend is running.';
                });
        }

        document.getElementById('locationInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                fetchWeather();
            }
        });

        // Load default weather on page load
        window.addEventListener('load', () => {
            fetchWeather();
        });
    </script>
</body>
</html>
```

## Testing the Integration

### 1. Test Backend API
```bash
# Check if backend is running
curl http://localhost:5000/api/health
```

### 2. Test in Browser
- Open `http://localhost:3000` (or your frontend URL)
- Navigate to Crop AI page and submit the form
- Check browser console (F12) for any errors
- Check backend terminal for logs

### 3. Troubleshooting

**Error: "Failed to get recommendation"**
- Ensure backend is running: `python app.py` in backend folder
- Check browser console for CORS errors
- Verify the API_BASE_URL is correct

**Error: "Module not found"**
- Install dependencies: `pip install -r requirements.txt`
- Activate virtual environment

## Next Steps

1. **Customize API URLs** - Update API_BASE_URL for your deployment
2. **Add Error Handling** - Add user-friendly error messages
3. **Add Loading States** - Show spinners during API calls
4. **Persist User Data** - Save preferences and history
5. **Add Authentication** - Implement user login system
6. **Deploy Backend** - Use Heroku, AWS, or similar for production

---

For more details, see `backend/README.md`
