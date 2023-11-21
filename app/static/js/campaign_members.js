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
    this.tab.style.display = "flex";
    this.tab.style.flexDirection = "column";
    this.tab.style.maxHeight = "fit-content";

    document.getElementById(this.button).style.borderBottomLeftRadius = "0px";
    document.getElementById(this.button).style.borderBottomRightRadius = "0px";


    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.marginTop = "-20px";
    this.tab.style.display = "none";

    document.getElementById(this.button).style.borderBottomLeftRadius = "5px";
    document.getElementById(this.button).style.borderBottomRightRadius = "5px";


    this.state = false;
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



// Modal class
class Modal {
  constructor({
    modal,
    button,
    span,
  }) {
    this.modal = modal;
    this.button = button;
    this.span = span;

    this.button.onclick = event => {
      this.openModal(event)
    } 

    this.span.onclick = event => {
      this.closeModal(event)
    } 

  }
  
  openModal() {
    this.modal.style.display = "flex";
  }

  closeModal() {
    this.modal.style.display = "none";
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


// Create array to hold modal objects
const modalItems = []

// Select all dropdown elements
var modals = document.querySelectorAll('[id^="modal-"]');
var buttons = document.querySelectorAll('[id^="button-"]');
var spans = document.querySelectorAll('[id^="close-"]');

var adminModals = document.querySelectorAll('[id^="admin-modal-"]');
var adminButtons = document.querySelectorAll('[id^="admin-button-"]');
var adminSpans = document.querySelectorAll('[id^="admin-close-"]');


buttons.forEach((button, index) => {

  var modal = new Modal({
    modal: modals[index],
    button: button,
    span: spans[index],
  })
  modalItems.push(modal)
  window.addEventListener('click', function(event) {
    if (event.target == modal.modal) {
      modal.closeModal();
    }
  });
  
});

adminButtons.forEach((button, index) => {

  if (button.dataset.modal == "True") {
    var modal = new Modal({
      modal: adminModals[index],
      button: button,
      span: adminSpans[index],
    })
    modalItems.push(modal)
    window.addEventListener('click', function(event) {
      if (event.target == modal.modal) {
        modal.closeModal();
      }
    });
  }
});


// Search for users when NewUserForm is submitted
function user_search(url, csrfToken) {

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
        innerHTML: "//204: No matching users found"}
        );

        newDiv.appendChild(newHeading);
        const startingDiv = document.getElementById("results-marker");
        resultsAreaDiv.insertBefore(newDiv, startingDiv);

      return ;
    }
    else if(response.status == 400) {

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

      var message = response.json().data;

      const newHeading = Object.assign(
        document.createElement("h4"), 
        {className: "results-username",
        innerHTML: `//400: Please enter a search query`}
        );

      newDiv.appendChild(newHeading);
      const startingDiv = document.getElementById("results-marker");
      resultsAreaDiv.insertBefore(newDiv, startingDiv);

      return;
    }
    
    // Create results elements
    response.json().then(function(data) {
      
      // Get the results area div element
      const resultsAreaDiv = document.getElementById("results-area");

      // Delete any existing dynamic elements
      resultsAreaDiv.innerHTML = '<div id="results-marker"></div>';

      let index = 0
      for (let user in data["results"]) {

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
          document.createElement("button"), 
          {className: "submit-button callsign-submit",
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
