import mongoose from 'mongoose';

let progressSchema = mongoose.Schema({
  user_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'user',
    required: true,
    index: true
  },
  acgn_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'acgn',
    required: true
  },
  episode: {
    type: String,
    required: true
  }
}, {
  strict: 'throw'  // throws StrictModeError if additional field is provided
});
progressSchema.index({user_id: 1, acgn_id: 1}, {unique: true});

let Progress = mongoose.model('progress', progressSchema);
Progress.get = function (callback, limit) {
  Progress.find(callback).limit(limit);
};

export default Progress;
