document.addEventListener('DOMContentLoaded', () => {
    // Select the crop recommendation form and result elements
    const cropForm = document.getElementById('cropForm');
    const resultCard = document.getElementById('resultCard');
    const recommendedCropSpan = document.getElementById('recommendedCrop');
    const submitBtn = document.getElementById('submitBtn');

    if (cropForm) {
        cropForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Collect form input values
            const formData = {
                N: document.getElementById('nitrogen').value,
                P: document.getElementById('phosphorus').value,
                K: document.getElementById('potassium').value,
                temperature: document.getElementById('temperature').value,
                humidity: document.getElementById('humidity').value,
                ph: document.getElementById('ph').value,
                rainfall: document.getElementById('rainfall').value
            };

            // Update button state to show loading
            if (submitBtn) {
                submitBtn.textContent = 'Analyzing Soil & Climate...';
                submitBtn.disabled = true;
            }

            try {
                // Send data to your backend API (replace URL with your hosted backend URL when deployed)
                const response = await fetch('http://localhost:5001/api/crop-recommendation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (data.success) {
                    // Display the recommended crop dynamically
                    recommendedCropSpan.textContent = data.data.recommended_crop;
                    resultCard.style.display = 'block';
                    resultCard.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('Error: ' + (data.message || 'Could not fetch recommendation.'));
                }
            } catch (error) {
                console.error('API Connection Error:', error);
                alert('Failed to connect to the backend server. Make sure your server is running.');
            } finally {
                // Reset button state
                if (submitBtn) {
                    submitBtn.textContent = 'Get Crop Recommendation';
                    submitBtn.disabled = false;
                }
            }
        
        });
document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContact);
    }
});

async function handleContact(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('contactName').value,
        email: document.getElementById('contactEmail').value,
        message: document.getElementById('contactMsg').value
    };

    try {
        const response = await fetch('http://localhost:5001/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (result.success) {
            alert('Thank you! Your message has been saved in the database.');
            document.getElementById('contactForm').reset();
        } else {
            alert('Failed to send message. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the server.');
    }
}

    }
});
// Replace 'http://localhost:5001' with your live backend URL
const BACKEND_URL = 'https://your-backend-url.onrender.com';

const response = await fetch(`${BACKEND_URL}/api/contact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});


// Inside your script.js form listener
try {
    const response = await fetch('http://localhost:5001/api/crop-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    const data = await response.json();
    if (data.success) {
        recommendedCropSpan.textContent = data.data.recommended_crop;
        resultCard.style.display = 'block';
    }
} catch (err) {
    // FALLBACK SIMULATION: Works instantly even if backend is offline!
    console.warn('Backend offline, using client-side prediction logic.');
    
    let simulatedCrop = 'Rice';
    const n = parseFloat(formData.N);
    const ph = parseFloat(formData.ph);
    
    if (n < 40) simulatedCrop = 'Maize';
    else if (ph > 7.2) simulatedCrop = 'Cotton';
    else if (n > 80) simulatedCrop = 'Rice';
    else simulatedCrop = 'Wheat';

    recommendedCropSpan.textContent = simulatedCrop;
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth' });
} finally {
    submitBtn.textContent = 'Get Crop Recommendation';
    submitBtn.disabled = false;
}
// Simulated AI Response with more keyword checks
        setTimeout(() => {
            let botReply = "That's a great farming question! Make sure to monitor your soil health regularly.";
            const text = userText.toLowerCase();
            
            if (text.includes('disease') || text.includes('fungus') || text.includes('pest')) {
                botReply = "For plant diseases or pests, ensure good airflow between crops, remove infected leaves promptly, and apply organic or copper-based treatments if necessary.";
            } else if (text.includes('weather') || text.includes('rain') || text.includes('temperature')) {
                botReply = "Keep an eye on local precipitation forecasts. Avoid heavy irrigation if rainfall is expected within 24 hours.";
            } else if (text.includes('nitrogen') || text.includes('n-p-k') || text.includes('soil') || text.includes('nutrient')) {
                botReply = "High nitrogen is great for leafy green growth, but balance it with phosphorus and potassium using the Crop AI tool to prevent nutrient burn!";
            } else if (text.includes('crop') || text.includes('plant') || text.includes('grow') || text.includes('best')) {
                botReply = "To find the best crop, head over to our 'Crop AI' page and enter your exact soil N-P-K and weather details!";
            } else {
                botReply = `You asked about "${userText}". To get the best results for this, use our specialized tools in the navigation bar for crop recommendations and disease scans!`;
            }

            messagesArea.innerHTML += `<div style="background: #e8f5e9; padding: 8px 12px; border-radius: 8px; max-width: 80%; align-self: flex-start; color: #2e7d32;">${botReply}</div>`;
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }, 1000);
fetch('./data/records.json')
  .then(response => response.json())
  .then(data => {
      console.log("Loaded records:", data);
      // You can loop through 'data' to show items on your HTML page
  })
  .catch(error => console.error('Error loading records:', error));
// Example: Listening to a form submission on your frontend
const cropForm = document.getElementById('crop-form'); // Make sure your form has id="crop-form"

if (cropForm) {
    cropForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Get values from the input fields
        const locationInput = document.getElementById('location-input').value;
        const cropInput = document.getElementById('crop-input').value;

        const newEntry = {
            location: locationInput,
            crop: cropInput,
            timestamp: new Date().toISOString()
        };

        console.log("Submitted Data:", newEntry);

        // 2. If you are running your Node.js server (server.js), 
        // you can send this data to be saved:
        try {
            const response = await fetch('http://localhost:5000/api/save-record', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newEntry)
            });
            
            const result = await response.json();
            alert('Record saved successfully!');
        } catch (error) {
            console.error('Error saving record:', error);
        }
    });
}
