/* CONSTANTS AND GLOBALS */
const width = window.innerWidth * 0.7,
  height = window.innerHeight * 0.7,
  margin = { top: 20, bottom: 60, left: 60, right: 40 },
  radius = 5,
  padding = 10,
  xDomain = [-200,200],
  yDomain = [-200, 200];

// these variables allow us to define anything we manipulate in init() but need access to in draw().
// All these variables are empty before we assign something to them.
// let svg;
let xScale;
let yScale;
let colorScale;
let tooltip;

/* APPLICATION STATE */
let state = {
  data: [],
  selectedParty: "All" // + YOUR INITIAL FILTER SELECTION
};

/* LOAD DATA */
d3.json("../data/filtered_data/book_vectors_no_vector.json", d3.autoType).then(raw_data => {
  console.log("data", raw_data);
  // save our data to application state
  state.data = raw_data;
  init();
  // initZoom();
});

/* INITIALIZING FUNCTION */
// this will be run *one time* when the data finishes loading in
function init() {
  // + SCALES
  xScale = d3.scaleLinear()
  .domain(xDomain)
  .range([width - padding, padding]);
  
  yScale = d3.scaleLinear()
  .domain(yDomain)
  .range([height - padding, padding]);

  colorScale = d3.scaleOrdinal()
    .domain([
        "Science Fiction", 
        "Fantasy Fiction",
        "Young Adult Fiction",
        "Historical Fiction",
        "Mystery Fiction",
        "General Fiction",
        "Short Stories",
        "Humor",
        "Western Fiction",
        "Adventure Fiction"
    ]).range(d3.schemeSet3)

  // + AXES
  const xAxis = d3.axisBottom(xScale)
  const yAxis = d3.axisLeft(yScale)

  // + UI ELEMENT SETUP
  const selectElement = d3.select("#dropdown")

  selectElement  
    .selectAll("option")
    .data([...Array.from(new Set(state.data.map(d => d.genre))), "All"])
    .join("option")
    .attr("value", d => d)
    .text(d => d)

  selectElement
    .on("change", (event) => {
      console.log(event)
      state.selectedParty = event.target.value;
      // initZoom(); //maybe?
      draw();
    })

  const container = d3.select("#container").style("position", "relative");
  tooltip = container.append("div")
  .attr("class", "tooltip")

  // + CREATE SVG ELEMENT
  svg = d3.select("#container")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    // .call(zoom)
    // .call(zoom.transform, d3.zoomIdentity);

  const grid = svg.append('g').attr("class", "grid grid--cartesian");

  // + CALL AXES
  // Plot the x-axis
  const xAxisPlot = grid.append("g")
			.attr("class", "axis axis--x")
			.attr("transform", "translate(0," + (height / 2) +")")
			.call(xAxis.tickSize(-height, 0, 0));

  // Plot the y-axis
  const yAxisPlot = grid.append("g")
		.attr("class", "axis axis--y")
		.attr("transform", "translate("+ (width/2) +",0)")
		.call(yAxis.tickSize(-width, 0, 0));
  
  // Add the x-axis lines/ticks
  xAxisPlot.selectAll(".tick line")
    	.attr("stroke", "silver")
		.attr("y1", (width - (2*padding))/2 * -1)
		.attr("y2", (width - (2*padding))/2 * 1);

  	// Add the y-axis lines/ticks
	yAxisPlot.selectAll(".tick line")
  	.attr("stroke", "silver")
		.attr("x1", (width - (2*padding))/2 * -1)
		.attr("x2", (width - (2*padding))/2 * 1);

  draw(); // calls the draw function

  // Define Zoom Behavior
  const zoom = d3.zoom()
    .scaleExtent([0.5, 5]) // Change these values for min and max zoom levels
    .translateExtent([[-100, -100], [width + 100, height + 100]]) // Adjust panning limits
    .on('zoom', zoomed);

  // Apply Zoom Behavior to the SVG
  svg.call(zoom);

  /* ZOOM FUNCTION */
  function zoomed(event) {
    // Create new transform
    const transform = event.transform;

    // Update scales with transform
    const new_xScale = transform.rescaleX(xScale);
    const new_yScale = transform.rescaleY(yScale);

    // Update axes with new scales
    svg.select(".axis--x")
      .attr("transform", `translate(0,${height / 2})`)
      .call(d3.axisBottom(new_xScale).tickSize(-height, 0, 0));
    svg.select(".axis--y")
      .attr("transform", `translate(${width / 2},0)`)
      .call(d3.axisLeft(new_yScale).tickSize(-width, 0, 0));

    // Update grid lines
    svg.selectAll(".axis--x .tick line")
      .attr("y1", (height - (2*padding))/2 * -1)
      .attr("y2", (height - (2*padding))/2 * 1)
      .attr('transform', d => `translate(${new_xScale(d) - width/2}, 0)`);

    svg.selectAll(".axis--y .tick line")
      .attr("x1", (width - (2*padding))/2 * -1)
      .attr("x2", (width - (2*padding))/2 * 1)
      .attr('transform', d => `translate(0, ${new_yScale(d) - height/2})`);

    // Update circles with new scales
    svg.selectAll("circle")
      .attr('cx', d => new_xScale(d.x_coord))
      .attr('cy', d => new_yScale(d.y_coord));
  }
}

/* DRAW FUNCTION */
// we call this every time there is an update to the data/state
function draw() {

  // + FILTER DATA BASED ON STATE
  const filteredData = state.data
    .filter(d => state.selectedParty === "All" || state.selectedParty === d.genre);

  
  const dot = svg
    .selectAll("circle")
    .data(filteredData, d => `id_${d.genre}_${d.y_coord}_${d.x_coord}`)
    .join(
      // + HANDLE ENTER SELECTION
      enter => enter.append("circle")
        .attr("r", radius)
        .attr("cx", 0)
        .attr("cy", d => yScale(d.y_coord))
        .attr("stroke", "darkblue")
        .attr("fill", d => colorScale(d.genre))
        .call(sel => sel
          .transition()
          .duration(1000)
          .attr("cx", d => xScale(d.x_coord))
        ),

      // + HANDLE UPDATE SELECTION
      update => {
        update
          .transition()
          .duration(250)
          .attr("r", radius * 3) // increase radius size
          .transition()
          .duration(250)
          .attr("r", radius); // bring it back to original size

        return update
      },

      // + HANDLE EXIT SELECTION
      exit => exit
        .call(sel => sel
          //before
          .attr("opacity", 1)
          .transition()
          .duration(1000)
          // after
          .attr("opacity", 0)
          .remove()
        )
    );
  
    // Create mouseover highlight for dots
    dot.on('mouseover', function(event, d) {
      // Position the tooltip and make it visible
      tooltip.style("visibility", "visible")
             .style("top", (event.pageY - 10) + "px")
             .style("left",(event.pageX + 10) + "px")
             .html(`ID: ${d.id}<br> Title: ${d.title}<br> Author: ${d.author}<br> Genre: ${d.genre}<br> Coord: ${d.x_coord}, ${d.y_coord}`); // Customize this text as needed
    
      // Highlight the dot
      d3.select(this).attr('stroke', '#333').attr('stroke-width', 2);
    })
    .on('mousemove', function(event) {
      // Make the tooltip follow the cursor
      tooltip.style("top", (event.pageY - 10) + "px")
             .style("left",(event.pageX + 10) + "px");
    })
    .on('mouseout', function() {
      // Hide the tooltip and remove the highlight from the dot
      tooltip.style("visibility", "hidden");
      d3.select(this).attr('stroke', null);
    });
}