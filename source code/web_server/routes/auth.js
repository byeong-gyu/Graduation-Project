const express = require('express');
//const authController = require('../controllers/auth');
const router = express.Router();
const mysql = require('mysql2');
const bcrypt= require('bcrypt');
const path = require('path');
const session = require('express-session');
const FileStore = require('session-file-store')(session);

const saltRounds = 12;


const db = mysql.createConnection({
    host     : process.env.DB_HOST,
    user     : process.env.DB_USER,
    password : process.env.DB_PASSWORD,
    database : process.env.DB
});

//router.post('/join',authController.join)
//router.post('/login',authController.login)

//회원가입
router.post('/join', (req,res,next) => {
  const param = [req.body.userID, req.body.userPassID, req.body.userName, req.body.userGender, req.body.userEmail, req.body.userCode]
  bcrypt.hash(param[1], saltRounds, (error, hash)=> {
    param[1]=hash
    db.query('INSERT INTO users(`userID`, `userPassID`, `userName`, `userGender`, `userEmail`, `userCode`) VALUES(?,?,?,?,?,?)', param, (error, row)=>{
      if(error) {console.log(error)
        console.log('이미 존재하는 아이디 입니다');
      } else {
        console.log(req.body);
      }
    })
  })
  res.redirect('/login');
});


router.post('/login', (req,res,next)=>{
     let param = req.body;
     console.log(param);

     let userID = param.userID;
     let userPassID = param.userPassID;
     let is_login = false;
     req.session.ss_userID = userID;

     db.query('SELECT * FROM users WHERE userID=?', userID,(error,data)=>{
       if(error) console.log(error);

        if(data.length > 0){
          //비밀번호 일치 여부 확인
          bcrypt.compare(param.userPassID,data[0].userPassID,(error,result)=>{
            if(result){
              req.session.userID=param.userID;
              req.session.userPassID=param.userPassID;
              req.session.is_login= true;              
              console.log('로그인 성공')
              
              //로그인을 성공하면 rediect로 main화면 띄우고 세션 정보 저장
              req.session.save(function(){
              console.log( req.session.id,req.session.pw)
                res.redirect('/main'),{
                  is_login : true,
                  userID : userID,
                  userPassID : userPassID,
                }
              })
            }  else{
              console.log('비밀번호 오류');
              res.redirect('/login');
            }
          })
        } else {
         console.log('존재하지 않는 아이디');
         res.redirect('/login');
        }
      })

    });



    

module.exports = router;
