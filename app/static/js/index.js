// Animate horizontal line on load
function animateHR(horizontalLine) {
  var horizontalLine = document.getElementById("title-hr");
  horizontalLine.style.width = "50%";
}
window.addEventListener("load", animateHR);

// Store timeout function so it can be cleared when screen returns to pos 0
var timeout;

// Get navbar and hide box-shadow if at position 0
// Hide down arrow if not a at position 0
function checkScrollPos () {
  var navbar = document.getElementById("navbar");
  var downArrow = document.getElementById("down-arrow");
  
  if (window.scrollY == 0) {
    navbar.style.boxShadow = "none";
    downArrow.style.opacity = "";
    downArrow.style.display = "flex";

    // Clear timeout
    clearTimeout(timeout);
  }
  else {
    navbar.style.boxShadow = "";
    navbar.style.transition = "box-shadow 0.5s ease";
    downArrow.style.opacity = "0";

    // Clear the timeout to prevent multiple timeouts from being set
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      downArrow.style.display = "none";
    }, 300);
  }
}

window.addEventListener("DOMContentLoaded", checkScrollPos);
window.addEventListener("scroll", checkScrollPos);

// Features area animations

// Main animation controller
function animateTimelineDemo() {

  var speedMultiplier = 0.3;

  var timings = {
    "fade-group-1": 1000 * speedMultiplier,
    "fade-group-2": 2000 * speedMultiplier,
    "fade-group-3": 3000 * speedMultiplier,
    "fade-group-4": 4000 * speedMultiplier,
    "fade-group-5": 5000 * speedMultiplier,
    "fade-group-6": 6000 * speedMultiplier,
    "fade-group-7": 7000 * speedMultiplier,
    "fade-group-8": 8000 * speedMultiplier,
  };

  // For each keyframe timing, trigger animation on element
  for (const [element, timing] of Object.entries(timings)) {
    fadeInElement(element, timing)
  }

}
// Fade in animations for features area
function fadeInElement(element, timing) {

  setTimeout(function() {
    var elements = document.getElementsByClassName(element);
    Array.from(elements).forEach((element) => {
      element.classList.add("fade-in-recursive");
    });
  }, timing);

}


// Fade in features elements when visible
const header = document.getElementById("features-header");
const paragraph = document.getElementById("features-paragraph");

function checkHeaderVisible() {
  const elementPosition = header.getBoundingClientRect().top;
  const windowHeight = window.innerHeight;

  if (elementPosition < windowHeight) {
    header.classList.add("hero-fade");
    animateTimelineDemo();
  }
}

checkHeaderVisible();
window.addEventListener('scroll', checkHeaderVisible);


// Scale down timeline demo if features page larger that viewport
function checkTimelineDemoHeight() {

  var featuresArea = document.getElementById("features-upper");
  var timelineDemo = document.getElementById("timeline-showcase");
  var screenHeight = window.innerHeight - 54;
  
  if (screenHeight < featuresArea.offsetHeight) {
    timelineDemo.classList.add("timeline-showcase-scaledown");
  }
  else {
    timelineDemo.classList.remove("timeline-showcase-scaledown");
  }

}

checkTimelineDemoHeight();
window.addEventListener('resize', checkTimelineDemoHeight);
