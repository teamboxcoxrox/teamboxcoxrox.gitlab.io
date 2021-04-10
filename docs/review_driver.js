var svg = d3.select("svg"),
    width = 900,
    height = 500,
    margin = 20,
    diameter = width;

var color = d3.scaleLinear()
    .domain([-1, 1])
    .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
    .interpolate(d3.interpolateHcl);

var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(2);

d3.dsv(",", "mock_main_df.csv", function(d) {
    return {
        asin: d.asin,
        description: d.description,
        topic: d.topic,
        topic_description: d.topic_description,
        sentiment: d.sentiment,
        quantile: d.quantile
    }
}).then(function(data) {
    console.table(data)
    console.log('made it')


 //   let topics = [...new Set(data.map(d => d.topic_description))];
    var newData = { name :"root", children : [] },
        levels = ["topic_description","asin"];

// For each data row, loop through the expected levels traversing the output tree
    data.forEach(function(d){
        // Keep this as a reference to the current level
        var depthCursor = newData.children;
        // Go down one level at a time
        levels.forEach(function( property, depth ){

            // Look to see if a branch has already been created
            var index;
            depthCursor.forEach(function(child,i){
                if ( d[property] == child.name ) index = i;
            });
            // Add a branch if it isn't there
            if ( isNaN(index) ) {
                depthCursor.push({ name : d[property], children : []});
                index = depthCursor.length - 1;
            }
            // Now reference the new child array as we go deeper into the tree
            depthCursor = depthCursor[index].children;
            // This is a leaf, so add the last element to the specified branch
            if ( depth === levels.length - 1 ) depthCursor.push({ name : d.description, value : Math.abs(d.sentiment) }); // d.sentiment
        });
    });

  console.log(newData)

 // var hierarchy = d3.hierarchy(newData).sum(function(d){ return d.value; }

    root = d3.hierarchy(newData)
        .sum(function(d) { return d.value; })
        .sort(function(a, b) { return b.value - a.value; });

console.log(root)

    var focus = root,
        nodes = pack(root).descendants(),
        view;

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("background", color(-1))
        .on("click", function() { zoom(root); });

    var node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("g")
        .attr("dx", function(d) {return d.x})
        .attr("dy", function(d) {return d.y})
        .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); });

    node.append("circle")
        .attr("r", function(d) {return d.r})
        .attr("dx", 0)
        .attr("dy", 0)
        .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
        .style("fill", function(d) { return d.children ? color(d.depth) : null; })


 //   var text = svg.selectAll("text")
  //      .data(nodes)
  //      .enter().append("text")
  //      .attr("class", "label")
  //      .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
  //      .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
  //      .text(function(d) { return d.data.name; });

   // var node = svg.selectAll("circle,text");


    zoomTo([root.x, root.y, root.r * 2 + margin]);

    function zoom(d) {
        var focus0 = focus; focus = d;

        var transition = d3.transition()
            .duration(d3.event.altKey ? 7500 : 750)
            .tween("zoom", function(d) {
                var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
                return function(t) { zoomTo(i(t)); };
            });

        transition.selectAll("text")
            .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
            .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
            .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
            .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
    }

    function zoomTo(v) {
        var k = diameter / v[2]; view = v;
        node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
        node.attr("r", function(d) { return d.r * k; });
    }


}).catch(function(error) {
    console.log(error);
});