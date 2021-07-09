import mongoose from 'mongoose';

let acgnSchema = mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  final_episode: {
    type: String,
    required: true
  }
});

let Acgn = mongoose.model('acgn', acgnSchema);
Acgn.get = function (callback, limit) {
  Acgn.find(callback).limit(limit);
};

export default Acgn
