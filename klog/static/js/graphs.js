function getDomain() {
    return location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
}
function pieChart() {
    function segColor(c) {
        return {low: "#807dba", mid: "#e08214", high: "#41ab5d"}[c];
    }

    d3.json(getDomain() + '/api/v1/client/countExceptions', function (error, data) {

        var color = d3.scaleOrdinal(d3.schemeCategory20);

        var pC = {}, pieDim = {w: 600, h: 600};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;
        var id = '#dashboard';

        // create svg for pie chart.
        var piesvg = d3.select(id).append("svg")
            .attr("width", 800)
            .attr("height", 800)
            .append("g")
            .attr("transform", "translate(" + (pieDim.w + 300) / 2 + "," + (pieDim.h + 300) / 2 + ")");

        var w = 0;
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
            .data(pie(data))
            .enter()
            .append("path")
            .attr("d", arc)
            .each(function (d) {
                this._current = d;
            })
            .attr("fill", function (d, i) {
                return color(i);
            });

        var arcs = piesvg.selectAll("g.arc")
            .data(pie(data))
            .enter()
            .append("g")
            .attr("class", "arc")

        arcs.append("text")
            .attr("transform", function (d) {
                var c = arc.centroid(d),
                    x = c[0],
                    y = c[1],
                    // pythagorean theorem for hypotenuse
                    h = Math.sqrt(x * x + y * y);
                console.log("translate(" + (x / h * pieDim.r) + ',' +
                    (y / h * pieDim.r) + ")");
                return "translate(" + (x / h * pieDim.r) + ',' +
                    (y / h * pieDim.r) + ")";
            })
            .attr("text-anchor", function (d) {
                // are we past the center?
                return (d.endAngle + d.startAngle) / 2 > Math.PI ?
                    "end" : "start";
            })
            .text(function (d) {
                return d.data.exception_name;
            });
        return pC;
    })
}

function lineChart() {
    var margin = {top: 50, right: 50, bottom: 50, left: 50}
        , width = window.innerWidth - margin.left - margin.right // Use the window's width
        , height = window.innerHeight - margin.top - margin.bottom; // Use the window's height

    var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%SZ");

    d3.json(getDomain() + '/api/v1/client/getExceptionsWithDateTime', function (d) {
        d.forEach(function (d) {
            d.date = parseTime(d.date);
            d.count = +d.count;
            return d;
        });
        var xScale = d3.scaleTime()
            .domain([d[0].date, d[d.length - 1].date]) // input
            .range([0, width]);// output

        var yScale = d3.scaleLinear()
            .domain([0, 2000]) // input
            .range([height, 0]); // output

        var line = d3.line()
            .x(function (d, i) {
                return xScale(d.date);
            }) // set the x values for the line generator
            .y(function (d) {
                return yScale(d.count);
            }) // set the y values for the line generator
            .curve(d3.curveMonotoneX)// apply smoothing to the line

        var svg = d3.select('#dashboard').append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

        svg.append("g")
            .attr("class", "y axis")
            .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

        svg.append("path")
            .datum(d) // 10. Binds data to the line
            .attr("class", "line") // Assign a class for styling
            .attr("d", line); // 11. Calls the line generator

    })
}

function nodeChart() {
    var svg =  d3.select('#dashboard').append("svg").attr("width", 800)
            .attr("height", 800),
        diameter = +svg.attr("width"),
        g = svg.append("g").attr("transform", "translate(2,2)"),
        format = d3.format(",d");

    var pack = d3.pack()
        .size([diameter - 4, diameter - 4]);

    d3.json(getDomain() + '/api/v1/getStructureWithExceptions', function (error, root) {
        if (error) throw error;

        root = d3.hierarchy(root)
            .sum(function (d) {
                console.log(d.size)
                return d.size;
            })
            .sort(function (a, b) {
                return b.value - a.value;
            });

        var color = d3.scaleLinear()
            .domain([-1, 0, 200])
            .range(["green", "white", "red"]);

        var node = g.selectAll(".node")
            .data(pack(root).descendants())
            .enter().append("g")
            // .attr("class", function (d) {
            //     return d.children ? "node" : "leaf node";
            // })
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

        node.append("title")
            .text(function (d) {
                return d.data.name + "\n" + format(d.value);
            });

        node.append("circle")
            .style('fill', function(d) {
                console.log(d['data']['size'] || 0)
                return color(d['data']['size'] != undefined ? d['data']['size'] : 0)
            })
            .attr("r", function (d) {
                return d.r;
            });

        node.filter(function (d) {
            return !d.children;
        }).append("text")
            .attr("dy", "0.3em")
            .text(function (d) {
                return d.data.name.substring(0, d.r / 3);
            });
    });
}
