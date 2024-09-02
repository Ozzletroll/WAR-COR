import { DynamicField } from "./dynamic_field.js";
import { DynamicBelligerentsField } from "./dynamic_belligerents_field.js";
import { createTextFieldHTML } from "./dynamic_field_templates/html_field_template.js";
import { createBasicFieldHTML } from "./dynamic_field_templates/basic_field_template.js";
import { createBelligerentsFieldHTML } from "./dynamic_field_templates/belligerents_field_template.js";
import { createDeleteModal } from "./modal_templates/close_modal_template.js";
import { summernoteInitialise } from "../summernote_initialise.js";
import { createHTMLPreviewModal } from "./modal_templates/html_preview_modal.js";


export class DynamicForm {
  constructor({
    form,
    basicButton,
    textButton,
    belligerentsButton
  }) {
    this._idValue = 0;
    this.basicButton = basicButton;
    this.textButton = textButton;
    this.belligerentsButton = belligerentsButton;
    this.form = form,
      this.fieldList;
    this.formArea = document.getElementById("dynamic-field-area");
    this.fields = this.getDynamicFields();
    this.fieldDataChanged = false;

    this.updateDraggableItems();
    this.bindSummernoteModalEvents();

    // Bind "this" to the instance for the new field methods
    this.addBasicField = this.addBasicField.bind(this);
    this.basicButton.addEventListener("click", this.addBasicField);

    this.addHTMLField = this.addHTMLField.bind(this);
    this.textButton.addEventListener("click", this.addHTMLField);

    this.addBelligerentsField = this.addBelligerentsField.bind(this);
    this.belligerentsButton.addEventListener("click", this.addBelligerentsField);

    this.updateBelligerentsFields = this.updateBelligerentsFields.bind(this);
    this.form.addEventListener("submit", this.updateBelligerentsFields)

    this.bindFieldChangeEvents();
    this.bindUnsavedChangesWarning();
    this.bindSubmitButtonEvents();
  }

  get idValue() {
    return ++this._idValue;
  }

  getDynamicFields() {
    var fields = [];
    var dynamicFields = document.getElementsByClassName("dynamic-field");
    Array.from(dynamicFields).forEach((element, index) => {
      var fieldType;
      if (element.classList.contains("html-field")) {
        fieldType = "text";
        this.addPreviewModal(index + 1);
      }
      else if (element.classList.contains("basic-field")) {
        fieldType = "basic";
      }
      else if (element.classList.contains("belligerents-field")) {
        fieldType = "belligerents";
      }
      this.addNewDeleteModal(index + 1);

      if (fieldType == "belligerents") {
        var newField = new DynamicBelligerentsField({
          form: this,
          type: "belligerents",
          element: element,
          index: this.idValue,
          parent: this,
        })
      }
      else {
        var newField = new DynamicField({
          form: this,
          type: fieldType,
          element: element,
          index: this.idValue,
          parent: this
        })
      }

      fields.push(newField);
    })
    return fields;
  }

  addBasicField() {
    // Flag changes
    this.fieldDataChanged = true;

    // Create page elements and insert in DOM
    var fieldID = this.idValue;
    this.formArea.insertAdjacentHTML("beforeend", createBasicFieldHTML(fieldID));

    // Insert modals into DOM
    this.addNewDeleteModal(fieldID);

    // Create instance of Field class
    var newField = new DynamicField({
      type: "basic",
      element: document.getElementById(`dynamic-field-${fieldID}`),
      index: fieldID,
      parent: this,
    })
    this.fields.push(newField);

    // Destroy the existing SortableJS instance to prevent iOS devices breaking
    this.fieldList.destroy();

    // Re-initialize SortableJS
    this.updateDraggableItems(this.formArea);
  }

  addHTMLField() {
    // Flag changes
    this.fieldDataChanged = true;

    // Create page elements and insert in DOM
    var fieldID = this.idValue;
    this.formArea.insertAdjacentHTML("beforeend", createTextFieldHTML(fieldID));

    // Insert modals into DOM
    this.addNewDeleteModal(fieldID);
    this.addPreviewModal(fieldID);

    // Initialise new summernote editor
    var id = `-dynamic-${fieldID}`;
    summernoteInitialise(
      id,
      "OPTIONAL",
      null,
      "True",
      "True",
      "True"
    );

    // Add event listeners to all summernote modals
    this.bindSummernoteModalEvents();

    // Create instance of Field class
    var newField = new DynamicField({
      type: "text",
      element: document.getElementById(`dynamic-field-${fieldID}`),
      index: fieldID,
      parent: this,
    })
    this.fields.push(newField);

    // Destroy the existing SortableJS instance to prevent iOS devices breaking
    this.fieldList.destroy();

    // Re-initialize SortableJS
    this.updateDraggableItems(this.formArea);
  }

