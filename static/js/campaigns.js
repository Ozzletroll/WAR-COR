// Dropdown class
class Dropdown {
  constructor({
    dropdown,
    button,
  }) {
    this.dropdown = dropdown;
    this.button = button;
    this.buttonOutline = button.parentNode;
    this.state = false

    this.button.onclick = event => {
      
      event.stopPropagation();

      if (this.state == false) {
        this.closeAllDropdowns();
        this.openDropdown(event)
      }
      else if (this.state == true) {
        this.closeDropdown(event)
      }

    } 
  }
  
  openDropdown() {
    this.button.style.transitionDelay = "0s";
    this.button.style.borderBottomLeftRadius = "0px";
    this.buttonOutline.style.borderBottomLeftRadius = "0px";
    this.button.style.borderBottomRightRadius = "0px";
    this.buttonOutline.style.borderBottomRightRadius = "0px";
    this.dropdown.style.height = "150px";
    this.dropdown.style.border = "1px solid var(--dark_red)";
    this.dropdown.style.borderTop = "0px";
    this.state = true
  }

  closeDropdown() {
    this.button.style.transitionDelay = "0.1s";
    this.dropdown.style.height = "0";
    this.state = false;

    // Disable transition delay after 0.1s
  setTimeout(() => {
    this.button.style.borderBottomLeftRadius = "";
    this.buttonOutline.style.borderBottomLeftRadius = "";
    this.button.style.borderBottomRightRadius = "";
    this.buttonOutline.style.borderBottomRightRadius = "";
    this.button.style.transitionDelay = "0s";
    this.dropdown.style.border = "0px";
  }, 100);
  }

  closeAllDropdowns() {
    for (let i = 0; i < menuItems.length; i++) {
      const dropdown = menuItems[i];
      if (dropdown.state == true) {
        dropdown.closeDropdown();
      }
    }
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

// Close drowdowns if another element clicked
window.onclick = event => {
  for (let i = 0; i < menuItems.length; i++) {
    const dropdown = menuItems[i];
    if (dropdown.state == true && !dropdown.dropdown.contains(event.target)) {
      dropdown.closeDropdown();
    }
  }
}