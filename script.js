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

