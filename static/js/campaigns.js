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
    this.button.style.transitionDelay = "0s";
    this.dropdown.style.height = "150px";
    this.dropdown.style.border = "1px solid var(--dark_red)";
    this.dropdown.style.borderTop = "0px";
    this.state = true
  }

  closeDropdown() {
    this.button.style.transitionDelay = "0.3s";
    this.dropdown.style.height = "0";
    this.state = false;

    // Disable transition delay after 0.3s
  setTimeout(() => {
    this.button.style.transitionDelay = "0s";
    this.dropdown.style.border = "0px";
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



