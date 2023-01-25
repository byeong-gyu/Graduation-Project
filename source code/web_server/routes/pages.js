const express = require('express');
const router = express.Router();
const path = require('path'); 

router.get('/', (req,res,next)=>{
res.render(path.join(__dirname,'../../front-end/index'))
});

router.get('/login', (req,res,next)=>{
res.render(path.join(__dirname,'../../front-end/login'))
});

router.get('/join', (req,res,next)=> {
res.render(path.join(__dirname, '../../front-end/join'))
});

module.exports = router;