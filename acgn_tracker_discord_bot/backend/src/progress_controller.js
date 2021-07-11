import mongoose from 'mongoose';

import Acgn from './acgn_model.js';
import Progress from './progress_model.js';

export const index = function (req, res) {
  Progress.get((err, progresses) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Progress retrieved successfully',
      data: progresses
    });
  });
};

export const findByUser = function(req, res) {
  if (req.query.acgnId) {
    findByUserAndAcgn(req, res);
    return;
  }
  if (req.query.title) {
    findByUserAndTitle(req, res);
    return;
  }
  Progress.find({
    user_id: mongoose.Types.ObjectId(req.params.userId)
  }, (err, progresses) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Progress retrieved successfully',
      data: progresses
    });
  });
};

function findByUserAndAcgn(req, res) {
  Progress.findOne({
    user_id: req.params.userId,
    acgn_id: req.query.acgnId
  }, (err, progress) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Progress retrieved successfully',
      data: progress
    });
  });
};

function findByUserAndTitle(req, res) {
  Acgn.aggregate([{
    $match: {  // search by title
      $text: {$search: req.query.title}
    }
  }, {
    $addFields: {
      title_search_score: {
        $meta: 'textScore'
      }
    }
  }, {
    $sort: {
      title_search_score: -1
    }
// for some reason this block breaks the last replaceRoot step
// should be separated into two steps as above
// apparently not mongoose's problem, because mongodb also suffer from it
//  }, {
//    $sort: {  // sort by search score
//      title_search_score: {$meta: 'textScore'}
//    }
  }, {
    $lookup: {  // join progress collection by id
      from: Progress.collection.name,
      localField: '_id',
      foreignField: 'acgn_id',
      as: 'progresses'
    }
  }, {
    $match: {  // filter user id
      progresses: {
        $elemMatch: {
          user_id: mongoose.Types.ObjectId(req.params.userId)
        }
      }
    }
  }, {  // deconstruct progresses, output one document for each progress
    $unwind: {
      path: '$progresses'
    }
  }, {
    $replaceRoot: {  // return progresses
      newRoot: '$progresses'
    }
  }], (err, progresses) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Progress retrieved successfully',
      data: progresses
    });
  });
};

export const create = function (req, res) {
  let progress = new Progress(req.body);

  progress.save((err) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'New progress created',
      data: progress
    });
  });
};

export const view = function (req, res) {
  Progress.findById(req.params.progressId, (err, progress) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Progress retrieved successfully',
      data: progress
    });
  });
};

export const update = function (req, res) {
  Progress.findByIdAndUpdate(req.params.progressId, req.body, (err, progress) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    };
    res.json({
      status: 'success',
      message: 'Progress updated successfully',
      data: progress  // default: document before update
    });
  });
};

const delete_ = function (req, res) {
  Progress.findByIdAndDelete(req.params.progressId, (err, progress) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Progress deleted successfully',
      data: progress
    });
  });
};
export { delete_ as delete };
