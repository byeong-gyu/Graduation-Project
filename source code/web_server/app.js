const express = require('express');
const cookieParser = require('cookie-parser');
const morgan = require('morgan');
const path = require('path');
const session = require('express-session');
const dotenv = require('dotenv');
const db = require('./config/mysql');
const ejs = require('ejs');
const cors= require('cors');
const FileStore = require('session-file-store')(session); // 세션을 파일에 저장



dotenv.config();
//서버 오픈
const app = express();
app.set('port', process.env.PORT || 3000);
//넌적스 템플릿 엔진
app.set('front-end',__dirname+'../front-end');
//엔진을 사용할 폴더명, 경로
app.set('view engine', 'ejs');
//요청 에러 기록
app.use(morgan('dev'));
//실제 주소 숨기기
app.use(express.static(path.join(__dirname, '../front-end')));
//req.body 값 불러오기
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

//app.use(cookieParser(process.env.COOKIE_SECRET));

app.use(cookieParser('secret'));

app.use(session({
  resave: false,
  saveUninitialized: true,
 // secret: process.env.COOKIE_SECRET,
  secret:'secret',
  store : new FileStore(), // 세션이 데이터를 저장하는 곳    
  cookie: {
    expires: 60 * 60 * 24,
    httpOnly: true,//자바스크립트로 공격을 당하지 않게
  },
}));
//데이터 처리 방식

app.use(cors({
  //데이터 요청을 모두 허용
  origin:true, 
  //Access-Control-Allow-Credentials : true
  credentials : true
}))

app.use('/', require('./routes/pages'));
app.use('/auth', require('./routes/auth'));



app.use((req, res, next) => {
  const error =  new Error(`${req.method} ${req.url} 라우터가 없습니다.`);
  error.status = 404;
  next(error);
});

app.use((err, req, res, next) => {
  res.locals.message = err.message;
  res.locals.error = process.env.NODE_ENV !== 'production' ? err : {};
  res.status(err.status || 500);
  res.render('error');
});//개발일 땐 에러 상세내역 보여주기, 배포 모드일 땐 감추기


app.listen(app.get('port'), () => {
  console.log(app.get('port'), '번 포트에서 대기중');
});
// app.get('port') port 값을 받은 후 
// 서버 열기, 열렸다면 서버 실행을 콘솔창에 출력
