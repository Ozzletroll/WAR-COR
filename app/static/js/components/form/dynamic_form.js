import { createTextFieldHTML } from "./dynamic_field_templates/html_field_template.js";
import { createBasicFieldHTML } from "./dynamic_field_templates/basic_field_template.js";
import { 
  createBelligerentsFieldHTML, 
  createBelligerentsColumnHTML, 
  createBelligerentsCellHTML 
} from "./dynamic_field_templates/belligerents_field_template.js";
import { createDeleteModal } from "./modal_templates/close_modal_template.js";
import { summernoteInitialise } from "../summernote_initialise.js";
import { Modal, PreviewModal } from "../modal.js";
import { createHTMLPreviewModal } from "./modal_templates/html_preview_modal.js";


export class DynamicForm {
    constructor({
      basicButton,
      textButton,
      belligerentsButton
    }) {
      this._idValue = 0;
      this.basicButton = basicButton;
      this.textButton = textButton;
      this.belligerentsButton = belligerentsButton;
      this.fieldList;
      this.formArea = document.getElementById("dynamic-field-area");
      this.fields = this.getDynamicFields();
      this.fieldDataChanged = false;

      this.updateDraggableItems(this.formArea);
      this.bindSummernoteModalEvents();

      // Bind "this" to the instance for the new field methods
      this.addBasicField = this.addBasicField.bind(this);
      this.basicButton.addEventListener("click", this.addBasicField);

      this.addHTMLField = this.addHTMLField.bind(this);
      this.textButton.addEventListener("click", this.addHTMLField);

      this.addBelligerentsField = this.addBelligerentsField.bind(this);
      this.belligerentsButton.addEventListener("click", this.addBelligerentsField);

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
        this.addNewDeleteModal(index + 1);
        var newField = new DynamicField({
          form: this,
          type: fieldType,
          element: element,
          index: this.idValue,
        })
        fields.push(newField);
    })
      return fields;
    }

    addBasicField() {
      // Create page elements and insert in DOM
      var fieldID = this.idValue;
      this.formArea.insertAdjacentHTML("beforeend", createBasicFieldHTML(fieldID));
      
      // Insert modals into DOM
      this.addNewDeleteModal(fieldID);

      // Create instance of Field class
      var newField = new DynamicField({
        type: "basic",
        element: document.getElementById(`event-dynamic-field-${fieldID}`),
        index: fieldID,
      })
      this.fields.push(newField);

      // Destroy the existing SortableJS instance to prevent iOS devices breaking
      this.fieldList.destroy();

      // Re-initialize SortableJS
      this.updateDraggableItems(this.formArea);
    }

    addHTMLField() {
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
        true,
        true
      );

      // Add event listeners to all summernote modals
      this.bindSummernoteModalEvents();

      // Create instance of Field class
      var newField = new DynamicField({
        type: "text",
        element: document.getElementById(`event-dynamic-field-${fieldID}`),
        index: fieldID,
      })
      this.fields.push(newField);

      // Destroy the existing SortableJS instance to prevent iOS devices breaking
      this.fieldList.destroy();

      // Re-initialize SortableJS
      this.updateDraggableItems(this.formArea);
    }

    addBelligerentsField() {
      // Create page elements and insert in DOM
      var fieldID = this.idValue;
      this.formArea.insertAdjacentHTML("beforeend", createBelligerentsFieldHTML(fieldID));
      
      // Insert modals into DOM
      this.addNewDeleteModal(fieldID);

      // Create instance of Field class
      var newField = new DynamicBelligerentsField({
        type: "belligerents",
        element: document.getElementById(`event-dynamic-field-${fieldID}`),
        index: fieldID,
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

    updateDraggableItems(formArea) {
      this.fieldList = new Sortable(formArea, {
          handle: ".handle",
          animation: 150,
          onEnd: (event) => {
              var items = event.from.getElementsByClassName("dynamic-field");
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
      });
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
      var formInputs = document.getElementsByClassName("form-input");
      var checkboxes = document.getElementsByClassName("input-checkbox");

      var fields = Array.from(formInputs).concat(Array.from(checkboxes));
      fields.forEach(field => {
        field.addEventListener("change", function() {
          this.fieldDataChanged = true;
        }.bind(this));
      });

      $(document).on("summernoteFieldChanged", (function(event, content) {
        this.fieldDataChanged = true;
      }).bind(this));
    }

    bindSubmitButtonEvents () {
      var excludedButtons = document.getElementsByClassName("campaign-submit");
      Array.from(excludedButtons).forEach(button => {
        button.addEventListener("click", function() {
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
  }


class DynamicField {
  constructor({
    type,
    element,
    index,
  }) {
    this.type = type;
    this.element = element;
    this.index = index;
    this.closeModal = new Modal({
      modal: document.getElementById(`dynamic-delete-modal-${this.index}`),
      button: document.getElementById(`dynamic-delete-button-${this.index}`),
      span: document.getElementById(`dynamic-delete-close-${this.index}`),
    });
    this.modalDeleteButton = document.getElementById(`dynamic-delete-confirm-${this.index}`);
    if (this.type == "text") {
      this.previewModal = new PreviewModal({
        modal: document.getElementById(`dynamic-preview-modal-${this.index}`),
        button: document.getElementById(`dynamic-preview-button-${this.index}`),
        span: document.getElementById(`dynamic-preview-close-${this.index}`),
        editor: element,
      });
    }
    this.modalDeleteButton.onclick = event => {
      this.delete(event)
    } 
  }

  delete() {
    this.closeModal.closeModal();
    this.closeModal.modal.remove();
    this.element.remove();
  }

}


class DynamicBelligerentsField extends DynamicField {
  constructor({
    type,
    element,
    index
  }) {
    super({type, element, index});
    this._columnIndex = 0;
    this.columns = [];
    this.tableElement = this.element.querySelector(".belligerents-table");
    this.newColumnButton = this.element.querySelector(".new-group-button");

    this.addColumn = this.addColumn.bind(this);
    this.newColumnButton.addEventListener("click", this.addColumn);
  }

  get columnIndex() {
    return ++this._columnIndex;
  }

  addColumn() {
    var columnIndex = this.columnIndex;
    this.tableElement.insertAdjacentHTML("beforeend", createBelligerentsColumnHTML(this.index, columnIndex));
    var newColumn = new BelligerentsColumn({
      index: columnIndex,
      parentIndex: this.index,
      element: this.element.querySelector(`#belligerents-column-${this.index}-${columnIndex}`),
    })
    newColumn.addCell();
    this.columns.push(newColumn);
  }

  deleteColumn() {
    
  }
}


class BelligerentsColumn {
  constructor({
    index,
    parentIndex,
    element,
  })
  {
    this._cellIndex = 0;
    this.index = index;
    this.parentIndex = parentIndex;
    this.element = element;
    this.cells = [];
    this.newBelligerentButton = element.querySelector(".new-belligerent-button");

    this.addCell = this.addCell.bind(this);
    this.newBelligerentButton.addEventListener("click", this.addCell);
    
  }

  get cellIndex() {
    return ++this._cellIndex;
  }

  addCell() {
    var cellIndex = this.cellIndex;
    this.element.insertAdjacentHTML("beforeend", createBelligerentsCellHTML(this.parentIndex, this.index, cellIndex));
    var newCell = new BelligerentsCell({
      index: cellIndex,
      parentIndex: this.parentIndex,
      element: this.element.querySelector(`#belligerent-cell-${this.parentIndex}-${this.index}-${cellIndex}`),
    })
    this.cells.push(newCell);
    
  }

}


class BelligerentsCell {
  constructor({
    index,
    parentIndex,
    element,
  })
  {
    this.index = index;
    this.parentIndex = parentIndex;
    this.element = element;

    this.deleteButton = this.element.querySelector(".belligerents-remove");
    this.delete = this.delete.bind(this);
    this.deleteButton.addEventListener("click", this.delete);
  }

  delete() {
    this.element.remove()
  }

}
