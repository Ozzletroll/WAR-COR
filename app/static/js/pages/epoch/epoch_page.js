import { checkLeftMarker } from '../../components/timeline/timeline_left_markers.js';
import { adjustEpochLine } from '../../components/timeline/epoch_line_adjust.js';
import { marginFix } from '../../components/timeline/margin_fix.js';
import { Toolbar } from '../../components/ui/ui_toolbar.js';
import { addHeaderIdMarker } from '../../components/header_id_marker.js';


// Add tooltips to ui toolbar
const toolbar = new Toolbar()

// Offset epoch elements
adjustEpochLine();

// Fix timeline element negative margins on safari iOS
window.addEventListener("resize", marginFix);
window.addEventListener("DOMContentLoaded", marginFix());

// Toggle display of left hand year marker
window.addEventListener("resize", checkLeftMarker);
checkLeftMarker();

// Add id's to user submitted header elements
var htmlFields = document.getElementsByClassName("event-page-description");
Array.from(htmlFields).forEach(field => {
  addHeaderIdMarker(field);
});

// Style all horus theme text elements
var horusElements = document.getElementsByClassName("summernote-horus");

Array.from(horusElements).forEach(element => {
  element.setAttribute("data-content", element.innerText);
});