const app = new Vue({
    el: '#app',
    delimiters: ['{(', ')}'],
    components: {
        'scatter': Scatter,
        'spinner': Spinner,
        'error-message': ErrorMsg,
    },
    data: {
        x: 'tempo',
        y: 'danceability',
        tracks: [],
        user: '1221063701',
        track: null,
        playlistActive: true,
        overviewActive: false,
        predictorActive: false,
        recommendationsActive: false,
        genreActive: false,
        submissionError: null,
        axes: ['acousticness', 'danceability', 'energy', 'instrumentalness', 'length',
            'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'time_signature'],
        users: [
            {id: '1221063701', name: 'Charles Stephens', color: '#92DCE5', selected: true},
            {id: '1213961138', name: 'Tempest Campbell', color: '#D64933', selected: true},
            {id: 'kukulski.2', name: 'Matt Kukulski', color: '#7D70BA', selected: true},
            {id: '1256631666', name: 'Stu Yates', color: '#f1d302', selected: true},
            {id: '1239315253', name: 'John Edward Shuford', color: '#ace4aa', selected: true},
            {id: '5x3jsdd20gyv86pg2naw63zwp', name: 'Pauly Richmeier', color: '#f84aa7', selected: true}
        ],
        loading: true,
        error: null,
    },
    computed: {
        selectedUsers: function () {
            return this.users.filter(user => user.selected);
        },
        userTracks: function () {
            return this.tracks.filter(track => track.info.user_id === this.user)
        }
    },
    methods: {
        toTitleCase: function (string) {
            return string.split('_')
                .map(word => word.charAt(0).toUpperCase() + word.substr(1))
                .join(' ');
        },
        changeActive: function (me) {
            this.playlistActive = me === 'playlist';
            this.overviewActive = me === 'overview';
            this.predictorActive = me === 'predictor';
            this.recommendationsActive = me === 'recommendations';
            this.genreActive = me === 'genre';
        },
        toggleUser: function (id) {
            const userIndex = this.users.indexOf(user => user.id === id);
            this.users[userIndex].selected = !this.users[userIndex].selected;
        },
        getRecommendations: function () {
            fetch('/recommend?track_id=' + this.track)
                .then(res => console.log(res))
                .catch(err => this.submissionError = err)
        }
    },
    created: function () {
        d3.json('/data')
            .then(data => {
                this.tracks = data;
                this.loading = false;
            })
            .catch(err => {
                this.error = err;
                this.loading = false;
            });
    }
});

