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



// Apply styling to user submitted image links
const elements = document.querySelectorAll(".event-desc p");
let imageCount = 0;

elements.forEach((element) => {
  if (element.querySelector("img")) {
    imageCount++;

  // Create surrounding element
  const newDiv1 = document.createElement("div");
  newDiv1.classList.add("user-image-area");

  // Wrap the element within the new div
  element.parentNode.insertBefore(newDiv1, element);
  newDiv1.appendChild(element);

  // Create surrounding element
  const newDiv2 = document.createElement("div");
  newDiv2.classList.add("user-image-elem");

  // Wrap the element within the new div
  element.parentNode.insertBefore(newDiv2, element);
  newDiv2.appendChild(element);

  // Create header
  const newHeader = document.createElement("div");
  newHeader.classList.add("user-image-header");
  newHeader.textContent = `Image::Data_${String(imageCount).padStart(2, "0")}`;

  // Insert the header
  element.parentNode.insertBefore(newHeader, element);

  // Centre img elements in user submitted p elements
  element.style.display = "flex";
  element.style.width = "auto";
  element.style.justifyContent = "center";
  element.style.margin = "0";

}});


// Apply styling to comment images
const images = document.querySelectorAll(".comment-body p");

images.forEach(element => {
  if (element.querySelector("img")) {

  // Centre img elements
   element.style.display = "flex";
   element.style.width = "auto";
   element.style.justifyContent = "center";
   element.style.margin = "20px"
  }

});

