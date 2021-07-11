import User from './user_model.js';

export const index = function (req, res) {
  if (req.query.discord_id) {
    search(req, res);
    return;
  }
  User.get((err, users) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(users);
  });
};

function search(req, res) {
  User.findOne(req.query, (err, user) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(user);
  });
};

export const create = function (req, res) {
  let user = new User(req.body);

  user.save((err) => {
    if (err) {
      res.status(400).send(err)
      return;
    }
    res.status(200).send(user);
  });
};

export const view = function (req, res) {
  User.findById(req.params.userId, (err, user) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(user);
  });
};

export const update = function (req, res) {
  User.findByIdAndUpdate(req.params.userId, req.body, (err, user) => {
    if (err) {
      res.status(400).send(err);
      return;
    };
    res.status(200).send(user);
  });
};

const delete_ = function (req, res) {
  User.findByIdAndDelete(req.params.userId, (err, user) => {
    if (err) {
      res.status(400).send(err);
      return;
    }
    res.status(200).send(user);
  });
};
export { delete_ as delete };
