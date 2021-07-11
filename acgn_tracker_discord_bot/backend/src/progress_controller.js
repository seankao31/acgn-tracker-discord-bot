import mongoose from 'mongoose';

import Acgn from './acgn_model.js';
import Progress from './progress_model.js';

export const index = function (req, res) {
  Progress.get((err, progresses) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(progresses);
  });
};

export const findByUser = function(req, res) {
  if (req.query.title) {
    findByUserAndTitle(req, res);
    return;
  }
  Progress.find({
    user_id: mongoose.Types.ObjectId(req.params.userId)
  }, (err, progresses) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(progresses);
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
      res.status(400).send(err);
      return;
    }
    res.status(200).send(progresses);
  });
};

export const create = function (req, res) {
  let progress = new Progress(req.body);

  progress.save((err) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(progress);
  });
};

export const view = function (req, res) {
  Progress.findById(req.params.progressId, (err, progress) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(progress);
  });
};

export const update = function (req, res) {
  Progress.findByIdAndUpdate(req.params.progressId, req.body, (err, progress) => {
    if (err) {
      res.status(400).send(err);
      return;
    };
    res.status(200).send(progress);
  });
};

const delete_ = function (req, res) {
  Progress.findByIdAndDelete(req.params.progressId, (err, progress) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(progress);
  });
};
export { delete_ as delete };
