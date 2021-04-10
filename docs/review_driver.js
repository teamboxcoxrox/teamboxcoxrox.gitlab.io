var svg = d3.select("svg"),
    width = 950,
    height = width,
    margin = 30,
    diameter = width,
    centered,
    rank_sel = 5;
console.log('hello')

function processDatas(data, rank_sel) {
    var data_filter = data.filter(function (d) {return d.topic_rank <= rank_sel;})
    var data_tree = {name: "root", children: []},
        levels = ["category", "topic_name", "asin"];

    data_filter.forEach(function (d) {
        // Keep this as a reference to the current level
        var depthCursor = data_tree.children;
        // Go down one level at a time
        levels.forEach(function (property, depth) {

            // Look to see if a branch has already been created
            var index;
            depthCursor.forEach(function (child, i) {
                if (d[property] == child.name) index = i;
            });
            // Add a branch if it isn't there
            if (isNaN(index)) {
                depthCursor.push({name: d[property], children: []});
                index = depthCursor.length - 1;
            }
            // Now reference the new child array as we go deeper into the tree
            depthCursor = depthCursor[index].children;
            // This is a leaf, so add the last element to the specified branch
            if (depth === levels.length - 1) depthCursor.push({
                name: d.asin,
                value: Math.abs(d.bubble_size),
                bubble_color: d.bubble_color,
                title: d.title,
                description: d.description,
                topic_rank: d.topic_rank,
                clean_link: d.clean_link
            });
        });
    });
    return {data_filter, data_tree}
}

function draw_circles(data_filter, data_tree) {
    var colorchoices = ['#005a32','#238443','#41ab5d','#78c679','#addd8e','#d9f0a3','#f7fcb9','#ffffe5'];
    var mincolor = d3.min(data_filter, function(d){return d.bubble_color;})
    var maxcolor = d3.max(data_filter, function(d){return d.bubble_color})

    var colorscale = d3.scaleQuantize()
        .domain([mincolor,maxcolor])
        .range(colorchoices);

    root = d3.hierarchy(data_tree)
        .sum(function(d) { return d.value; })
        .sort(function(a, b) { return b.value - a.value; });

    var nodes = pack(root).descendants();

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("background", depthcolor(-1))
        .style("position", "absolute")

    svg.call(tooltip);

    var g = svg.append("g")
        .attr("transform", "translate(0, 0) scale(1)");

    var node = svg.selectAll(".node")
        .data(root.descendants().slice(1).filter(d => d.children))
        .enter().append('g')
        .attr('class','node')

    node.append("circle")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("r", d => d.r)
        .style("fill", function(d) {
            if (d.depth == 3) {return colorscale(d.data.children[0].bubble_color);}
            else {return d.children ? depthcolor(d.depth) : null;}; });

    node.append("image")
        .attr("xlink:href", function(d) {if (d.depth == 3 && d.data.children[0].topic_rank == 1) {return "../lib/staricon.svg"}})
        .attr("x", d => (d.x - d.r) )
        .attr("y", d => (d.y - d.r) )
        .attr("width", d => d.r * 2)
        .attr("height", d => d.r * 2)
        .on('mouseover', tooltip.show)
        .on("click", zoomTo);

//curved titles approach from https://www.visualcinnamon.com/2015/09/placing-text-on-arcs/
    node.append("path")
        .attr("id", function(d) {
            if (d.depth == 1) {return "path"+d.data.name;}}) //Unique id of the path
        .attr("d", function(d) {arcstart_x = d.x - d.r
                                arcstart_y = d.y
                                arcend_x = d.x + d.r
                                arcend_y = d.y
                                arc_r = d.r
                                arcstring = "M " + arcstart_x + "," + arcstart_y
                                    + " A " + arc_r + "," + arc_r + " 0 0,1 "
                                    + arcend_x + "," + arcend_y
                                if (d.depth == 1)
                                {return arcstring}})
        .style("fill", "none")
        .style("stroke", "#AAAAAA");

    node.append("text")
        .append("textPath")
        .attr("xlink:href", function(d) {if (d.depth == 1) {return "#path"+d.data.name;}})
        .style("text-anchor","middle")
        .classed("cattext", true)
        .style("font-weight", 700)
        .attr("startOffset", "50%")
        .text(function(d) {if (d.depth == 1) {return d.data.name}});

    //zooming https://bl.ocks.org/mbostock/2206590
    function zoomTo(d) {
        var x, y, k;
        console.log('ive been clicked')
        if (d && centered !== d) {
            var centroid = [d.x, d.y];
            x = centroid[0];
            y = centroid[1];
            k = 4;
            centered = d;}
        else {
            x = width / 2;
            y = height / 2;
            k = 1;
            centered = null; }

        node.transition()
            .duration(1000)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
    }

}


var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(function(d) {if (d.depth == 0) {return 25} else {return 3}});

function set_tooltip(data) {
  //  console.log(data)
    if (data.children[0].clean_link >= 50) {
        HTMLstring =  `<center><a href="http://www.amazon.com/gp/product/${data.name}" target="_blank" rel="noopener noreferrer">${data.children[0].title}</a></center>
                       <br><center></center><b>Rank: </b> ${data.children[0].topic_rank} <b>Sentiment: </b> ${Math.round(data.children[0].bubble_color * 100)} <b>Ratings: </b> ${data.children[0].value}</center>
                       <br><br></btr>${data.children[0].description} 
                ` }
    else {
        HTMLstring =  `<center>${data.children[0].title} (Discontinued)</center>
                        <br><center><b>Rank: </b> ${data.children[0].topic_rank} <b>Sentiment: </b> ${Math.round(data.children[0].bubble_color * 100)} <b>Ratings: </b> ${data.children[0].value}</center>
                        <br></btr>${data.children[0].description}
                        `}
    HTMLstring = HTMLstring.replaceAll('-1','N/A').replaceAll('nan','')
    return HTMLstring}

var tooltip = d3.tip()
    .attr('class', 'tooltip')
    .style("background",'#f0f0f0')
    .style("opacity", 0)
    .attr("margin", 0)
    .html(function(d) { if (d.depth == 3 ) {return set_tooltip(d.data); }});
;

var depthcolorchoices = ['#f7f7f7','#525252']
var depthcolor = d3.scaleLinear()
    .domain([-1, 1]) //depth count
    .range(depthcolorchoices)
    .interpolate(d3.interpolateHcl);

d3.dsv(",", "../data/products_prepped.csv", function(d) {
    return {
        asin: d.asin,
        title: d.title,
        description: d.description,
        category: d.category,
        topic_name: d.topic_name,
        topic_rank: d.topic_rank,
        bubble_color: d.bubble_color,
        bubble_size: d.bubble_size,
        clean_link: d.clean_link
    }
}).then(function(data) {
    var data_results = processDatas(data, rank_sel)
    var data_filter = data_results['data_filter']
    var data_tree = data_results['data_tree']

    draw_circles(data_filter, data_tree)

//slider https://bl.ocks.org/mtaptich/d07fe9ac3f33b03963517d6b2c17467d
    d3.select("#rank_sel").on("input", function() {
        rank_sel = +this.value;
        d3.select('#rank_val').text(rank_sel);
        var data_results = processDatas(data, rank_sel)
        var data_filter = data_results['data_filter']
        var data_tree = data_results['data_tree']
        d3.selectAll("g > *").remove()
        draw_circles(data_filter, data_tree)

// For each data row, loop through the expected levels traversing the output tree

    });

}).catch(function(error) {
    console.log(error);
}); 