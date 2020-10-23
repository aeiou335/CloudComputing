/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
const mongoose = require('mongoose');
const Item = require('./Item');
mongoose
  .connect(
    'mongodb+srv://admin:admin@cluster0.sz1u6.mongodb.net/test?retryWrites=true&w=majority',
    { useNewUrlParser: true }
  )
  .then(() => console.log('MongoDB Connected'))
  .catch(err => console.log(err));
exports.helloWorld = (req, res) => {
  Item.find()
    //.then(items => res.render('index', { items }))
    .then(items => res.status(200).json({items: items}))
    .catch(err => res.status(404).json({ msg: 'No items found' }));
};
