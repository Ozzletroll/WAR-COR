// Dropdown class
class Dropdown {
  constructor({
    dropdown,
    button,
  }) {
    this.dropdown = dropdown;
    this.button = button;
    this.state = false

    this.button.onclick = event => {
      
      if (this.state == false) {
        this.openDropdown(event)
      }
      else if (this.state == true) {
        this.closeDropdown(event)
      }
    } 
  }
  
  openDropdown() {
    this.button.style.marginBottom = "0"
    this.button.style.transitionDelay = "0s"
    this.dropdown.style.height = "150px"
    this.state = true
  }

  closeDropdown() {
    this.button.style.transitionDelay = "0.3s"
    this.dropdown.style.height = "0"
    this.state = false

    // Disable transition delay after 0.3s
  setTimeout(() => {
    this.button.style.transitionDelay = "0s";
  }, 300);
  }

}

// Create array to hold dropdown objects
const menuItems = []

// Select all dropdown elements
var buttons = document.querySelectorAll('[id^="button-"]');
var dropdowns = document.querySelectorAll('[id^="dropdown-"]');

// Iterate through both arrays, creating dropdown objects
buttons.forEach((button, index) => {

  var dropdown = new Dropdown({
    dropdown: dropdowns[index],
    button: button,
  })

  // Append object to array
  menuItems.push(dropdown)
});


// Get the radio buttons
const radioList = document.getElementById("campaign-toggle-list");
const radioGrid = document.getElementById("campaign-toggle-grid");

// Add event listener to each radio button
radioList.addEventListener("click", toggleLabelBackground);
radioGrid.addEventListener("click", toggleLabelBackground);

// Add event listener for page load
document.addEventListener("DOMContentLoaded", toggleLabelBackground);

// Function to toggle label background
function toggleLabelBackground() {
  // Get the labels
  const labelList = document.querySelector('label[for="campaign-toggle-list"]');
  const labelGrid = document.querySelector('label[for="campaign-toggle-grid"]');

  // Change label background based on checked status
  if (radioList.checked) {
    labelList.style.backgroundColor = "var(--elem_bright)";
    labelGrid.style.backgroundColor = "";
  } else if (radioGrid.checked) {
    labelList.style.backgroundColor = "";
    labelGrid.style.backgroundColor = "var(--elem_bright)";
  }
}
