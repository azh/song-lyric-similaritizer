const Lyricist = require('lyricist/node6');
const https = require('https');
const fs = require('fs');

var visited = {}

async function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function getLyrics(id) {
	var element = {};
	client_token = 'vRRj7jEa5AFK0ukuJjUVEzhl9sBIEP-Uwg-9tkpyrh3thEzJQflkbhIx_fAOADSI';
const lyricist = new Lyricist(client_token);
let uri = 'https://api.genius.com/referents?access_token=' + 
	client_token + '&song_id=' + id;

var req = https.get(uri, (res) => {
  	var output = '';
  	res.on('data', function (chunk) {
        output += chunk;
    });

    res.on('end', function() {
        var obj = JSON.parse(output);
        var str = '';
	try{
		for (let l = 0; l < obj.response.referents.length;l++){ 
			str += obj.response.referents[l].annotations[0].body.dom.children[0].children[0];
		}
		element['annotations'] = str;
	}
	catch(e) {
		// do nothing
		console.log("bad object");
	}
  	});
  	req.on('error', function(err) {
        console.log('invalid id');
    });
  	req.end();
	});
	try {
		song = await lyricist.song(id, { fetchLyrics: true });
	} catch(err){
		console.log('invalid id');
	}
	element['lyrics'] = song.lyrics;
	element['id'] = id;

	fs.appendFileSync('./songData.json', JSON.stringify(element, null, '\t'),'utf8');
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

async function run(){
	while(true){
	let id = getRandomInt(80000)
	if (visited[id] == undefined){
		var pointless = await Promise.all([getLyrics(id), timeout(1000)]);
		}
	}
}

run();