  addBelligerentsField() {
    // Flag changes
    this.fieldDataChanged = true;

    // Create page elements and insert in DOM
    var fieldID = this.idValue;
    this.formArea.insertAdjacentHTML("beforeend", createBelligerentsFieldHTML(fieldID));

    // Insert modals into DOM
    this.addNewDeleteModal(fieldID);

    // Create instance of Field class
    var newField = new DynamicBelligerentsField({
      type: "belligerents",
      element: document.getElementById(`dynamic-field-${fieldID}`),
      index: fieldID,
      parent: this,
    })
    this.fields.push(newField);

    // Destroy the existing SortableJS instance to prevent iOS devices breaking
    this.fieldList.destroy();

    // Re-initialize SortableJS
    this.updateDraggableItems(this.formArea);
  }

  addPreviewModal(index) {
    document.body.insertAdjacentHTML("beforeend", createHTMLPreviewModal(index));
  }

  addNewDeleteModal(index) {
    document.body.insertAdjacentHTML("beforeend", createDeleteModal(index));
  }

  updateDraggableItems() {
    this.fieldList = new Sortable(this.formArea, {
      dataIdAttr: "id",
      handle: ".handle",
      animation: 150,
      onEnd: (event) => {
        this.updateFieldOrder();
      }
    });
  }

  updateFieldOrder() {
    var items = this.form.getElementsByClassName("dynamic-field");

    // Update id's and names to match new positions
    for (var index = 0; index < items.length; index++) {
      items[index].id = "dynamic-field-" + (index + 1);
    }

    for (var index = 0; index < items.length; index++) {
      var inputs = items[index].getElementsByTagName("input");
      for (var index2 = 0; index2 < inputs.length; index2++) {
        inputs[index2].name = inputs[index2].name.replace(/dynamic_fields-\d+-/, "dynamic_fields-" + index + "-");
      }
      var textAreas = items[index].getElementsByTagName("textarea");
      for (var index3 = 0; index3 < textAreas.length; index3++) {
        textAreas[index3].name = textAreas[index3].name.replace(/dynamic_fields-\d+-/, "dynamic_fields-" + index + "-");
      }
    }

    this.fieldDataChanged = true;
  }

  bindSummernoteModalEvents() {
    var summernoteModals = document.getElementsByClassName("note-modal");
    Array.from(summernoteModals).forEach(modal => {
      var modalCloseButton = modal.querySelector(".close");
      modal.addEventListener("click", (event) => {
        if (event.target.classList.contains("note-modal")) {
          modalCloseButton.click();
        }
      });
    });
  }

  bindFieldChangeEvents() {
    var formInputs = this.form.querySelectorAll(".form-input");
    var checkboxes = this.form.querySelectorAll(".input-checkbox");

    var fields = Array.from(formInputs).concat(Array.from(checkboxes));
    fields.forEach(field => {
      field.addEventListener("change", function () {
        this.fieldDataChanged = true;
      }.bind(this));
    });

    $(document).on("summernoteFieldChanged", (function (event, content) {
      this.fieldDataChanged = true;
    }).bind(this));
  }

  bindSubmitButtonEvents() {
    var excludedButtons = document.getElementsByClassName("campaign-submit");
    Array.from(excludedButtons).forEach(button => {
      button.addEventListener("click", function () {
        this.fieldDataChanged = false;
      }.bind(this));
    })
  }

  bindUnsavedChangesWarning() {
    window.addEventListener("beforeunload", (event) => {
      if (this.fieldDataChanged) {
        event.preventDefault();
      }
    });
  }

  updateBelligerentsFields() {
    this.fields.forEach(field => {
      if (field instanceof DynamicBelligerentsField) {
        field.updateFieldData();
      }
    });
  }
}
