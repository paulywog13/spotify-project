var Scatter = Vue.component('scatter', {
    props: {
        tracks: Array,
        x: String,
        y: String,
    },
    template: `<svg :width="params.tWidth" :height="params.tHeight" class="has-background-dark has-text-white">
                    <g class="chart-group" :transform="'translate(' + params.mLeft + ', ' + params.mTop + ')'">
                          <g class="x-axis" :transform="'translate(0, ' + params.iHeight + ')'"></g>
                          <g class="y-axis"></g>
                          <text class="x-label"
                                stroke="lightgrey"
                                text-anchor="middle"
                                :x="params.iWidth / 2"
                                :y="params.iHeight + params.mBottom / 2">
                          {{ toTitleCase(x) }}</text>
                          <text class="y-label" 
                                stroke="lightgrey"
                                text-anchor="middle"
                                transform="rotate(-90)"
                                :x="0 - (params.iHeight / 2)"
                                :y="0 - params.mLeft"
                                dy="2em">
                          {{ toTitleCase(y) }}</text>
                    </g>
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
                .domain([d3.min(data, d => d[this[axis]]) * (1 - offset),
                    d3.max(data, d => d[this[axis]]) * (1 + offset)])
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
                .attr(`c${axis}`, d => scale(d[this[axis]]));
            circlesGroup.selectAll('text')
                .transition()
                .duration(500)
                .attr(axis, d => scale(d[this[axis]]));
        },
        toTitleCase: function (string) {
            return string.split('_')
                .map(word => word.charAt(0).toUpperCase() + word.substr(1))
                .join(' ');
        },
    },
    mounted: function() {
        const chartGroup = d3.select('.chart-group');

        let xScale = this.linearScale('x', this.tracks);
        let yScale = this.linearScale('y', this.tracks);

        let xAxis = d3.select('.x-axis')
            .call(d3.axisBottom(xScale));
        let yAxis = d3.select('.y-axis')
            .call(d3.axisLeft(yScale));

        const circlesGroup = chartGroup.selectAll('circle')
            .data(this.tracks)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d[this.x]))
            .attr('cy', d => yScale(d[this.y]))
            .attr('fill', 'grey')
            .attr('stroke', 'lightgrey')
            .attr('r', 5);
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