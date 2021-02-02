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
        axes: ['acousticness', 'danceability', 'energy', 'instrumentalness', 'length',
            'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'time_signature'],
        users: [],
        loading: true,
        error: null,
    },
    methods: {
        toTitleCase: function (string) {
            return string.split('_')
                .map(word => word.charAt(0).toUpperCase() + word.substr(1))
                .join(' ');
        },
    },
    computed: {
        colorCodes: function () {
            const colors = ['#92DCE5', '#D64933', '#7D70BA', '#f1d302', '#ace4aa', '#f84aa7'];
            const colorCodes = {};
            this.users.forEach((user, index) => colorCodes[user] = colors[index]);
            console.log(colorCodes)
            return colorCodes;
        }
    },
    created: function () {
        d3.json('http://127.0.0.1:5000/data')
            .then(data => {
                this.tracks = data;
                this.loading = false;
                this.users = [...new Set(data.map(track => track.user_id))];
                console.log(this.users);
            })
            .catch(err => {
                this.error = err;
                this.loading = false;
            });
    }
});