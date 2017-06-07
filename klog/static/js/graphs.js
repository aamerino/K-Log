
function getDataGraph(callback) {
    d3.json('http://localhost:8000/client/firstgraph', function (error, data) {
        datarino = data;
        callback(data);
    })
}

function pieChart(datarino) {
    function segColor(c) {
        return {low: "#807dba", mid: "#e08214", high: "#41ab5d"}[c];
    }

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var pC = {}, pieDim = {w: 600, h: 600};
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
            return "translate(" + labelArc.centroid(d) + ")";
        })
        .attr("text-anchor", "middle")
        .text(function (d) {
            console.log(d.data.exception_name);
            return d.data.exception_name;
        });
    return pC;
}

function lineChart() {
    var svg = d3.select("svg"),
        margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var parseTime = d3.timeParse("%d-%b-%y");

    var x = d3.scaleTime()
        .rangeRound([0, width]);

    var y = d3.scaleLinear()
        .rangeRound([height, 0]);

    var line = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.close); });

    d3.tsv("data.tsv", function(d) {
        d.date = parseTime(d.date);
        d.close = +d.close;
        return d;
    }, function(error, data) {
        if (error) throw error;

        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain(d3.extent(data, function(d) { return d.close; }));

        g.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))
            .select(".domain")
            .remove();

        g.append("g")
            .call(d3.axisLeft(y))
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Price ($)");

        g.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 1.5)
            .attr("d", line);
    });
}