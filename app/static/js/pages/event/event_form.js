import { Modal, PreviewModal } from "../../components/modal.js";
import { summernoteInitialise } from "../../components/summernote_initialise.js";

const formArea = document.getElementById("dynamic-field-area");

function addNewField() {

  function createFieldHTML(index) {
    return `
      <div id="event-dynamic-field-${index}" class="form-container form-container-large dynamic-field">
        <div class="campaign-form-label form-icon">
          <div class="campaign-form-label-container form-label-wrap">
            <img class="icon campaign-form-icon icon-invert" aria-label="Pen Icon"
            src="/static/images/icons/edit.svg">
            <input name="dynamic_fields-${index-1}-title" class="dynamic-field-title" value="Dynamic Field">
            <nav role="toolbar" class="form-extra-button-area form-button-dynamic" aria-label="Dynamic Field ${index} Toolbar">
              <button id="html-preview-button-${index}" type="button" class="button form-button form-preview-button">
                HTML PREVIEW
              </button>
  
              <button id="dynamic-field-delete-${index}" type="button" class="button form-button form-preview-button">
                X
              </button>
            </nav> 
          </div>
          <p class="flavour-text" aria-label="Flavour Text">UWC-6-0${4 + index} //  Event::Dynamic Field</p>
        </div>
  
        <textarea name="dynamic_fields-${index-1}-value" id="summernote-dynamic-${index}" class="campaign-input large-input event-input"></textarea>

      </div>
    `;
  }

  var newDiv = document.createElement("div");
  var dynamicFieldCount = document.getElementsByClassName("dynamic-field").length + 1;
  newDiv.innerHTML = createFieldHTML(dynamicFieldCount);
  formArea.appendChild(newDiv);

  var id = `-dynamic-${dynamicFieldCount}`;

  summernoteInitialise(
    id,
    "OPTIONAL",
    null,
    false,
    false
  );
}
window.addNewField = addNewField;

// // Create form edit check
// const editEventForm = new Form({
//   form: "edit-event-form",
//   fields: [
//     "event-form-title",
//     "event-form-type",
//     "event-form-date",
//     "event-form-location",
//     "event-form-belligerents",
//     "event-form-hide-time",
//     "summernote-desc",
//     "event-form-result"]
// })

// // Create modals
// const modal_1 = new Modal({
//   modal: document.getElementById("help-modal-1"),
//   button: document.getElementById("event-date-help-button"),
//   span: document.getElementById("help-close-1"),
// })

// const modal_2 = new Modal({
//   modal: document.getElementById("help-modal-2"),
//   button: document.getElementById("event-belligerents-help-button"),
//   span: document.getElementById("help-close-2"),
// })

// const modal_3 = new Modal({
//   modal: document.getElementById("help-modal-3"),
//   button: document.getElementById("event-format-help-button"),
//   span: document.getElementById("help-close-3"),
// })

// // HTML Preview Area Modal
// const modal_preview = new PreviewModal({
//   modal: document.getElementById("preview-modal-4"),
//   button: document.getElementById("html-preview-button"),
//   span: document.getElementById("preview-close-4"),
//   editor: document.getElementById("event-desc-field")
// })

// Check if page has delete button and create modal instance
const deleteModalCheck = document.getElementById("event-modal-0");
let deleteModal;
if (deleteModalCheck!= null) {
  deleteModal = new Modal({
    modal: document.getElementById("event-modal-0"),
    button: document.getElementById("event-delete-button"),
    span: document.getElementById("event-close-0"),
  })
}
