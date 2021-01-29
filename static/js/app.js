var Scatter = Vue.component('scatter', {
    props: {
        tracks: Array,
        selected: Object,
    },
    template: `<svg :width="params.tWidth" :height="params.tHeight">
                    <g id="chartGroup" :transform="'translate(' + params.mLeft + ', ' + params.mTop + ')'"></g>
                </svg>`,
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
    methods: {
        linearScale: function(axis, data) {
            const offset = axis === 'x' ? 0.05 : 0.2;
            return d3.scaleLinear()
                .domain([d3.min(data, d => d[this.selected[axis]]) * (1 - offset),
                    d3.max(data, d => d[this.selected[axis]]) * (1 + offset)])
                .range(axis === 'x' ? [0, this.params.iWidth] : [this.params.iHeight, 0]);
        },
        renderAxis: function(axis, axisObj, scale) {
            return axisObj.transition()
                .duration(500)
                .call(axis === 'x' ? d3.axisBottom(scale) : d3.axisLeft(scale));
        },
        renderCircles: function(circlesGroup, scale, axis) {
            circlesGroup.selectAll('circle')
                .transition()
                .duration(500)
                .attr(`c${axis}`, d => scale(d[this.selected[axis]]));
            circlesGroup.selectAll('text')
                .transition()
                .duration(500)
                .attr(axis, d => scale(d[this.selected[axis]]));
        },
    },
    mounted: function() {
        const chartGroup = d3.select('#chartGroup');
        let xScale = this.linearScale('x', this.tracks);
        let xAxis = chartGroup.append('g')
            .classed('x-axis', true)
            .attr('transform', `translate(0, ${this.params.iHeight})`)
            .call(d3.axisBottom(xScale));
        let yScale = this.linearScale('y', this.tracks);
        let yAxis = chartGroup.append('g')
            .classed('y-axis', true)
            .call(d3.axisLeft(yScale));

        const circlesGroup = chartGroup.selectAll('circle')
            .data(this.tracks)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d[this.selected.x]))
            .attr('cy', d => yScale(d[this.selected.y]))
            .attr('r', 10);
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
        selected: {
          x: 'tempo',
          y: 'danceability',
        },
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