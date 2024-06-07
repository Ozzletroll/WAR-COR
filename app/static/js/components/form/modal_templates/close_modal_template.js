export function createDeleteModal(index) {
    return `
      <div id="dynamic-delete-modal-${index}" class="modal dynamic-delete-modal">
        <div class="modal-content modal-content-small" role="dialog" aria-label="Confirm Delete Field" aria-modal="false" tabindex="-1">
          <div class="modal-content-inner">
            <div class="modal-header">
              <h2 class="modal-header-small">Delete Field</h2>
              <button id="dynamic-delete-close-${index}" class="modal-close" aria-label="Close Modal">
                <img class="icon" aria-label="Close Icon" src="/static/images/icons/cancel.svg">
              </button>
            </div>
            <div class="modal-body modal-body-small">
              
                <p class="flavour-text modal-flavour" aria-label="Flavour Text">CNF-07-${index} // FIELD::DELETE</p>
                <p class="modal-text modal-text-upper">
                  Confirm deletion of dynamic field. This action cannot be undone.
                </p>
                <button id="dynamic-delete-confirm-${index}" class="button modal-confirm-button field-delete-button">REMOVE FIELD</button>

            </div>
          </div>
        </div>
      </div>
    `;
  }
