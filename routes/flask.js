const express = require('express');
const axios = require('axios');
const router = express.Router();

router.post('/predict', async (req, res) => {
  try {
    const flaskApiUrl = 'http://localhost:5000/predict'; // Adjust with Flask URL
    const response = await axios.post(flaskApiUrl, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

module.exports = router;
