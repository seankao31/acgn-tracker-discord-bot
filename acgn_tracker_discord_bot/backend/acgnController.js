import Acgn from './acgnModel.js';

export const index = function (req, res) {
  Acgn.get((err, acgns) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Acgn retrieved successfully',
      data: acgns
    });
  });
};

export const create = function (req, res) {
  let acgn = new Acgn();
  acgn.title = req.body.title;
  acgn.final_episode = req.body.final_episode;

  acgn.save((err) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'New acgn created',
      data: acgn
    });
  });
};

export const view = function (req, res) {
  Acgn.findById(req.params.acgnId, (err, acgn) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'Acgn retrieved successfully',
      data: acgn
    });
  });
};
