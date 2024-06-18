import { checkLeftMarker } from '../../components/timeline/timeline_left_markers.js';
import { adjustEpochLine } from '../../components/timeline/epoch_line_adjust.js';
import { marginFix } from '../../components/timeline/margin_fix.js';
import { Toolbar } from '../../components/ui/ui_toolbar.js';


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
