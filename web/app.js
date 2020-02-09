const express = require('express');

const mongoose = require('mongoose');
const passport = require('passport');
const flash = require('connect-flash');
const session = require('express-session');
const app = express();  
 
const  PORT = process.env.PORT || 3000;

//Passport config
require('./config/passport')(passport);

//DB config
const db = require("./config/keys").MongoURI;

//Connect to MongoDB
mongoose.connect(db, {useNewUrlParser: true})
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.log(err));

//EJS

app.set("view engine", "ejs");

// Express body parser
app.use(express.urlencoded({ extended: true }));
//Some stuff


////////// PASSPORT CONFIGURATION //////////

//Express session
app.use(
    session({
      secret: 'secret',
      resave: true,
      saveUninitialized: true
    })
  );

// Passport middleware
app.use(passport.initialize());
app.use(passport.session());

//connect flash
app.use(flash());

//Global Variables
app.use(function(req, res, next){
    res.locals.currentUser = req.user;
    res.locals.success_msg = req.flash('success_msg');
    res.locals.error_msg = req.flash('error_msg');
    res.locals.error = req.flash('error');
    next();
});

////////// Routes //////////

app.use('/', require('./routes/index.js'));
app.use('/users', require('./routes/users.js'));


// listen
app.listen(PORT, console.log(`Server started on port ${PORT}`));






