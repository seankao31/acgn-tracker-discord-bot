import express from 'express'

let router = express.Router()

router.get('/', (req, res) => {
  res.json({
    status: 'API is working',
    message: 'Welcome to Acgn Tracker!'
  });
});

export default router;
