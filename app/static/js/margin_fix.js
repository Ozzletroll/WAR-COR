// Target safari browsers to fix timeline negative margin bug
function marginFix() {

    var is_safari = navigator.userAgent.indexOf("Safari") > -1 && navigator.userAgent.indexOf('Chrome') == -1;

    if (is_safari) {
        var timelines = document.getElementsByClassName("timeline-year-container");
        var timelineWidth = timelines[0].offsetWidth;
        for (var i = 0; i < timelines.length; i++) {
            timelines[i].style.marginRight = -0.5 * timelineWidth + "px";
        }
    }

}

