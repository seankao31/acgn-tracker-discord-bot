import Progress from './progressModel.js';

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