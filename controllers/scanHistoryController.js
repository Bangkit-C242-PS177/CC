const pool = require('../config/db');

// Menambahkan riwayat scan
exports.addScanHistory = async (req, res) => {
  const { userId, scanResult, date } = req.body;
  try {
    const query = 'INSERT INTO scan_history (user_id, scan_result, date) VALUES (?, ?, ?)';
    await pool.query(query, [userId, scanResult, date]);
    res.status(201).send('Scan history added');
  } catch (error) {
    res.status(500).send(error.message);
  }
};

// Mendapatkan riwayat scan
exports.getScanHistory = async (req, res) => {
  const { userId } = req.params;
  try {
    const query = 'SELECT * FROM scan_history WHERE user_id = ?';
    const [rows] = await pool.query(query, [userId]);
    res.status(200).json(rows);
  } catch (error) {
    res.status(500).send(error.message);
  }
};
