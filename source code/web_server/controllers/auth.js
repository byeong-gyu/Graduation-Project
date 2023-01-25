const mysql = require('mysql2');
const jwt= require('jsonwebtoken');
const bcrypt = require('bcrypt');

const db = mysql.createConnection({
    host     : process.env.DB_HOST,
    user     : process.env.DB_USER,
    password : process.env.DB_PASSWORD,
    database : process.env.DB
});

exports.join=(req,res) => {
    console.log(req.body);

    const { userID, userPassID, userName, userGender, userEmail, userCode } = req.body;


    db.query('SELECT userID FROM users WHERE userID = ?' ,[userID], async (error, results)=>{
        if(error) {
            console.log(error)
        }

        if( results.length > 0){
            return res.render('../../front-end/join', {
                msg: 'exist ID'
            })
        } 

        let hashedPassword = await bcrypt.hash(userPassID, 12);
        console.log(hashedPassword);

        db.query('INSERT INTO users SET ?', {userID, userPassID, userName, userGender, userEmail, userCode}, (error, results) => {
            if(error){
                console.log(error);
            } else{
                return res.render('../../front-end/login', {
                    message: 'user registered'
                });
            }
    })
    }) ;
}