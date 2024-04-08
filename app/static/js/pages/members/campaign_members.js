import { Modal } from "../../components/modal.js";


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
    this.tab.style.display = "flex";
    this.tab.style.flexDirection = "column";
    this.tab.style.maxHeight = "fit-content";

    document.getElementById(this.button).style.borderBottomLeftRadius = "0px";
    document.getElementById(this.button).style.borderBottomRightRadius = "0px";

    this.state = true
  }

  closeTab() {
    this.tab.style.maxHeight = "0";
    this.tab.style.display = "none";

    document.getElementById(this.button).style.borderBottomLeftRadius = "5px";
    document.getElementById(this.button).style.borderBottomRightRadius = "5px";


    this.state = false;
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

const tab_3 = new Tab({
  tab: "tab-3",
  button: "t3-button",
})


// Create array to hold modal objects
const modalItems = []

// Select all dropdown elements
var modals = document.querySelectorAll('[id^="remove-modal-"]');
var buttons = document.querySelectorAll('[id^="remove-button-"]');
var spans = document.querySelectorAll('[id^="remove-close-"]');

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
