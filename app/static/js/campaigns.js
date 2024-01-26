// Tab class
class Tab {
  constructor({
    tab,
    button,
  }) {
    this.tab = tab;
    this.button = button;
    this.corner = this.button.parentNode.querySelector(".campaign-corner");
    this.state = false;

    this.button.onclick = event => {

      var screenWidth = window.innerWidth || document.documentElement.clientWidth;
      
      if (this.state == false && screenWidth <= 500) {
        this.openTab(event)
      }
      else if (this.state == true && screenWidth <= 500) {
        this.closeTab(event)
      }
    } 
  }
  
  openTab() {
    this.tab.style.display = "flex";
    this.tab.style.maxHeight = "fit-content";

    this.button.style.borderBottomLeftRadius = "0px";
    this.corner.style.borderBottomRightRadius = "0px";

    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.display = "none";

    this.button.style.borderBottomLeftRadius = "5px";
    this.corner.style.borderBottomRightRadius = "5px";

    this.state = false;
  }

}

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

// Create mobile tabs for all campaigns
const campaigns = [];
var tabs = document.getElementsByClassName("campaign-entry");
Array.from(tabs).forEach((element) => {

  var buttonElement = element.querySelector(".campaign-header");
  var tabElement = element.querySelector(".campaign-body");

  var tab = new Tab({
    tab: tabElement,
    button: buttonElement,
  })

  campaigns.push(tab);

})

// If resizing above 500px, open all tabs again
window.addEventListener("resize", function() {
  if (window.innerWidth > 500) {
    Array.from(campaigns).forEach((tab) => {
      tab.openTab();
    })
  }
  else {
    Array.from(campaigns).forEach((tab) => {
      tab.closeTab();
    })
  }
});