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
        else if(element.classList.contains("belligerents-field")) {
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
          })
        }

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

    updateBelligerentsFields() {
      this.fields.forEach(field => {
        if (field instanceof DynamicBelligerentsField) {
          field.updateFieldData();
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
    this.sizeButton = this.element.querySelector(".field-size-toggle");
    if (this.sizeButton != null) {
      this.state = this.sizeButton.checked;
      this.toggleLabel = this.element.querySelector(".size-toggle-label");
      this.sizeButton.onclick = event => {
        this.toggleSize();
      }
      this.initialiseSize();
    }
  }

  delete() {
    this.closeModal.closeModal();
    this.closeModal.modal.remove();
    this.element.remove();
  }

  initialiseSize() {
    if (this.state == false) {
      this.element.style.width = "";
      this.toggleLabel.innerHTML = `
        <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Expand Icon"
        version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <g stroke="none" stroke-width="1" fill-rule="evenodd">
              <g transform="translate(64.000000, 64.000000)">
                  <path d="M175.386477,217.309035 L175.36453,366.630013 L132.697864,366.630013 L132.697,290.401 L30.1698842,392.671075 L1.95399252e-14,362.501191 L102.796,259.963 L26.031197,259.963346 L26.0531439,217.309035 L175.386477,217.309035 Z M363.759612,2.84217094e-14 L393.929502,30.1698893 L291.381,131.975 L367.386477,131.975702 L367.386477,174.642368 L218.053144,174.642368 L218.053144,25.309035 L260.719811,25.309035 L260.719,102.294 L363.759612,2.84217094e-14 Z" id="Combined-Shape"></path>
              </g>
          </g>
        </svg>
      `
    }
    else {
      this.element.style.width = "100%";
      this.toggleLabel.innerHTML = `
        <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Shrink Icon"
        version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <g stroke="none" stroke-width="1" fill-rule="evenodd">
              <g id="Combined-Shape" transform="translate(64.000000, 64.000000)">
                  <path d="M384,8.15703061e-12 L384,149.333333 L341.333333,149.333333 L341.333,73.103 L238.805354,175.374396 L208.63547,145.204512 L311.431,42.666 L234.666667,42.6666667 L234.666667,1.09174891e-11 L384,8.15703061e-12 Z M145.515738,209.223881 L175.685627,239.393771 L73.002,341.333 L149.333333,341.333333 L149.333333,384 L6.38067377e-12,384 L1.42108547e-14,234.666667 L42.6666667,234.666667 L42.666,311.328 L145.515738,209.223881 Z"></path>
              </g>
          </g>
        </svg>
      `
    }
  }

  toggleSize() {
    if (this.state == false) {
      this.element.style.width = "100%";
      this.toggleLabel.innerHTML = `
        <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Shrink Icon"
        version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <g stroke="none" stroke-width="1" fill-rule="evenodd">
              <g id="Combined-Shape" transform="translate(64.000000, 64.000000)">
                  <path d="M384,8.15703061e-12 L384,149.333333 L341.333333,149.333333 L341.333,73.103 L238.805354,175.374396 L208.63547,145.204512 L311.431,42.666 L234.666667,42.6666667 L234.666667,1.09174891e-11 L384,8.15703061e-12 Z M145.515738,209.223881 L175.685627,239.393771 L73.002,341.333 L149.333333,341.333333 L149.333333,384 L6.38067377e-12,384 L1.42108547e-14,234.666667 L42.6666667,234.666667 L42.666,311.328 L145.515738,209.223881 Z"></path>
              </g>
          </g>
        </svg>
      `
    }
    else {
      this.element.style.width = "";
      this.toggleLabel.innerHTML = `
        <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Expand Icon"
        version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <g stroke="none" stroke-width="1" fill-rule="evenodd">
              <g transform="translate(64.000000, 64.000000)">
                  <path d="M175.386477,217.309035 L175.36453,366.630013 L132.697864,366.630013 L132.697,290.401 L30.1698842,392.671075 L1.95399252e-14,362.501191 L102.796,259.963 L26.031197,259.963346 L26.0531439,217.309035 L175.386477,217.309035 Z M363.759612,2.84217094e-14 L393.929502,30.1698893 L291.381,131.975 L367.386477,131.975702 L367.386477,174.642368 L218.053144,174.642368 L218.053144,25.309035 L260.719811,25.309035 L260.719,102.294 L363.759612,2.84217094e-14 Z" id="Combined-Shape"></path>
              </g>
          </g>
        </svg>
      `
    }
    this.state = !this.state;
  }

}


class DynamicBelligerentsField extends DynamicField {
  constructor({
    type,
    element,
    index,
    parent
  }) {
    super({type, element, index});
    this._columnIndex = 0;
    this.columns = [];
    this.columnList = [];
    this.parent = parent;
    this.tableElement = this.element.querySelector(".belligerents-table");
    this.newColumnButton = this.element.querySelector(".new-group-button");
    this.valueField = this.element.querySelector(".belligerents-hidden-value");

    this.addColumn = this.addColumn.bind(this);
    this.newColumnButton.addEventListener("click", this.addColumn);

    this.getColumns();
    this.updateDraggableColumns();
  }

  get columnIndex() {
    return ++this._columnIndex;
  }

  getColumns() {
    var existingColumns = this.element.querySelectorAll(".belligerents-column");

    if (existingColumns != null) {
      Array.from(existingColumns).forEach(column => {
        var columnIndex = this.columnIndex;
        var newColumn = new BelligerentsColumn({
          index: columnIndex,
          parentIndex: this.index,
          element: column,
          parentClass: this,
        })
        this.columns.push(newColumn);
      })
    }
  }

  addColumn() {
    var columnIndex = this.columnIndex;
    this.tableElement.insertAdjacentHTML("beforeend", createBelligerentsColumnHTML(this.index, columnIndex));
    var newColumn = new BelligerentsColumn({
      index: columnIndex,
      parentIndex: this.index,
      element: this.element.querySelector(`#belligerents-column-${this.index}-${columnIndex}`),
      parentClass: this,
    })
    newColumn.addCell();
    this.columns.push(newColumn);

    // Destroy the existing SortableJS instance to prevent iOS devices breaking
    this.columnList.destroy();
    this.updateDraggableColumns();
  }

  updateDraggableColumns() {
    this.columnList = new Sortable(this.element.querySelector(".belligerents-table"), {
      handle: ".belligerents-handle",
      animation: 150,
      onEnd: (event) => {
        this.updateColumnOrder();
        this.parent.fieldDataChanged = true;
        this.updateFieldData();
      }
    });
  }

  updateColumnOrder() {
    var columnElements = this.element.querySelectorAll(".belligerents-column");
    Array.from(columnElements).forEach((column, index) => {
      var positionField = column.querySelector(".column-position");
      positionField.value = index + 1;
    });
  }

  updateFieldData() {

    var formData = [];
    this.columns.forEach(column => {

      var columnData = {
        title: column.title,
        position: column.position,
        entries: [],
      };
      
      column.cells.forEach(cell => {
        columnData["entries"].push(cell.value) 
      });

      formData.push(columnData);

    });
    this.valueField.value = JSON.stringify(formData);
  }
}


class BelligerentsColumn {
  constructor({
    index,
    parentIndex,
    element,
    parentClass
  })
  {
    this.parentClass = parentClass;
    this._cellIndex = 0;
    this.index = index;
    this.parentIndex = parentIndex;
    this.element = element;
    this.titleField = element.querySelector(".column-header-text");
    this.positionField = element.querySelector(".column-position");
    this._title = "";
    this._position = 0;
    this.cells = [];
    this.deleteColumnButton = element.querySelector(".form-close")
    this.newBelligerentButton = element.querySelector(".new-belligerent-button");

    this.addCell = this.addCell.bind(this);
    this.newBelligerentButton.addEventListener("click", this.addCell);

    this.delete = this.delete.bind(this);
    this.deleteColumnButton.addEventListener("click", this.delete); 

    this.getCells();
  }

  get cellIndex() {
    return ++this._cellIndex;
  }

  get title() {
    return this.titleField.value;
  }

  get position() {
    return this.positionField.value;
  }

  getCells() {
    var existingCells = this.element.querySelectorAll(".belligerent-cell");

    if (existingCells != null) {
      Array.from(existingCells).forEach(cell => {
        var cellIndex = this.cellIndex;
        var newCell = new BelligerentsCell({
          index: cellIndex,
          parentIndex: this.parentIndex,
          element: cell,
          parentClass: this,
        })
        this.cells.push(newCell);
      })
    }
  }

  addCell() {
    var cellIndex = this.cellIndex;
    this.element.querySelector(".column-body").insertAdjacentHTML("beforeend", createBelligerentsCellHTML(this.parentIndex, this.index, cellIndex));
    var newCell = new BelligerentsCell({
      index: cellIndex,
      parentIndex: this.parentIndex,
      element: this.element.querySelector(`#belligerent-cell-${this.parentIndex}-${this.index}-${cellIndex}`),
      parentClass: this,
    })
    this.cells.push(newCell);
  }

  delete() {
    this.element.remove();
    this.parentClass.columns = this.parentClass.columns.filter(item => item != this);
    this.parentClass.updateColumnOrder();
    this.parentClass.parent.fieldDataChanged = true;
    this.parentClass.updateFieldData();
  }

}


class BelligerentsCell {
  constructor({
    index,
    parentIndex,
    element,
    parentClass
  })
  {
    this.parentClass = parentClass;
    this.index = index;
    this.parentIndex = parentIndex;
    this.element = element;
    this.field = element.querySelector(".belligerent-input");
    this._value = "";

    this.deleteButton = this.element.querySelector(".belligerents-remove");
    this.delete = this.delete.bind(this);
    this.deleteButton.addEventListener("click", this.delete);
  }

  get value() {
    return this.field.value;
  }

  delete() {
    this.element.remove()
    this.parentClass.cells = this.parentClass.cells.filter(item => item != this);
  }
}
