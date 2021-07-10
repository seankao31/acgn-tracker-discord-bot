import User from './userModel.js';

export const index = function (req, res) {
  User.get((err, users) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'User retrieved successfully',
      data: users
    });
  });
};

export const create = function (req, res) {
  let user = new User(req.body);

  user.save((err) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'New user created',
      data: user
    });
  });
};

export const view = function (req, res) {
  User.findById(req.params.userId, (err, user) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'User retrieved successfully',
      data: user
    });
  });
};

export const update = function (req, res) {
  User.findByIdAndUpdate(req.params.userId, req.body, (err, user) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    };
    res.json({
      status: 'success',
      message: 'User updated successfully',
      data: user  // default: document before update
    });
  });
};

const delete_ = function (req, res) {
  User.findByIdAndDelete(req.params.userId, (err, user) => {
    if (err) {
      res.json({
        status: 'error',
        message: err
      });
      return;
    }
    res.json({
      status: 'success',
      message: 'User deleted successfully',
      data: user
    });
  });
};
export { delete_ as delete };
