const express = require('express');
const app = express();

const PORT = 3000;
const INSTANCE_ID = process.env.INSTANCE_ID || 0;

app.get('/api', (req, res) => {
  res.send(`Hello from backend instance ${INSTANCE_ID}`);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Backend instance ${INSTANCE_ID} running on port ${PORT}`);
});
