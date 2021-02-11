# spotify-project

**Introduction:**
Plotify!  The project will use data collected from a collaborative playlist dataset created by the Fall/Winter 2020-21 Data Visualization Bootcamp cohort.  The aim of the project is to answer several music related questions from the dataset used.  The research findings are mostly for fun, may also be extrapolated to market research or continued work on a music application.  Initial research questions posed are:  
1.	What is the danceability distribution of songs in the playlist? 
2.	What is the energy distribution of songs in the playlist? 
3.	What is the liveness distribution of songs in the playlist?
4.	What is the music genre distribution of songs in the playlist?
5.	What is the tempo distribution of songs in the playlist?  
Datasets to be used were collected using Spotify’s collaborative playlist function:
Playlist: “Data Analysis Jamz" - https://open.spotify.com/playlist/0fCFwL8LJE99raQb1g2YvF?si=riMLWeEsTeqfAreToKI5_g
**Data Extraction using Python Library – Spotipy**
	Data was extracted using Python and Spotify’s Python library: Spotipy.  A series of successive API calls were used to pull data from Spotify.  To extract information using Spotipy, Spotify requires that a developer application be setup.  Once setup, the app will issue a Client ID and a Secret Client ID.  Similarly, a redirect URI is required to “bounce” a unique user token to be used with the API calls.  A unique playlist and user ID was required to extract the playlist and audio track information. 

JavaScript Libraries
We chose to use a Bulma page format of our project’s main page due to the variety 
of option and styles available. The page format we chose was the Bulma Hero as 
the banner container allowed us to include links for both Spotify and the playlist 
websites as well as active tabs for both the playlist and overview which shows the 
definitions of each of the objects being compared. Spotify has their color scheme 
and logo available so we were able to include each of these items on our site for 
authenticity.
We also used Vue coding for the active tabs and the checklist options for the users 
who contributed to the playlist. Using Vue for the active tabs allowed us to utilize 
only one index.html page which just fills in the lower container of the page with the 
data based upon which tab is chosen.

 