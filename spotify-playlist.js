var request = require('request');
var user_id = "1221063701";
var token = "Bearer BQDyMmKkkKZ2vJrpz2jvKaKpA3gJFCCzW-TLOna3ykWJAGycFr3pCtAJ3P2RWcRZTDTo7GooINu6OJhneaoGMaO5jiF2pEUY3vj1EuMjSfFHRWJ7MLt1gPzNNl3eIoc0JuiWRaVKKIPWj2IYNQ"
var playlists_url = "https://api.spotify.com/v1/users/"+user_id+"/playlists";

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

