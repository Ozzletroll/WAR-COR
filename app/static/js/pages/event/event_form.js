import { Modal } from "../../components/modal.js";
import { DynamicForm } from "../../components/form/dynamic_form.js";


// Create dynamic form 
const eventForm = new DynamicForm({
  basicButton: document.getElementById("new-basic-field-button"),
  textButton: document.getElementById("new-text-field-button"),
});
window.addNewField = eventForm.addHTMLField;

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
