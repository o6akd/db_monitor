const express = require('express');
const router = express.Router();
// KAMILS variables
var formidable = require('formidable');
let {PythonShell} = require('python-shell')
var fs = require("fs");
var clientFile = 'empty';


// Welcome Page
router.get('/', (req, res) => {
  res.render('index');
});

router.get('/data',function(req, res) {
    console.log('clientfile '+clientFile);
    let options = {
      mode: 'text',
      args: [__dirname + '/../uploads/' + 'client.csv']
    };
    PythonShell.run(__dirname + '/../engines/script.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution
      console.log('results: %j', results);
      res.json(results);
    });
  });
  
  router.post('/upload', function (req, res){
      var form = new formidable.IncomingForm();
  
      form.parse(req);
  
      form.on('fileBegin', function (name, file){
          file.path = __dirname + '/../uploads/' + 'client.csv';
          clientFile = file.path;
      });
  
      form.on('file', function (name, file){
          console.log('Uploaded ' + file.path);
      });
      //res.sendFile(__dirname + '/client/index_data.html'); //invalid now
      res.status(200).json('success');
  });

module.exports = router;