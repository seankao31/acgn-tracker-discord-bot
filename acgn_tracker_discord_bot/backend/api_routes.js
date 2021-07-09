import express from 'express'

import * as acgnController from './acgnController.js'

let router = express.Router()

router.get('/', (req, res) => {
  res.json({
    status: 'API is working',
    message: 'Welcome to Acgn Tracker!'
  });
});

router.route('/acgns')
  .get(acgnController.index)
  .post(acgnController.create)

router.route('/acgns/:acgnId')
  .get(acgnController.view)
  .put(acgnController.update)

export default router;
