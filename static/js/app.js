var Scatter = Vue.component('scatter', {
    props: {
        tracks: Array,
    },
    template: `<svg :width="params.tWidth" :height="params.tHeight">
                    <g id="chartGroup" :transform="'translate(' + params.mLeft + ', ' + params.mTop + ')'"></g>
                </svg>`,
    data: function() {
        return {
            x: 'tempo',
            y: 'danceability'
        }
    },
    computed: {
        params: function() {
            return {
                tWidth: window.innerWidth * 0.9,
                iWidth: window.innerWidth * 0.7,
                mLeft: window.innerWidth * 0.1,
                mRight: window.innerWidth * 0.1,
                tHeight: window.innerHeight * 0.6,
                iHeight: window.innerHeight * 0.45,
                mTop: window.innerHeight * 0.05,
                mBottom: window.innerHeight * 0.1,
            }
        },
    },
    mounted: function() {
        console.log(this.tracks);
    }
})

var Spinner = Vue.component('spinner', {
    template: `<div>
                    <h2 class="loading">Loading...</h2>
                </div>`
})

var ErrorMsg = Vue.component('error-msg', {
    template: `<div>
                    <h2 class="error">There was an error loading the data</h2>
                </div>`
})


var app = new Vue({
    el: '#app',
    components: {
        'scatter': Scatter,
        'spinner': Spinner,
        'error-message': ErrorMsg,
    },
    data: {
        tracks: [],
        loading: true,
        error: null,
    },
    created: function() {
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
})