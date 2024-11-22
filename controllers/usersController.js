exports.getUsers = (req, res) => {
    // Fetch users from database
    res.send('Fetch all users');
  };
  
  exports.createUser = (req, res) => {
    // Add user to database
    res.send('Create a new user');
  };
  