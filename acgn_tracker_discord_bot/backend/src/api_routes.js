import express from 'express'

import * as acgnController from './acgnController.js'
import * as progressController from './progressController.js'

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
  .delete(acgnController.delete)

router.route('/progresses')
  .get(progressController.index)
  .post(progressController.create)

router.route('/progresses/:progressId')
  .get(progressController.view)
  .put(progressController.update)
  .delete(progressController.delete)

export default router;
