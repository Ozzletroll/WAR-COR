import { Modal } from "../../components/modal.js";
import { DynamicForm } from "../../components/form/dynamic_form.js";
import { Footer} from "../../components/footer.js";


// Create dynamic form 
const epochForm = new DynamicForm({
  form: document.getElementById("edit-epoch-form"),
  basicButton: document.getElementById("new-basic-field-button"),
  textButton: document.getElementById("new-text-field-button"),
  belligerentsButton: document.getElementById("new-composite-field-button"),
});
window.addNewField = epochForm.addHTMLField;

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

const footerModal = new Modal({
  modal: document.getElementById("help-modal-4"),
  button: document.getElementById("footer-help-button"),
  span: document.getElementById("help-close-4"),
})

// Check if page has delete button and create modal instance
const modalDeleteTest = document.getElementById("epoch-delete-button");
var modalDelete;
if (modalDeleteTest != null) {
  modalDelete = new Modal({
    modal: document.getElementById("epoch-modal-0"),
    button: document.getElementById("epoch-delete-button"),
    span: document.getElementById("epoch-close-0"),
  })
}

// Create form footer
const formFooter = new Footer({
  formSubmitButton: document.getElementById("submit"),
  formDeleteButton: document.getElementById("epoch-delete-button"),
  updateButton: document.getElementById("footer-update-button"),
  deleteButton: document.getElementById("footer-delete-button"),
})
