import express from 'express';
import mongoose from 'mongoose';

import apiRoutes from './api_routes.js';

let app = express();

app.use(express.urlencoded({
  extended: true
}));
app.use(express.json());

// Deprecations: https://mongoosejs.com/docs/deprecations.html
mongoose.set('useNewUrlParser', true);
mongoose.set('useUnifiedTopology', true);
mongoose.set('useFindAndModify', false);
mongoose.set('useCreateIndex', true);  // THIS. with this my compound unique index finally works

let mongodbUri = process.env.MONGODB_URI || 'mongodb://localhost:27017/acgn_tracker';
mongoose.connect(mongodbUri);
let db = mongoose.connection;
if (!db)
    console.log('Error connecting db');
else
    console.log('Db connected successfully');

let port = process.env.PORT || 8080;
app.get('/', (req, res) => res.send('Hello World Express'));
app.use('/api', apiRoutes);

app.listen(port, () => {
  console.log('Running Acgn Tracker Backend on port ' + port);
});
