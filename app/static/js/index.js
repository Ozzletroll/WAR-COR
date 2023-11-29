// Modal class
class Modal {
  constructor({
    modal,
    button,
    span,
  }) {
    this.modal = document.getElementById(modal);
    this.button = button;
    this.span = span;

    document.getElementById(this.button).onclick = event => {
      this.openModal(event)
    } 

    document.getElementById(this.span).onclick = event => {
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

// Create modals
const modal_1 = new Modal({
  modal: "modal-1",
  button: "m1-button",
  span: "close-1",
})

const modal_2 = new Modal({
  modal: "modal-2",
  button: "m2-button",
  span: "close-2",
})

const modal_3 = new Modal({
  modal: "modal-3",
  button: "m3-button",
  span: "close-3",
})

const modal_4 = new Modal({
  modal: "modal-4",
  button: "m4-button",
  span: "close-4",
})


// Close modals if the user clicks anywhere else
window.onclick = function(event) {
    if (event.target == modal_1.modal) {
      modal_1.closeModal();
    }
    if (event.target == modal_2.modal) {
      modal_2.closeModal();
    }
    if (event.target == modal_3.modal) {
      modal_3.closeModal();
    }
    if (event.target == modal_4.modal) {
      modal_4.closeModal();
    }

  }

var timeout;

// Get navbar and hide box-shadow if at position 0
// Hide down arrow if not a at position 0
function checkScrollPos () {
  var navbar = document.getElementById("navbar");
  var downArrow = document.getElementById("down-arrow");
  
  if (window.scrollY == 0) {
    navbar.style.boxShadow = "none";
    downArrow.style.opacity = "";
    downArrow.style.display = "flex";

    // Clear timeout
    clearTimeout(timeout);
  }
  else {
    navbar.style.boxShadow = "";
    downArrow.style.opacity = "0";

    // Clear the timeout to prevent multiple timeouts from being set
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      downArrow.style.display = "none";
    }, 300);
  }
  
}

window.addEventListener("load", checkScrollPos);
window.addEventListener("scroll", checkScrollPos);
