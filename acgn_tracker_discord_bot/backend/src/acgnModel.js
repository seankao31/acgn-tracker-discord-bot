import mongoose from 'mongoose';

let acgnSchema = mongoose.Schema({
  title: {
    type: String,
    required: true,
    unique: true
  },
  final_episode: {
    type: String,
    required: true
  }
}, {
  strict: 'throw'  // throws StrictModeError if additional field is provided
});

let Acgn = mongoose.model('acgn', acgnSchema);
Acgn.get = function (callback, limit) {
  Acgn.find(callback).limit(limit);
};

export default Acgn
