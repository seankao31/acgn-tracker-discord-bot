import Acgn from './acgn_model.js';

export const index = function (req, res) {
  if (req.query.title) {
    search(req, res);
    return;
  }
  Acgn.get((err, acgns) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(acgns);
  });
};

export const create = function (req, res) {
  let acgn = new Acgn(req.body);

  acgn.save((err) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(acgn);
  });
};

function search(req, res) {
  Acgn.find({
    $text: {$search: req.query.title}
  }, {
    title_search_score: {$meta : 'textScore'}
  })
    .sort({title_search_score: {$meta: 'textScore'}})
    .exec((err, acgns) => {
      if (err) {
        res.status(400).send(err);
        return;
      }
      res.json({
        status: 'success',
        message: 'Acgn retrieved successfully',
        data: acgns
      });
    });
};

export const view = function (req, res) {
  Acgn.findById(req.params.acgnId, (err, acgn) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.json({
      status: 'success',
      message: 'Acgn retrieved successfully',
      data: acgn
    });
  });
};

export const update = function (req, res) {
  Acgn.findByIdAndUpdate(req.params.acgnId, req.body, (err, acgn) => {
    if (err) {
      res.status(400).send(err);
      return;
    };
    res.json({
      status: 'success',
      message: 'Acgn updated successfully',
      data: acgn  // default: document before update
    });
  });
};

const delete_ = function (req, res) {
  Acgn.findByIdAndDelete(req.params.acgnId, (err, acgn) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(acgn);
  });
};
export { delete_ as delete };
