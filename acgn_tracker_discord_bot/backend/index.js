import express from 'express';

let app = express();
var port = process.env.PORT || 8080;

app.get('/', (req, res) => res.send("Hello World Express"))

app.listen(port, () => console.log("Running Acgn Tracker Backend on port " + port))
