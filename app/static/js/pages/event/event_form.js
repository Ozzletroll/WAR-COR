import { Modal, PreviewModal } from "../../components/modal.js";
import { summernoteInitialise } from "../../components/summernote_initialise.js";


function setDraggableItems(formArea) {
  var fieldList = new Sortable(formArea, {
    handle: ".handle",
    animation: 150
  });
}

const formArea = document.getElementById("dynamic-field-area");
setDraggableItems(formArea);

function addNewField() {

  function createFieldHTML(index) {
    return `
      <div id="event-dynamic-field-${index}" class="form-container form-container-large dynamic-field">
        <div class="dynamic-field-inner">
          <div class="dynamic-field-draggable">
            <div class="campaign-form-label form-icon">
              <div class="campaign-form-label-container dynamic-form-label-container">

                <div class="dynamic-form-title-container">
                  <img class="icon campaign-form-icon icon-invert" aria-label="Pen Icon"
                  src="/static/images/icons/edit.svg">
                  <div class="form-input-container dynamic-form-title-area">
                    <input name="dynamic_fields-${index-1}-title" class="form-input dynamic-field-title campaign-form-label-title" value="Dynamic Field" autocomplete="off">
                    <div class="form-underline"></div>
                  </div>
                </div>

                <nav role="toolbar" class="form-extra-button-area form-buttons-dynamic" aria-label="Dynamic Field ${index} Toolbar">
                  
                  <button type="button" class="form-button handle" aria-label="Drag">
                    <svg width="30px" height="30px" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                      <g stroke="none" class="icon-colour-var" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g id="drop" transform="translate(42.666667, 42.666667)">
                            <path d="M234.666667,256 L234.666667,341.333333 L277.333333,341.333333 L213.333333,426.666667 L149.333333,341.333333 L192,341.333333 L192,256 L234.666667,256 Z M341.333333,149.333333 L426.666667,213.333333 L341.333333,277.333333 L341.333333,234.666667 L256,234.666667 L256,192 L341.333333,192 L341.333333,149.333333 Z M85.3333333,149.333333 L85.3333333,192 L170.666667,192 L170.666667,234.666667 L85.3333333,234.666667 L85.3333333,277.333333 L3.55271368e-14,213.333333 L85.3333333,149.333333 Z M213.333333,3.55271368e-14 L277.333333,85.3333333 L234.666667,85.3333333 L234.666667,170.666667 L192,170.666667 L192,85.3333333 L149.333333,85.3333333 L213.333333,3.55271368e-14 Z" id="Combined-Shape"></path>
                          </g>
                        </g>
                    </svg>
                  </button>

                  <button id="html-preview-button" type="button" class="button form-button form-preview-button form-close">
                    HTML PREVIEW
                  </button>

                  <button id="form-delete-${index}" type="button" class="button form-button form-close">
                    <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                      <g stroke="none" stroke-width="1" fill-rule="evenodd">
                        <g transform="translate(91.520000, 91.520000)">
                          <polygon points="328.96 30.2933333 298.666667 1.42108547e-14 164.48 134.4 30.2933333 1.42108547e-14 1.42108547e-14 30.2933333 134.4 164.48 1.42108547e-14 298.666667 30.2933333 328.96 164.48 194.56 298.666667 328.96 328.96 298.666667 194.56 164.48"></polygon>
                        </g>
                      </g>
                    </svg>
                  </button>

                </nav> 

              </div>
              <p class="flavour-text" aria-label="Flavour Text">UWC-6-0${4 + index} //  Event::Dynamic Field</p>
            </div>
        
            <textarea name="dynamic_fields-${index-1}-value" 
            id="summernote-dynamic-${index}" 
            class="campaign-input large-input event-input">
            </textarea>

          </div>
        </div> 
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
  setDraggableItems(formArea);
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

// Create modals
const modal_1 = new Modal({
  modal: document.getElementById("help-modal-1"),
  button: document.getElementById("event-date-help-button"),
  span: document.getElementById("help-close-1"),
})

// const modal_2 = new Modal({
//   modal: document.getElementById("help-modal-2"),
//   button: document.getElementById("event-belligerents-help-button"),
//   span: document.getElementById("help-close-2"),
// })

const modal_3 = new Modal({
  modal: document.getElementById("help-modal-3"),
  button: document.getElementById("event-format-help-button"),
  span: document.getElementById("help-close-3"),
})

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
