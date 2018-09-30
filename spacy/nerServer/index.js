var express = require('express');
var app = express();
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
var ObjectID = require('mongodb').ObjectID;

const url = 'mongodb://localhost:27017';
const dbName = 'eventbrite';

var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies


// Add headers
app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', '*');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});


app.get('/events',function(req,res){

	MongoClient.connect(url,function(err,client){
		assert.equal(null,err);
		
		const db = client.db(dbName);
		const findDocuments = function(db, callback){
			const collection = db.collection('eventbrite');

			collection.find({}).toArray(function(err,docs){
				assert.equal(err,null);
				callback(docs);
			});
		};
			
		findDocuments(db,function(dados){
			res.send(dados);
		});
	});
});

app.post('/update',function(req,res){
	var dados = (req.body);

	try{
        MongoClient.connect(url,function(err,client){
            assert.equal(null,err);
			console.log(dados._id);
            const db = client.db(dbName);
            var myquery = { "_id": ObjectID(dados._id) };
            var newvalues = { $set: {details: dados.details, entityManualList: dados.entidadesNomeadasManualmente } };
            //var newvalues = { $set: {details: dados.details} };

            const collection = db.collection('eventbrite');
            collection.update(myquery,newvalues,function(err, result) {
            	console.log(result.result.nModified);
                if (err) throw err;
                res.send("OK");

            });
        });


	}
	catch(err){
		console.log(err);
		res.send(err.message);
	}

});


app.listen(3000);
