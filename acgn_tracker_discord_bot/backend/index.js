import express from 'express';
import mongoose from 'mongoose';

import apiRoutes from './api_routes.js';


let app = express();

app.use(express.urlencoded({
  extended: true
}));
app.use(express.json());

let mongodbUri = process.env.MONGODB_URI || 'mongodb://localhost:27017/acgn_tracker';
mongoose.connect(mongodbUri, {useNewUrlParser: true, useUnifiedTopology: true});
let db = mongoose.connection;
if(!db)
    console.log("Error connecting db");
else
    console.log("Db connected successfully");

let port = process.env.PORT || 8080;
app.get('/', (req, res) => res.send('Hello World Express'));
app.use('/api', apiRoutes);

app.listen(port, () => {
  console.log('Running Acgn Tracker Backend on port ' + port);
});
