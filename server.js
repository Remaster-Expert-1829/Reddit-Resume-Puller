const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 8000;

// Enable CORS so VS Code Live Server can talk to this backend
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    if (req.method === 'OPTIONS') {
        return res.sendStatus(200);
    }
    next();
});

// Serve static files from the current directory
app.use(express.static(__dirname));

// API endpoint to trigger python script
app.post('/api/refresh', (req, res) => {
    console.log('Triggering data refresh...');
    // Run the python script
    exec('python main.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ 
                status: 'error', 
                message: 'Script failed.', 
                error: stderr || error.message 
            });
        }
        
        console.log(`stdout: ${stdout}`);
        if (stderr) console.error(`stderr: ${stderr}`);
        
        res.json({ 
            status: 'success', 
            message: 'Data refreshed successfully!' 
        });
    });
});

app.listen(PORT, () => {
    console.log(`Node server running at http://localhost:${PORT}`);
    console.log(`Serving static files from ${__dirname}`);
    console.log('Press Ctrl+C to stop.');
});
