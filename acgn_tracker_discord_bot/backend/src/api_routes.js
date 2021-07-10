import express from 'express'

import * as acgnController from './acgn_controller.js'
import * as userController from './user_controller.js'
import * as progressController from './progress_controller.js'

let router = express.Router()

router.get('/', (req, res) => {
  res.json({
    status: 'API is working',
    message: 'Welcome to Acgn Tracker!'
  });
});

router.route('/acgns')
  .get(acgnController.index)  // also accepts query: title
  .post(acgnController.create)

router.route('/acgns/:acgnId')
  .get(acgnController.view)
  .put(acgnController.update)
  .delete(acgnController.delete)

router.route('/users')
  .get(userController.index)
  .post(userController.create)

router.route('/users/:userId')
  .get(userController.view)
  .put(userController.update)
  .delete(userController.delete)

router.route('/users/:userId/progresses')
  .get(progressController.findByUser)  // also accepts query: title

router.route('/progresses')
  .get(progressController.index)
  .post(progressController.create)

router.route('/progresses/:progressId')
  .get(progressController.view)
  .put(progressController.update)
  .delete(progressController.delete)

export default router;
