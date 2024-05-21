import { Modal } from "../../components/modal.js";
import { DynamicForm } from "../../components/form/dynamic_form.js";
import { Footer} from "../../components/footer.js";


// Create dynamic form 
const eventForm = new DynamicForm({
  form: document.getElementById("edit-event-form"),
  basicButton: document.getElementById("new-basic-field-button"),
  textButton: document.getElementById("new-text-field-button"),
  belligerentsButton: document.getElementById("new-composite-field-button"),
});
window.addNewField = eventForm.addHTMLField;

// Create modals
const modal1 = new Modal({
  modal: document.getElementById("help-modal-1"),
  button: document.getElementById("event-date-help-button"),
  span: document.getElementById("help-close-1"),
})

const modal2 = new Modal({
  modal: document.getElementById("help-modal-2"),
  button: document.getElementById("event-format-help-button"),
  span: document.getElementById("help-close-2"),
})

const footerModal = new Modal({
  modal: document.getElementById("help-modal-3"),
  button: document.getElementById("footer-help-button"),
  span: document.getElementById("help-close-3"),
})

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

// Create form footer
const formFooter = new Footer({
  formSubmitButton: document.getElementById("submit"),
  formDeleteButton: document.getElementById("event-delete-button"),
  updateButton: document.getElementById("footer-update-button"),
  deleteButton: document.getElementById("footer-delete-button"),
})
