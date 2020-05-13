function display(data) {
  var layout = d3.layout
    .cloud()
    .size([500, 500])
    .words(
      Object.keys(data).map(function (key) {
        return { text: key, size: data[key] };
      })
    )
    .padding(5)
    .rotate(function () {
      return ~~(Math.random() * 2) * 90;
    })
    .font("Impact")
    .fontSize(function (d) {
      return d.size;
    })
    .on("end", draw);

  layout.start();

  function draw(words) {
    d3.select("#drc_word")
      .append("svg")
      .attr("width", layout.size()[0])
      .attr("height", layout.size()[1])
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
      .style("font-family", "Impact")
      .attr("text-anchor", "middle")
      .attr("transform", function (d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function (d) {
        return d.text;
      });
  }
}
