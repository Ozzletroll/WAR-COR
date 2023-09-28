// Search for campaigns when CampaignSearchForm submitted
function campaignSearch(url, csrfToken) {

  var target_url = url;
  var searchField = document.getElementById("campaign-search");

  var data = new FormData();
  data.append("search", searchField.value);

  // Send fetch request to target url
  fetch(target_url, {
    "method": "POST",
    "headers": {
      'X-CSRF-TOKEN': csrfToken,
    },
    "body" : data,
  })
  .then(function(response) {
    if (response.status == 204){
      
      console.log("404 NOT FOUND")
      return;
    }
    else if(response.status == 400) {

      console.log("400 REPONSE OK")
      return;
    }
    
    // Create results elements
    response.json().then(function(data) {

      console.log("DO SOMETHING WITH REPONSE")
      
      // Get the results area div element
      const resultsAreaDiv = document.getElementById("results-area");

      // Delete any existing dynamic elements
      resultsAreaDiv.innerHTML = '<div id="results-marker"></div>';

      // Iterate through results data
      let index = 0
      for (let campaign in data) {

        // Create the new elements
        const newDiv = Object.assign(
          document.createElement("div"), 
          {id: "results-" + campaign,
          className: "results-area"}
          );

        const newHeading = Object.assign(
          document.createElement("h4"), 
          {className: "results-username",
          innerHTML: "Campaign: " + campaign}
          );

        const newButton = Object.assign(
          document.createElement("a"), 
          {className: "submit-button callsign-submit campaign-results-button",
          innerHTML: "Request Membership",
          href: data[campaign][1]}
          );

        // Add the elements as child
        newDiv.appendChild(newHeading);
        newDiv.appendChild(newButton);

        // Add the newly created elements
        if (index == 0) {
          const startingDiv = document.getElementById("results-marker");
          resultsAreaDiv.insertBefore(newDiv, startingDiv);
        }
        else {
          const currentDiv = document.getElementById("results-" + user);
          resultsAreaDiv.insertBefore(newDiv, currentDiv);
        }
        
        index += 1

      }

    })

  })

}