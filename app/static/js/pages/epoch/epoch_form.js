import { Modal, PreviewModal } from "../../components/modal.js";
import { Form } from "../../components/form_edited.js";


// Create form edit check
const editEpochForm = new Form({
  form: "edit-epoch-form",
  fields: [
    "epoch-form-title",
    "epoch-form-start-date",
    "epoch-form-end-date",
    "summernote-overview",
    "summernote-desc"]
})

// Create modals
const modal_1 = new Modal({
  modal: document.getElementById("help-modal-1"),
  button: document.getElementById("epoch-start-button"),
  span: document.getElementById("help-close-1"),
})

const modal_2 = new Modal({
  modal: document.getElementById("help-modal-2"),
  button: document.getElementById("epoch-end-button"),
  span: document.getElementById("help-close-2"),
})

const modal_3 = new Modal({
  modal: document.getElementById("help-modal-3"),
  button: document.getElementById("epoch-overview-button"),
  span: document.getElementById("help-close-3"),
})

const modal_4 = new Modal({
  modal: document.getElementById("help-modal-4"),
  button: document.getElementById("epoch-desc-button"),
  span: document.getElementById("help-close-4"),
})

// HTML Preview Area Modal
const modal_preview = new PreviewModal({
  modal: document.getElementById("preview-modal-5"),
  button: document.getElementById("html-preview-button"),
  span: document.getElementById("preview-close-5"),
  editor: document.getElementById("epoch-desc-field")
})

// Only create delete modal if elements present (IE, we are actually on the edit epoch template)
const modalDeleteTest = document.getElementById("epoch-delete-button");
var modalDelete;
if (modalDeleteTest != null) {
  modalDelete = new Modal({
    modal: document.getElementById("epoch-modal-0"),
    button: document.getElementById("epoch-delete-button"),
    span: document.getElementById("epoch-close-0"),
  })
}

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
  if (event.target == modal_preview.modal) {
    modal_preview.closeModal();
  }
  if (modalDeleteTest != null) {
    if (event.target == modalDelete.modal) {
      modalDelete.closeModal();
    }
  }
}
