$.getJSON( "data.json", function( data ) {
  document.getElementById("biden-count").innerText = data.biden.college_count;
  document.getElementById("trump-count").innerText = data.trump.college_count;
  document.getElementById("biden").setAttribute("style", "--biden-width: " + data.biden.width);
  document.getElementById("trump").setAttribute("style", "--trump-width: " + data.trump.width);
  document.getElementById("time-updated").innerText = "Time updated: " + data.time_updated;
});