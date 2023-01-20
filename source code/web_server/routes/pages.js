const express = require('express');
const router = express.Router();
const path = require('path'); 

router.get('/', (req,res,next)=>{
res.render(path.join(__dirname,'../../front-end/index'))
});

module.exports = router;