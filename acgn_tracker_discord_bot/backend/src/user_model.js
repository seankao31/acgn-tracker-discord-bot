import mongoose from 'mongoose';

let userSchema = mongoose.Schema({
  discord_id: {
    type: Number,
    required: true,
    index: true,
    unique: true
  },
  discord_username: {
    type: String,
    required: true,
  }
}, {
  strict: 'throw'  // throws StrictModeError if additional field is provided
});

let User = mongoose.model('user', userSchema);
User.get = function (callback, limit) {
  User.find(callback).limit(limit);
};

export default User;
