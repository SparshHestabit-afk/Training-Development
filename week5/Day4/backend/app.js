const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({
        message: 'Hello from Backend',
        protocol: req.protocol
    });
});

app.listen(3000, () => {
    console.log('Backend running on port: 3000');
})