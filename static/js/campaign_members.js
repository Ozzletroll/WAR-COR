// Tab class
class Tab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
    this.state = false

    document.getElementById(this.button).onclick = event => {
      
      if (this.state == false) {
        this.openTab(event)
      }
      else if (this.state == true) {
        this.closeTab(event)
      }
    } 
  }
  
  openTab() {
    this.tab.style.marginTop = "20px";
    this.tab.style.display = "flex"
    this.tab.style.flexDirection = "column"
    this.tab.style.maxHeight = "fit-content";
    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.marginTop = "-20px";
    this.tab.style.display = "none"
    this.state = false
  }

}

// Dropdown user results class
class ToggleButton {
  constructor({
    area,
    button,
  }) {
    this.area = document.getElementById(area);
    this.button = button;
    this.state = false

    document.getElementById(this.button).onclick = event => {
      
      if (this.state == false) {
        this.openArea(event)
      }
      else if (this.state == true) {
        this.closeArea(event)
      }
    } 
  }
  
  openArea() {
    this.area.style.display = "flex"
    this.state = true
  }

  closeArea() {
    this.area.style.display = "none"
    this.state = false
  }

}

// Create tabs
const tab_1 = new Tab({
  tab: "tab-1",
  button: "t1-button",
})

const tab_2 = new Tab({
  tab: "tab-2",
  button: "t2-button",
})

// Search for users when NewUserForm is submitted
function user_search(url) {

  var target_url = url
  var username = document.getElementById("username-search")

  var data = new FormData()
  data.append("username", username.value)

  // Send fetch request to target url
  fetch(target_url, {
    "method": "POST",
    "body" : data,
  })
  .then(function(response) {
    if (response.status !== 200){
      
      // Get the results area div element
      const resultsAreaDiv = document.getElementById("results-area");

      // Delete any existing dynamic elements
      resultsAreaDiv.innerHTML = '<div id="results-marker"></div>';

      // Create no users found entry
      const newDiv = Object.assign(
        document.createElement("div"), 
        {id: "results-none",
        className: "results-area"}
        );

      const newHeading = Object.assign(
        document.createElement("h4"), 
        {className: "results-username",
        innerHTML: "No users found"}
        );

        newDiv.appendChild(newHeading);
        const startingDiv = document.getElementById("results-marker");
        resultsAreaDiv.insertBefore(newDiv, startingDiv);

      return ;
    }
    
    // Create results elements
    response.json().then(function(data) {
      
      // Get the results area div element
      const resultsAreaDiv = document.getElementById("results-area");

      // Delete any existing dynamic elements
      resultsAreaDiv.innerHTML = '<div id="results-marker"></div>';

      let index = 0
      for (let user in data) {

        // Create the new elements
        const newDiv = Object.assign(
          document.createElement("div"), 
          {id: "results-" + user ,
          className: "results-area"}
          );

        const newHeading = Object.assign(
          document.createElement("h4"), 
          {className: "results-username",
          innerHTML: "User: " + user}
          );

        const newButton = Object.assign(
          document.createElement("a"), 
          {className: "submit-button callsign-submit",
          innerHTML: "Invite",
          href: data[user][1]}
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