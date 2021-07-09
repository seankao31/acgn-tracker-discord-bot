import express from 'express';

import api_routes from './api_routes.js';


let app = express();
var port = process.env.PORT || 8080;

app.get('/', (req, res) => res.send("Hello World Express"))
app.use('/api', api_routes)

app.listen(port, () => console.log("Running Acgn Tracker Backend on port " + port))
