const { bucket } = require('../config/storage');

// Upload file ke Cloud Storage
exports.uploadFile = async (req, res) => {
  try {
    const file = req.file;
    if (!file) return res.status(400).send('No file uploaded.');

    const blob = bucket.file(file.originalname);
    const blobStream = blob.createWriteStream();

    blobStream.on('finish', () => {
      const publicUrl = `https://storage.googleapis.com/${bucket.name}/${blob.name}`;
      res.status(200).send({ message: 'File uploaded successfully', url: publicUrl });
    });

    blobStream.on('error', (err) => res.status(500).send(err.message));
    blobStream.end(file.buffer);
  } catch (error) {
    res.status(500).send(error.message);
  }
};

// List file di Cloud Storage
exports.listFiles = async (req, res) => {
  try {
    const [files] = await bucket.getFiles();
    const fileNames = files.map(file => file.name);
    res.status(200).send(fileNames);
  } catch (error) {
    res.status(500).send(error.message);
  }
};
