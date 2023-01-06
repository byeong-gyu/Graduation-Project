const express = require('express');//express 서버
const path = require ('path');

const app = express();

app.use((req,res,next)=>{
console.log('모든 요청 미들웨어')
next();//exress는 위에서 내려오며 실행하지만 미들웨어는 next를 해야
// 다음이 실행됨
// },(req,res,next)=>{
//     try{
//         console.log('error 발생');
//     } catch(error){
//         next(error);
//     }
 });//에러 

app.set('port', process.env.PORT||3000);
//포트를 따로 지정하지 않으면 port 값은 3000

app.use('/', express.static(path.join(__dirname,'public-3030')));

app.get('/', (req,res)=>{
res.sendFile(path.join(__dirname,'../front-end/index.html'));   
});
//__dirname 절대경로 현재위치
// app.get((err, req, res, next)=>{
//     res.status(200).send('404 Error');
// });// 에러 status 값을 변경

app.use((err,req,res,next) => {
console.log('error'); //콘솔에는 에러를 띄우고
res.send('404 Error');// 클라이언트 화면에는 이렇게 띄우기
});

app.listen(app.get('port'), () =>{
console.log('서버 실행 3000번 포트');
});
// app.get('port') port 값을 받은 후 
// 서버 열기, 열렸다면 서버 실행을 콘솔창에 출력


