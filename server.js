const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

const usersRoutes = require('./routes/users');
const skincareRoutes = require('./routes/skincare');
const flaskRoutes = require('./routes/flask');

app.use(cors());
app.use(express.json());

// Routes
app.use('/users', usersRoutes);
app.use('/skincare', skincareRoutes);
app.use('/flask', flaskRoutes);

app.listen(port, () => {
  console.log(`Express.js server running on http://localhost:${port}`);
});
