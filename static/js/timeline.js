// Dropdown class
class Event {
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
    var contentHeight = this.dropdown.scrollHeight;
    this.dropdown.style.minHeight = contentHeight + "px";
    this.state = true

    // Update contentHeight to account for sidebar resizing
    setInterval(() => {
      const updatedContentHeight = this.dropdown.scrollHeight;
      if (contentHeight !== updatedContentHeight && this.state == true) {
        contentHeight = updatedContentHeight;
        this.dropdown.style.minHeight = contentHeight + "px";
      }
    }, 300);

  }

  closeDropdown() {
    this.dropdown.style.minHeight = "0"
    this.state = false
  }

}

// Create array to hold dropdown objects
const eventItems = []

// Select all dropdown elements
var buttons = document.querySelectorAll('[id^="event-"]');
var dropdowns = document.querySelectorAll('[id^="dropdown-"]');

// Iterate through both arrays, creating dropdown objects
buttons.forEach((button, index) => {

  var event = new Event({
    dropdown: dropdowns[index],
    button: button,
  })

  // Append object to array
  eventItems.push(event)
});




