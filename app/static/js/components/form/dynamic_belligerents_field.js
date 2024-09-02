import { DynamicField } from "./dynamic_field.js";
import { 
  createBelligerentsColumnHTML, 
  createBelligerentsCellHTML 
} from "./dynamic_field_templates/belligerents_field_template.js";


export class DynamicBelligerentsField extends DynamicField {
  constructor({
    type,
    element,
    index,
    parent
  }) {
    super({ type, element, index });
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
      dataIdAttr: "id",
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
  }) {
    this.parentClass = parentClass;
    this._cellIndex = 0;
    this.index = index;
    this.parentIndex = parentIndex;
    this.element = element;
    this.dragHandle = this.element.querySelector(".belligerents-handle");
    this.initialiseKeyboardDrag();
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

  initialiseKeyboardDrag() {

    this.element.addEventListener("keypress", (event) => {
      if (event.key === "Enter" && document.activeElement === this.element) {
        event.stopPropagation();
        event.preventDefault();
        this.element.blur();
        this.dragHandle.focus();
      }
    });

    // Add enter key listener to focus element
    this.dragHandle.addEventListener("keypress", (event) => {
      if (event.key === "Enter") {
        event.stopPropagation();
        event.preventDefault();
        this.element.tabIndex = 0;
        this.element.focus();
      }
    });

    // Add up/down key listener to move focussed element
    this.element.addEventListener("keydown", (event) => {
      // Check if element is focussed
      if (document.activeElement === this.element) {
        var code = event.which || event.keyCode;
        if (code === 38) {
          this.moveElement("up");
        } else if (code === 40) {
          this.moveElement("down");
        }
      }
    });

    // Remove from tab index when not active
    this.element.addEventListener("blur", () => {
      this.element.tabIndex = -1;
    });

  }

  moveElement(direction) {

    var sortableId = this.element.id;
    var order = this.parentClass.columnList.toArray();
    var index = order.indexOf(sortableId);

    // Prevent moving first item upwards
    if (index == 0 && direction == "up") {
      return
    }

    // Remove the selected item from the order
    order.splice(index, 1)

    // Insert back into the new position
    if (direction == "down") {
      order.splice(index + 1, 0, sortableId)
    } else if (direction == "up") {
      order.splice(index - 1, 0, sortableId)
    }

    // Sort fieldList into new order
    this.parentClass.columnList.sort(order, true);
    this.parentClass.updateColumnOrder();
    this.parentClass.updateDraggableColumns();

    // Reselect element
    this.element.focus();
  }

}


class BelligerentsCell {
  constructor({
    index,
    parentIndex,
    element,
    parentClass
  }) {
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