$.getJSON( "data.json", function( data ) {
  document.getElementById("biden-count").innerText = data.biden.college_count;
  document.getElementById("trump-count").innerText = data.trump.college_count;
  document.getElementById("biden").setAttribute("style", "--biden-width: " + data.biden.width);
  document.getElementById("trump").setAttribute("style", "--trump-width: " + data.trump.width);
  document.getElementById("time-updated").innerText = "Time updated: " + data.time_updated;

  let states = ["georgia","nevada","north-carolina","pennsylvania","arizona","florida"];

  states.forEach((state) => {

    let state_obj = data[state]

    let biden_background_color;
    let trump_background_color;

    let biden_text_color;
    let trump_text_color;

    if (state_obj.won){
      if (state_obj.leaning === "Biden"){
        biden_background_color = "#25428f";
        trump_background_color = "#ccc";
        biden_text_color = "#fff";
        trump_text_color = "#000";
      } else {
        biden_background_color = "#ccc";
        trump_background_color = "#cc0a11";
        biden_text_color = "#000";
        trump_text_color = "#fff";
      }
    } else {
      if (state_obj.leaning === "Biden"){
        biden_background_color = "#8ca6e7";
        trump_background_color = "#ccc";
        biden_text_color = "#fff";
        trump_text_color = "#000";
      } else {
        biden_background_color = "#ccc";
        trump_background_color = "#ee888c";
        biden_text_color = "#000";
        trump_text_color = "#fff";
      }
    }

    let vote_diff = "";

    if (state_obj.leaning === "Biden"){
      vote_diff = "<span style='color:#25428f;font-weight:bold;'>+" + (state_obj.biden_votes - state_obj.trump_votes) + " votes </span>";
    } else {
      vote_diff = "<span style='color:#cc0a11;font-weight:bold;'>+" + (state_obj.trump_votes - state_obj.biden_votes) + " votes </span>";
    }

    let biden_div = "<div class='perc' style='background-color:" + biden_background_color + "'>" + "<span class='perc-label' style='color:" + biden_text_color + "'>" + state_obj.biden_perc + "%</span>" + "</div>"
    let trump_div = "<div class='perc' style='background-color:" + trump_background_color + "'>" + "<span class='perc-label' style='color:" + trump_text_color + "'>" + state_obj.trump_perc + "%</span>" + "</div>"

    let state_label = "<span class='state-label'>" + state_obj.name + " - " + state_obj.perc_counted + "% counted " + vote_diff + "</span>";

    document.getElementById(state).innerHTML = state_label + "<div class='perc-container'>" + biden_div + trump_div + "</div>";
  })

});

