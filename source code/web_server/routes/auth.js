const express = require('express');
const authController = require('../controllers/auth');
const router = express.Router();

router.post('/join',authController.join)

module.exports = router;