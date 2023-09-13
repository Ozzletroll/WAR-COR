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

// Iterate through both arrays, creating dropdown objects
buttons.forEach((button, index) => {

  var modal = new Modal({
    modal: modals[index],
    button: button,
    span: spans[index],
  })

  // Append object to array
  modalItems.push(modal)

  // Add click event listener to close the modal when clicking outside
  window.addEventListener('click', function(event) {
    if (event.target == modal.modal) {
      modal.closeModal();
    }
  });
  
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
    if (response.status == 404){
      
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
        innerHTML: "//404: No users found"}
        );

        newDiv.appendChild(newHeading);
        const startingDiv = document.getElementById("results-marker");
        resultsAreaDiv.insertBefore(newDiv, startingDiv);

      return ;
    }
    else if(response.status == 400) {

      console.log(response)

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
      console.log(message)

      const newHeading = Object.assign(
        document.createElement("h4"), 
        {className: "results-username",
        innerHTML: `//400: ${message}`}
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