import { Modal } from "../../components/modal.js";
import { CharCount } from "../../components/char_count.js";
import { Toolbar } from '../../components/ui/ui_toolbar.js';
import { addHeaderIdMarker } from '../../components/header_id_marker.js';


// Add tooltips to ui toolbar
const toolbar = new Toolbar()

// Create array to hold modal objects
const modalItems = []

// Select all dropdown elements
var modals = document.querySelectorAll('[id^="comment-modal-"]');
var buttons = document.querySelectorAll('[id^="comment-button-"]');
var spans = document.querySelectorAll('[id^="comment-close-"]');

// Iterate through both arrays, creating modal objects
buttons.forEach((button, index) => {

  var modal = new Modal({
    modal: modals[index],
    button: button,
    span: spans[index],
  })
  modalItems.push(modal)
});

// Show/hide lower adjacent element links based on event-main-container height
function checkEventHeight() {
  var lowerAdjacentElement = document.querySelector(".adjacent-events-lower");

  var event = document.querySelector(".event-centre-container");
  var eventHeight = event.clientHeight + 200;
  var windowHeight = window.innerHeight;

  if (eventHeight > windowHeight) {
    lowerAdjacentElement.style.display = "flex";
  }
  else {
    lowerAdjacentElement.style.display = "none";
  }
  
}

// Add click event listener to close the modal when clicking outside
window.addEventListener('load', function() {
  checkEventHeight();
});
window.addEventListener('resize', function() {
  checkEventHeight();
});

// Add id's to user submitted header elements
var htmlFields = document.getElementsByClassName("event-page-description");
Array.from(htmlFields).forEach(field => {
  addHeaderIdMarker(field);
});

// Create char count on comment form
var commentFormPresent = document.getElementById("summernote-comment");
if (commentFormPresent) {
  const commentCharCount = new CharCount({
    charField: document.getElementsByClassName("note-editable")[0],
    charCount: document.getElementById("remaining-chars"),
    summernote: true,
  })
}

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

// Style all horus theme text elements
var horusElements = document.getElementsByClassName("summernote-horus");

Array.from(horusElements).forEach(element => {
  element.setAttribute("data-content", element.innerText);
});
