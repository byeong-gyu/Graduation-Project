const express =require("express");
const app = express();
const home = require("./routes/home");
//앱 세팅
app.set("views", "./views");
app.set("view engine","ejs");


app.use("/", home);//미들 웨어를 등록해주는 서비스

module.exports=app;




