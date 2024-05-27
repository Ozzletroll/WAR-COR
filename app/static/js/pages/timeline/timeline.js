import { checkLeftMarker } from '../../components/timeline/timeline_left_markers.js';
import { adjustEpochLine } from '../../components/timeline/epoch_line_adjust.js';
import { marginFix } from '../../components/timeline/margin_fix.js';
import { Modal } from '../../components/modal.js';
import { TimelineFooter } from '../../components/footer.js';

// Offset epoch elements
adjustEpochLine();

// Fix timeline element negative margins on safari iOS
window.addEventListener("resize", marginFix);
window.addEventListener("DOMContentLoaded", marginFix());

// Toggle display of left hand year marker
window.addEventListener("resize", checkLeftMarker);
checkLeftMarker();

var editPageElem = document.getElementById("editPageVariable").getAttribute("editPage");
if (editPageElem == "true") {
  const footerModal = new Modal({
    modal: document.getElementById("help-modal-1"),
    button: document.getElementById("footer-help-button"),
    span: document.getElementById("help-close-1"),
  })
}

// Create footer
const formFooter = new TimelineFooter();
