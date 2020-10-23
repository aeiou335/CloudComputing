var url = require('url');
const express = require('express');
const fetch = require('node-fetch');

const app = express();
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
  fetch("http://us-central1-turnkey-slice-293317.cloudfunctions.net/fetchData")
    .then(res => res.json())
    .then(items => {
      console.log(items.items[0].name)
      res.render('index', { items:items.items })
    })
    //.then(items => res.status(200).json({items: items}))
    .catch(err => res.status(404).json({ msg: 'No items found' }));
});

app.post('/', (req, res) => {
  console.log(typeof(req.body.name));
  const body = {name: req.body.name};
  fetch("http://us-central1-turnkey-slice-293317.cloudfunctions.net/AddData", 
  {method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'application/json' }})
  .then(result => {
    console.log(result.status)
    res.redirect('/Dashboard');
  })
  .catch(() => res.redirect('/Dashboard'));
  
});

exports.helloWorld = app;
//app.listen(3000);