datarino = [];

function getDataGraph() {
    d3.json('https://pure-beach-44803.herokuapp.com/client/firstgraph', function (error, data) {
        datarino = data;
    })
}

function pieChart() {
    getDataGraph();
    function segColor(c) {
        return {low: "#807dba", mid: "#e08214", high: "#41ab5d"}[c];
    }

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var pC = {}, pieDim = {w: 250, h: 250};
    pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;
    var id = '#dashboard';

    // create svg for pie chart.
    var piesvg = d3.select(id).append("svg")
        .attr("width", pieDim.w).attr("height", pieDim.h).append("g")
        .attr("transform", "translate(" + pieDim.w / 2 + "," + pieDim.h / 2 + ")");

    var w = 300;
    var outerRadius = w / 2;

    // create function to draw the arcs of the pie slices.
    var arc = d3.arc()
        .outerRadius(pieDim.r - 10)
        .innerRadius(0);

    var labelArc = d3.arc()
        .outerRadius(pieDim.r - 10)
        .innerRadius(0);

    // create a function to compute the pie slice angles.
    var pie = d3.pie().sort(null).value(function (d) {
        return d.total;
    });

    // Draw the pie slices.
    piesvg.selectAll("path")
        .data(pie(datarino))
        .enter().append("path")
        .attr("d", arc)
        .each(function (d) {
            this._current = d;
        })
        .attr("fill", function (d, i) {
            return color(i);
        });

    // Utility function to be called on mouseover a pie slice.
    function mouseover(d) {
        // call the update function of histogram with new data.
        hG.update(fData.map(function (v) {
            return [v.State, v.freq[d.data.type]];
        }), segColor(d.data.type));
    }

    //Utility function to be called on mouseout a pie slice.
    function mouseout(d) {
        // call the update function of histogram with all data.
        hG.update(fData.map(function (v) {
            return [v.State, v.total];
        }), barColor);
    }

    // Animating the pie-slice requiring a custom function which specifies
    // how the intermediate paths should be drawn.
    function arcTween(a) {
        var i = d3.interpolate(this._current, a);
        this._current = i(0);
        return function (t) {
            return arc(i(t));
        };
    }

    var arcs = piesvg.selectAll("g.arc")
        .data(pie(datarino))
        .enter()
        .append("g")
        .attr("class", "arc")
        .attr("transform", "translate(" + outerRadius + ", " + outerRadius + ")");

    arcs.append("text")
        .attr("transform", function (d) {
            return "translate(" + arc.centroid(d) + ")";
        })
        .attr("text-anchor", "middle")
        .text(function (d) {
            console.log(d);
            return d.data;
        });
    return pC;
}