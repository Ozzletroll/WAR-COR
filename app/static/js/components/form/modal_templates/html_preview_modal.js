export function createHTMLPreviewModal(index, fieldTitle) {
  return `
    <div id="dynamic-preview-modal-${index}" class="modal dynamic-preview-modal">
      <div class="modal-content modal-preview-content" role="dialog" aria-label="{{ aria_label }}" aria-modal="false" tabindex="-1">
        <div class="modal-content-inner">
          <div class="modal-header">
            <h2 class="modal-header-small">HTML PREVIEW</h2>
            <button id="dynamic-preview-close-${index}" class="modal-close" aria-label="Close Modal">
              <img class="icon" aria-label="Close Icon" src="/static/images/icons/cancel.svg">
            </button>
          </div>
          <div class="modal-body modal-preview-overflow">
            <div class="event-page-elem event-elem-large elem-body event-page-description">
              <div class="entry-left-padding"></div>
              <div class="description-body">
                <h4 class="event-desc-header dynamic-preview-header"></h4>
                <div class="event-desc">
                  <div id="preview-modal-body-${index}" class="modal-body modal-body-preview">
                    
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}
