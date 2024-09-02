import { Modal, PreviewModal } from "../modal.js";


export class DynamicField {
  constructor({
    type,
    element,
    index,
    parent
  }) {
    this.parent = parent;
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
        button: this.element.querySelector(".note-mybutton"),
        span: document.getElementById(`dynamic-preview-close-${this.index}`),
        editor: element,
      });
    }
    this.modalDeleteButton.onclick = event => {
      this.delete(event)
    }
    this.dragHandle = this.element.querySelector(".handle");
    this.dragState = false;
    this.initialiseKeyboardDrag();
    this.sizeButton = this.element.querySelector(".field-size-toggle");
    if (this.sizeButton != null) {
      this.state = this.sizeButton.checked;
      this.toggleLabel = this.element.querySelector(".size-toggle-label");
      this.sizeButton.onclick = event => {
        this.toggleSize();
      }
      this.toggleLabel.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          this.sizeButton.click();
        }
      });
      this.initialiseSize();
    }
  }

  delete() {
    this.closeModal.closeModal();
    this.closeModal.modal.remove();
    this.element.remove();
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
    var order = this.parent.fieldList.toArray();
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
    this.parent.fieldList.sort(order, true);
    this.parent.updateFieldOrder();
    this.parent.updateDraggableItems();

    // Reselect element
    this.element.focus();
  }

  initialiseSize() {
    if (this.state == false) {
      this.element.style.width = "";
      this.toggleLabel.innerHTML = `
          <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Expand Icon"
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
      this.element.style.width = "100%";
      this.toggleLabel.innerHTML = `
        <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Shrink Icon"
        version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
          <g stroke="none" stroke-width="1" fill-rule="evenodd">
              <g transform="translate(64.000000, 64.000000)">
                  <path d="M175.386477,217.309035 L175.36453,366.630013 L132.697864,366.630013 L132.697,290.401 L30.1698842,392.671075 L1.95399252e-14,362.501191 L102.796,259.963 L26.031197,259.963346 L26.0531439,217.309035 L175.386477,217.309035 Z M363.759612,2.84217094e-14 L393.929502,30.1698893 L291.381,131.975 L367.386477,131.975702 L367.386477,174.642368 L218.053144,174.642368 L218.053144,25.309035 L260.719811,25.309035 L260.719,102.294 L363.759612,2.84217094e-14 Z" id="Combined-Shape"></path>
              </g>
          </g>
        </svg>
        `
    }
  }

  toggleSize() {
    if (this.state == false) {
      this.element.style.transition = "0.15s";
      this.element.style.width = "100%";
      this.toggleLabel.innerHTML = `
          <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Shrink Icon"
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
      this.element.style.transition = "0.15s";
      this.element.style.width = "";
      this.toggleLabel.innerHTML = `
          <svg class="icon-colour-var" width="20px" height="20px" viewBox="0 0 512 512" aria-label="Expand Icon"
          version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
            <g stroke="none" stroke-width="1" fill-rule="evenodd">
                <g id="Combined-Shape" transform="translate(64.000000, 64.000000)">
                    <path d="M384,8.15703061e-12 L384,149.333333 L341.333333,149.333333 L341.333,73.103 L238.805354,175.374396 L208.63547,145.204512 L311.431,42.666 L234.666667,42.6666667 L234.666667,1.09174891e-11 L384,8.15703061e-12 Z M145.515738,209.223881 L175.685627,239.393771 L73.002,341.333 L149.333333,341.333333 L149.333333,384 L6.38067377e-12,384 L1.42108547e-14,234.666667 L42.6666667,234.666667 L42.666,311.328 L145.515738,209.223881 Z"></path>
                </g>
            </g>
          </svg>
        `
    }
    this.state = !this.state;
  }

}