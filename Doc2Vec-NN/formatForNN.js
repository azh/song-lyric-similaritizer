var fs = require('fs');

var d = fs.readFileSync('songData.json');

var list = [];

dj = JSON.parse(d);