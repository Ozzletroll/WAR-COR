// Search for users when NewUserForm is submitted
function userSearch(url, csrfToken, additionalArg=null, previousSearch=null) {

    

    var target_url = url;
    var username = document.getElementById("username-search").value;
  
    var data = new FormData();
    if (previousSearch != null) {
      username = previousSearch;
    }
    data.append("username", username);
    data.append("page", additionalArg)

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
        deleteOldElements(resultsAreaDiv);

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
        deleteOldElements(resultsAreaDiv);
  
        // Create no users found entry
        const newLi = Object.assign(
          document.createElement("li"), 
          {id: "results-none",
          className: "results-area"}
          );
  
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
        deleteOldElements(resultsAreaDiv);

        for (let index in data["page"]["items"]) {

          // Create the new elements
          const newLi = Object.assign(
            document.createElement("li"), 
            {id: "results-" + index ,
            className: "results-area"}
            );
  
          const newHeading = Object.assign(
            document.createElement("h4"), 
            {className: "results-username",
            innerHTML: data["page"]["items"][index]["username"]}
            );
  
          const newButton = Object.assign(
            document.createElement("button"), 
            {className: "button submit-button callsign-submit",
            innerHTML: "Invite"}
            );
  
          // Set result data as attributes of button
          newButton.setAttribute("data-userID", data["data"][index]["id"]);
          newButton.setAttribute("data-username", data["data"][index]["username"]);
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
            const currentDiv = document.getElementById("results-" + index);
            resultsAreaDiv.insertBefore(newLi, currentDiv);
          }
          
        }

        if (data["pages"].length > 1) {

          var newMemberTab = document.getElementById("tab-2");
      
          let innerElements = "";

          for (let index = 0; index < data["page_numbers"].length; index++) {
            const page_number = data["page_numbers"][index];
            if (page_number) {
              if (page_number !== data.current_page) {
                innerElements += `<button id="page-${page_number}" class="pagination-item page-button" data-pagenumber="${page_number}">${page_number}</button>`;
              } else {
                innerElements += `<strong class="pagination-item current-page-item" aria-label="Current Page">${page_number}</strong>`;
              }
            } else {
              innerElements += `<span class="pagination-item ellipsis">…</span>`;
            }
          }

          const newPageWidget = Object.assign(
            document.createElement("nav"), 
            {id: "user-search-pagination",
            className: "user-search-pagination",
            ariaLabel: "Page Selection",
            innerHTML: innerElements}
            );

          newMemberTab.appendChild(newPageWidget);
          bindPageFunctions();
        }
  
      })
  
    })
  
    // Function to bind fetch request functions to page number buttons
    // Passes previous search value, preventing changing page
    // from taking new search input values.
    function bindPageFunctions() {
      var pageButtons = document.getElementsByClassName("page-button");

      Array.from(pageButtons).forEach(button => {
        let pageNumber = button.dataset.pagenumber;
        button.addEventListener("click", function() {
          userSearch(url, csrfToken, pageNumber, username);
        });
      })
    }

    function deleteOldElements(resultsAreaDiv) {
      resultsAreaDiv.innerHTML = '<div id="results-marker" aria-hidden="true"></div>';
      var pageSelector = document.getElementById("user-search-pagination");
      if (pageSelector != null) {
        pageSelector.remove();
      }
    }

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
  