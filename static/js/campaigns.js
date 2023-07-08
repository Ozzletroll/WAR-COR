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
    this.dropdown.style.height = "140px"
    this.state = true
  }

  closeDropdown() {
    this.button.style.marginBottom = "5px"
    this.button.style.transitionDelay = "0.3s"
    this.dropdown.style.height = "0"
    this.state = false
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




