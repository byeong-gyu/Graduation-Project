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

router.get('/main', (req,res,next)=> {
    let is_login = req.session.is_login;
    let ss_userID = req.session.ss_userID;
    res.render(path.join(__dirname, '../../front-end/main'),{
        is_login : is_login,
        ss_userID : ss_userID
    })
    console.log('로그인 상태 : '+ is_login)
    console.log('로그인 아이디 : '+ ss_userID)
});

router.get('/logoutAction',(req,res)=>{
    console.log('로그아웃 성공');
    req.session.destroy(function(err){
     res.redirect('/');
    })
   });


module.exports = router;