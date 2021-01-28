var request = require('request');
var user_id = "1221063701";
var token = "Bearer BQDyMmKkkKZ2vJrpz2jvKaKpA3gJFCCzW-TLOna3ykWJAGycFr3pCtAJ3P2RWcRZTDTo7GooINu6OJhneaoGMaO5jiF2pEUY3vj1EuMjSfFHRWJ7MLt1gPzNNl3eIoc0JuiWRaVKKIPWj2IYNQ"
var playlists_url = "https://api.spotify.com/v1/users/"+user_id+"/playlists";


var svgWidth = 800;
var svgHeight = 600;

var margin = {
  top: 20,
  right: 40,
  bottom: 100,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
var svg = d3.select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);


request({url:playlists_url, headers:{"Authorization":token}}, function(err, res){
	if (res){
		var playlists=JSON.parse(res.body);	
		var playlist_url = playlists.items[0].href;
		request({url:playlist_url, headers:{"Authorization":token}}, function(err, res){
			if (res){
				var playlist = JSON.parse(res.body);
				console.log("playlist: " + playlist.name);
				playlist.tracks.items.forEach(function(track){
					console.log(track.track.name);
				});
			}
		})		
	}
})

