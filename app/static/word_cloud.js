function display(data) {
  // set the dimensions and margins of the graph
  var svg = d3
    .select("#drc_word")
    .append("svg")
    .attr("style", "solid 1px black")
    .attr("width", "100%")
    .attr("height", "350px");

  var projection = d3.geoMercator().center([45, 55]);
  var path = d3.geoPath().projection(projection);

  var g = svg.append("g");
  d3.json(
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/AGO.geo.json",
    function (error, json) {
      g.selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("fill", "red");
    }
  );
  // Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
  var layout = d3.layout
    .cloud()
    .size([width, height])
    .words(
      Object.keys(data).map(function (key) {
        return { text: key, size: data[key] };
      })
    )
    .padding(10)
    .fontSize(60)
    .on("end", draw);
  layout.start();

  // This function takes the output of 'layout' above and draw the words
  // Better not to touch it. To change parameters, play with the 'layout' variable above
  function draw(words) {
    svg
      .append("g")
      .attr(
        "transform",
        "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")"
      )
      .selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .style("font-size", function (d) {
        return d.size + "px";
      })
      .attr("text-anchor", "middle")
      .attr("transform", function (d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function (d) {
        return d.text;
      });
  }
}
