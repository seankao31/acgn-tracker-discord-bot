import Acgn from './acgnModel.js';

export const index = function (req, res) {
  Acgn.get((err, acgns) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
    }
    res.json({
      status: 'success',
      message: 'Acgn retrieved successfully',
      data: acgns
    });
  });
};
