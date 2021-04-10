console.log('hello')
var svg = d3.select("svg"),
    width = 950,
    height = width,
    margin = 30,
    diameter = width;

var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(3);

function set_tooltip(data) {
    console.log(data)
    var HTMLstring =  `<a href="http://www.amazon.com/gp/product/${data.name}" target="_blank" rel="noopener noreferrer">${data.children[0].title}</a>
                       <br><b>Rank: </b> ${data.children[0].topic_rank} <b>Sentiment: </b> ${data.children[0].bubble_color} <b>Ratings: </b> ${data.children[0].value}
                       <br>${data.children[0].description} 
                `
    HTMLstring = HTMLstring.replaceAll('-1','N/A')
    return HTMLstring}

var tooltip = d3.tip()
    .attr('class', 'd3-tip')
    .style("background",'#f0f0f0')
    .style("opacity", 0)
    .attr("width", 200)
    .html(function(d) { if (d.depth == 3) {return set_tooltip(d.data); }})
;

var depthcolorchoices = ['#f7f7f7','#525252']
var depthcolor = d3.scaleLinear()
    .domain([-1, 1]) //depth count
    .range(depthcolorchoices)
    .interpolate(d3.interpolateHcl);

d3.dsv(",", "../data/products_4.9 - filter.csv", function(d) {
    return {
        asin: d.asin,
        title: d.title,
        description: d.description,
        category: d.category,
        topic_name: d.topic_name,
        topic_rank: d.topic_rank,
        bubble_color: d.bubble_color,
        bubble_size: d.bubble_size
    }
}).then(function(data) {

    var newData = { name :"root", children : [] },
        levels = ["category","topic_name","asin"];

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
            if ( depth === levels.length - 1 ) depthCursor.push({name : d.asin,
                                                                 value : Math.abs(d.bubble_size),
                                                                 bubble_color: Math.abs(d.bubble_color),
                                                                 title: d.title,
                                                                 description: d.description,
                                                                 topic_rank: d.topic_rank}); // d.sentiment
        });
    });

    var colorchoices = ['#ffffe5','#f7fcb9','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#005a32'];
    var mincolor = d3.min(data, function(d){return d.bubble_color;})
    var maxcolor = d3.max(data, function(d){return d.bubble_color})

    var colorscale = d3.scaleQuantize()
        .domain([mincolor,maxcolor])
        .range(colorchoices);

    root = d3.hierarchy(newData)
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

    let parents = g.selectAll(".parent")
            .data(root.descendants().slice(1).filter(d => d.children))
            .join("circle")
            .classed("parent", true)
            .attr("vector-effect", "non-scaling-stroke")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .attr("r", d => d.r)
            .attr("fill", "transparent")
            .attr("stroke", "none")
            .attr("stroke-width", 1)
            .style("fill", function(d) {
                            if (d.depth == 3) {return colorscale(d.data.children[0].bubble_color);}
                                         else {return d.children ? depthcolor(d.depth) : null;}; })
            .on('mouseover', tooltip.show)
        //.on('mouseout', tooltip.hide)
    ;








}).catch(function(error) {
    console.log(error);
}); 