const express = require('express');
const multer = require('multer');
const upload = multer({ storage: multer.memoryStorage() });
const { uploadFile, listFiles } = require('../controllers/storageController');

const router = express.Router();

router.post('/upload', upload.single('file'), uploadFile);
router.get('/list', listFiles);

module.exports = router;
