const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// 1. Basic Test Route
app.get('/', (req, res) => {
    res.json({ status: 'AgroSense API is running successfully' });
});

// 2. Endpoint to Save Form Data into records.json
app.post('/api/save-record', (req, res) => {
    try {
        const filePath = path.join(__dirname, 'data', 'records.json');
        
        // Read existing records
        let records = [];
        if (fs.existsSync(filePath)) {
            const fileData = fs.readFileSync(filePath, 'utf8');
            records = JSON.parse(fileData);
        }

        // Create new entry with an ID and timestamp
        const newEntry = {
            id: records.length + 1,
            ...req.body,
            timestamp: new Date().toISOString()
        };
        
        records.push(newEntry);

        // Write updated array back to records.json
        fs.writeFileSync(filePath, JSON.stringify(records, null, 2));

        res.status(200).json({ success: true, message: 'Saved to records.json successfully!', data: newEntry });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, error: 'Failed to save record' });
    }
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
