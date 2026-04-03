const express = require('express');
const mongoose = require('mongoose');

const app = express();
const PORT = 3000;

const MONGO_URI = process.env.MONGO_URI;

mongoose
    .connect(MONGO_URI)
    .then( () => { console.log('MongoDB connected Successfully') })
    .catch( err => { console.error('Failed to connect MongoDB, connection error:', err) });

app.get('/', (req, res) => {
    res.send('Server running inside: (Docker + MongoDB) connected');
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});