// Get all timeline-year elements and hide the left marker element
// unless the years height exceeds the current viewport height
function checkLeftMarker() {
    
    const timelineYears = document.getElementsByClassName("timeline-year");
    Array.from(timelineYears).forEach(element => {
    
        var viewportHeight = window.innerHeight - 54; // - 54px navbar height
        var yearHeight = element.clientHeight;
        var leftMarker = element.querySelector(".timeline-left-marker");
    
        if (yearHeight >= viewportHeight) {
            leftMarker.style.visibility = "visible";
        }
        else {
            leftMarker.style.visibility = "hidden";
        }
        
    });
}

// Call function once on page load, then on screen resize
window.addEventListener("resize", checkLeftMarker);
checkLeftMarker();
