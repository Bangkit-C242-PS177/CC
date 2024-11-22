const express = require('express');
const { addScanHistory, getScanHistory } = require('../controllers/scanHistoryController');

const router = express.Router();

router.post('/add', addScanHistory);
router.get('/:userId', getScanHistory);

module.exports = router;
