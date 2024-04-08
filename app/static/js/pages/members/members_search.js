// Search for users when NewUserForm is submitted
function userSearch(url, csrfToken) {

    var target_url = url;
    var username = document.getElementById("username-search");
  
    var data = new FormData();
    data.append("username", username.value);
  
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
        
        // Get the results area div element
        const resultsAreaDiv = document.getElementById("results-area");
        // Delete any existing dynamic elements
        resultsAreaDiv.innerHTML = '<div id="results-marker" aria-hidden="true"></div>';
  
        // Create no users found entry
        const newLi = Object.assign(
          document.createElement("li"), 
          {id: "results-none",
          className: "results-area"}
          );
  
        const newHeading = Object.assign(
          document.createElement("h4"), 
          {className: "results-username",
          innerHTML: "//204: No matching users found"}
          );
  
          newLi.appendChild(newHeading);
          const startingDiv = document.getElementById("results-marker");
          resultsAreaDiv.insertBefore(newLi, startingDiv);
  
        return ;
      }
      else if(response.status == 400) {
  
        // Get the results area div element
        const resultsAreaDiv = document.getElementById("results-area");
        // Delete any existing dynamic elements
        resultsAreaDiv.innerHTML = '<div id="results-marker" aria-hidden="true"></div>';
  
        // Create no users found entry
        const newLi = Object.assign(
          document.createElement("li"), 
          {id: "results-none",
          className: "results-area"}
          );
  
        var message = response.json().data;
  
        const newHeading = Object.assign(
          document.createElement("h4"), 
          {className: "results-username",
          innerHTML: `//400: Please enter a search query`}
          );
  
        newLi.appendChild(newHeading);
        const startingDiv = document.getElementById("results-marker");
        resultsAreaDiv.insertBefore(newLi, startingDiv);
  
        return;
      }
      
      // Create results elements
      response.json().then(function(data) {
        
        // Get the results area div element
        const resultsAreaDiv = document.getElementById("results-area");
  
        // Delete any existing dynamic elements
        resultsAreaDiv.innerHTML = '<div id="results-marker" aria-hidden="true"></div>';
  
        let index = 0
        for (let user in data["results"]) {
  
          // Create the new elements
          const newLi = Object.assign(
            document.createElement("li"), 
            {id: "results-" + user ,
            className: "results-area"}
            );
  
          const newHeading = Object.assign(
            document.createElement("h4"), 
            {className: "results-username",
            innerHTML: user}
            );
  
          const newButton = Object.assign(
            document.createElement("button"), 
            {className: "button submit-button callsign-submit",
            innerHTML: "Invite"}
            );
  
          // Set result data as attributes of button
          newButton.setAttribute("data-userID", data["results"][user]["id"]);
          newButton.setAttribute("data-username", data["results"][user]["username"]);
          newButton.setAttribute("data-targetURL", data["target_url"]);
  
          // Bind onclick function
          newButton.addEventListener("click", function(event) {
            element = event.target;
            populateForm(element);
          });
  
          // Add the elements as child of parent div
          newLi.appendChild(newHeading);
          newLi.appendChild(newButton);
  
          // Add the newly created elements
          if (index == 0) {
            const startingDiv = document.getElementById("results-marker");
            resultsAreaDiv.insertBefore(newLi, startingDiv);
          }
          else {
            const currentDiv = document.getElementById("results-" + user);
            resultsAreaDiv.insertBefore(newLi, currentDiv);
          }
          
          index += 1
  
        }
  
      })
  
    })
  
  }
  
  // Function called when clicking an invite button. Grabs user data and fills hidden form, then submits.
  function populateForm(element) {
  
    var userID = element.dataset.userid;
    var username = element.dataset.username;
    var targetURL = element.dataset.targeturl;
  
    // Get form and set target url
    var form = document.getElementById("add-user-form");
    form.setAttribute("action", targetURL);
  
    // Populate form with search result data
    var usernameField = form.elements.username;
    var userIDField = form.elements.user_id;
    usernameField.value = username;
    userIDField.value = userID;
  
    // Submit form
    form.submit()
  }
  