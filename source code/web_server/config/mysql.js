const mysql = require('mysql2');
const dotenv = require('dotenv');

dotenv.config();

const db = mysql.createConnection({
    host     : process.env.DB_HOST,
    user     : process.env.DB_USER,
    password : process.env.DB_PASSWORD,
    database : process.env.DB
});
db.connect((error, result) => {
    if(error){
        console.log(error);
    } else {
        console.log('db connected');
    }
});
module.exports = db;
db.end();
