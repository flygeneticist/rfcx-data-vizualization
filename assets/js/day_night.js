function day_night(data) {
  "use strict";
  // create space + structre for chart based on JSON data
  d3.select("div.metrics")
    .append("div")
      .attr("class", "chart r1 c1")
      .selectAll("div.line")
    .data(data)
    .enter()
    .append("div")
      .attr("class","line");

  // attach a label to each line
  d3.selectAll("div.line")
    .append("div")
      .attr("class","label")
      .text(function(d) { return d.guid });

  // attach a bar to each line
  d3.selectAll("div.line")
    .append("div")
      .attr("class","bar")
      .style("width", function(d) { return d.alerts.length*100 + "px" })
      .text(function(d) { return d.alerts.length });

}
