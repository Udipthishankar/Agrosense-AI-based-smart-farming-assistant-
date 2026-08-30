const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

// 1. Connect to MongoDB Atlas (Replace with your connection string or use local SQLite)
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/agrosense';
mongoose.connect(MONGO_URI)
    .then(() => console.log('Connected to AgroSense Database'))
    .catch(err => console.error('Database connection error:', err));

// 2. Define a Schema for Contact Messages / User Queries
const ContactSchema = new mongoose.Schema({
    name: String,
    email: String,
    message: String,
    date: { type: Date, default: Date.now }
});
const Contact = mongoose.model('Contact', ContactSchema);

// 3. API Endpoint to handle Contact Form submissions from about.html
app.post('/api/contact', async (req, res) => {
    try {
        const { name, email, message } = req.body;
        const newContact = new Contact({ name, email, message });
        await newContact.save();
        res.json({ success: true, message: 'Message saved successfully to database!' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 4. API Endpoint for Chatbot (Connects to OpenAI / ChatGPT or local logic)
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        
        // You can integrate OpenAI SDK here using process.env.OPENAI_API_KEY
        // For now, it returns a smart fallback response
        let reply = "I am your AgroSense AI farming assistant. Make sure your soil pH and N-P-K levels are balanced!";
        if (message.toLowerCase().includes('crop')) {
            reply = "Use our Crop AI tool page to calculate the best crop based on your local soil metrics.";
        }

        res.json({ success: true, reply });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => console.log(`AgroSense Backend running on port ${PORT}`));

