// Target safari browsers to fix timeline negative margin bug
function marginFix() {

    var is_safari = navigator.userAgent.indexOf("Safari") > -1 && navigator.userAgent.indexOf('Chrome') == -1;

    if (is_safari) {
        var timelines = document.getElementsByClassName("timeline-year-container");
        var timelineWidth = timelines[0].offsetWidth;
        for (var i = 0; i < timelines.length; i++) {
            timelines[i].style.marginRight = -0.5 * timelineWidth + "px";
        }

        // Adjust year label back into position
        var yearLabels = document.getElementsByClassName("timeline-year-header");
        for (var i = 0; i < yearLabels.length; i++) {
            var labelWidth = yearLabels[i].offsetWidth;
            // 50% of self width - 5% left offset of timeline-year-outer-container
            yearLabels[i].style.marginRight = 0.45 * labelWidth + "px";
        }

    }

}
