/* CONSTANTS AND GLOBALS */
const width = window.innerWidth * 0.7,
  height = window.innerHeight * 0.7,
  margin = { top: 20, bottom: 60, left: 60, right: 40 },
  radius = 5;

// these variables allow us to define anything we manipulate in init() but need access to in draw().
// All these variables are empty before we assign something to them.
let svg;
let xScale;
let yScale;
let colorScale;

/* APPLICATION STATE */
let state = {
  data: [],
  selectedParty: "All" // + YOUR INITIAL FILTER SELECTION
};

/* LOAD DATA */
d3.json("../data/filtered_data/sample_vectors2.json", d3.autoType).then(raw_data => {
  console.log("data", raw_data);
  // save our data to application state
  state.data = raw_data;
  init();
});

/* INITIALIZING FUNCTION */
// this will be run *one time* when the data finishes loading in
function init() {
  // + SCALES
  xScale = d3.scaleLinear()
    .domain(d3.extent(state.data, d => d.x_coord))
    .range([margin.left, width - margin.right]);
  
  yScale = d3.scaleLinear()
    .domain(d3.extent(state.data, d => d.y_coord))
    .range([height-margin.top, margin.bottom]);

    // if "Science fiction" in subject:
    //     return "Science Fiction"
    // if "Fantasy" in subject:
    //     return "Fantasy Fiction"
    // if "Juvenile fiction" in subject:
    //     return "Young Adult Fiction"
    // if "Mystery fiction" in subject:
    //     return "Mystery Fiction"
    // if "Historical fiction" in subject:
    //     return "Historical Fiction"
    // if "Humor" in subject:
    //     return "Humor"
    // if "Western" in subject:
    //     return "Western Fiction"
    // if "Adventure" in subject:
    //     return "Adventure Fiction"
    // if "Short stories" in subject:
    //     return "Short Stories"
    // return "General Fiction"
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
    ])
    .range([
        "red", 
        "blue", 
        "green", 
        "yellow", 
        "pink", 
        "purple", 
        "orange", 
        "brown", 
        "silver", 
        "gold"
    ])

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
      draw();
    })


  // + CREATE SVG ELEMENT
  svg = d3.select("#container")
    .append("svg")
    .attr("width", width)
    .attr("height", height)

  // + CALL AXES
  svg
    .append("g")
    .call(xAxis)
    .attr("transform", `translate(0,${height - margin.top})`)
  
  svg
    .append("g")
    .call(yAxis)
    .attr("transform", `translate(${margin.left},0)`)

  draw(); // calls the draw function
}

/* DRAW FUNCTION */
// we call this every time there is an update to the data/state
function draw() {

  // + FILTER DATA BASED ON STATE
  const filteredData = state.data
    .filter(d => state.selectedParty === "All" || state.selectedParty === d.genre)

  const dot = svg
    .selectAll("circle")
    .data(filteredData, d => `id_${d.genre}_${d.y_coord}_${d.x_coord}`)
    .join(
      // + HANDLE ENTER SELECTION
      enter => enter.append("circle")
        .attr("r", radius)
        .attr("cx", 0)
        .attr("cy", d => yScale(d.y_coord))
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
          .attr("r", radius) // bring it back to original size

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
}