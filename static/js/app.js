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
        playlistActive: true,
        overviewActive: false,
        axes: ['acousticness', 'danceability', 'energy', 'instrumentalness', 'length',
            'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'time_signature'],
        users: [
            {id: '1221063701', name: 'Charles Stephens', color: '#92DCE5', active: true},
            {id: '1213961138', name: 'Tempest Campbell', color: '#D64933', active: true},
            {id: 'kukulski.2', name: 'Matt Kukulski', color: '#7D70BA', active: true},
            {id: '1256631666', name: 'Stu Yates', color: '#f1d302', active: true},
            {id: '1239315253', name: 'John Edward Shuford', color: '#ace4aa', active: true},
            {id: '5x3jsdd20gyv86pg2naw63zwp', name: 'Pauly Richmeier', color: '#f84aa7', active: true}
        ],
        loading: true,
        error: null,
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
        },
        toggleUser: function (id) {
            const userIndex = this.users.indexOf(user => user.id === id);
            this.users[userIndex].active = !this.users[userIndex].active;
        }
    },
    created: function () {
        d3.json('http://127.0.0.1:5000/data')
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