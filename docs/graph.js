d3.dsv(",", "board_games.csv", function(d) {
    return {
        source: d.source,
        target: d.target,
        value: +d.value
    }
}).then(function(data) {

    var def_size = 4
    var colorchoices = ['#dadaeb','#bcbddc','#9e9ac8','#807dba','#6a51a3','#4a1486'];


    var links = data;

    var nodes = {};

    // compute the distinct nodes from the links.
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
    });

    var width = 1200,
        height = 700;

    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(100))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-250))
        .alphaTarget(1)
        .on("tick", tick);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var gtusername = svg.append("text")
        .attr("x", width - 300)
        .attr("y", 20)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .text("kmatisko3");

    // add the links
    var path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("class", function(d) { return "link " + d.type; });

    // define the nodes
    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")
        .on("dblclick", unpin)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    //I originally used a node counting code from StackOverflow: https://stackoverflow.com/questions/54471028/how-can-i-calculate-the-degree-of-nodes-in-d3-v5
    //After reading the policy on StackOverflow on piazza, I realized I used the code inappropriately, removed that portion and redid it
    //I'm sourcing it here in the interest of transparency and because my final structure may still have similarities to the StackOverflow code because I need the same final variables to feed the next portion of the code

//    console.log(links)
    links.forEach(d => {d.source.degree = 0})
    links.forEach(d => {d.source.degree = d.source.degree + 1})
    links.forEach(d => {d.target.degree = 0})
    links.forEach(d => {d.target.degree = d.target.degree + 1})

  //  console.log(links)
    var sourcedegrees = links.map(function(d) { return d.source.degree; });
    var targetdegrees = links.map(function(d) { return d.target.degree; });
    var degreevals = sourcedegrees.concat(targetdegrees)
 //   console.log(d3.extent(degreevals))
 //   console.log(links)

    var nodescale = d3.scaleSqrt()
        .domain(d3.extent(degreevals))
        .range([def_size,def_size*4])

    var colorscale = d3.scaleQuantile()
        .domain(d3.extent(degreevals))
        .range(colorchoices);

    // add the nodes
    node.append("circle")
            .attr("r", function(d) {return nodescale(d.degree) || def_size })
            .style("fill", function(d) {return colorscale(d.degree); });

    // add the titles
    node.append("text")
        .attr("dx", function(d) {return (nodescale(d.degree) + 2) || 6 })
        .attr("dy", -5)
        .style("font-weight", 700)
        .text(function(d) { return d.name});

    // add the curvy lines
    function tick() {
        path.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        })
            .style("stroke",function(d) {if (d.value == 0) {return "gray"} else {return "green"}})
            .style("stroke-width", function(d) {if (d.value == 0) {return '5px'} else {return '2px'}})
            .style("stroke-dasharray", function(d) {if (d.value != 0) {return ("3,3")}});

        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    };

    function dragstarted(d) {
        if (!d3.event.active) force.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
        d.fixed = true;
   //     console.log(d.name + " : you dragged me!")
    };

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
   //     console.log(d.name + " : I was dragged! arrrgghhh")
    };

    function dragended(d) {
        if (!d3.event.active) force.alphaTarget(0);
        if (d.fixed == true) {
            d.fx = d.x;
            d.fy = d.y;
    //        console.log(d.name + " : You stopped dragging me!  Thank you.  I am fixed now")
            d3.select(this)
                .select("circle")
                .style("fill","#2ca25f");

        }
        else {
            d.fx = null;
            d.fy = null;
   //         console.log(d.name + " : I am no longer fixed")
        }
    };

    function unpin(d) {
        if (!d3.event.active) force.alphaTarget(0.3).restart();
        d3.select(this)
            .select("circle")
            .style("fill", function(d) {return colorscale(d.degree); });
        d.fixed = false;
        d.fx = null;
        d.fy = null;
   //     console.log(d.name + " : Thank you for unpinning me.  I am free!")
    };


}).catch(function(error) {
    console.log(error);
});