import { checkLeftMarker } from '../../components/timeline/timeline_left_markers.js';
import { adjustEpochLine } from '../../components/timeline/epoch_line_adjust.js';
import { marginFix } from '../../components/timeline/margin_fix.js';
import { Modal } from '../../components/modal.js';
import { Toolbar } from '../../components/ui/ui_toolbar.js';
import { TimelineFooter } from '../../components/ui/footer.js';

// Offset epoch elements
adjustEpochLine();

// Fade in timeline area
var timeline = document.querySelector(".timeline-centring");
if (timeline != null) {
  timeline.style.visibility = "visible";
}

// Fix timeline element negative margins on safari iOS
window.addEventListener("resize", marginFix);
window.addEventListener("DOMContentLoaded", marginFix());

// Toggle display of left hand year marker
window.addEventListener("resize", checkLeftMarker);
checkLeftMarker();

// Add tooltips to ui toolbar
const toolbar = new Toolbar()

var editPageElem = document.getElementById("editPageVariable").getAttribute("editPage");
if (editPageElem == "true") {
  const footerModal = new Modal({
    modal: document.getElementById("help-modal-1"),
    button: document.getElementById("footer-help-button"),
    span: document.getElementById("help-close-1"),
  })
  const formFooter = new TimelineFooter({
    newButton: document.getElementById("footer-new-button"),
    menu: document.getElementById("footer-new-menu"),
  });
}

// Style all horus theme text elements
var horusElements = document.getElementsByClassName("summernote-horus");

Array.from(horusElements).forEach(element => {
  element.setAttribute("data-content", element.innerText);
});