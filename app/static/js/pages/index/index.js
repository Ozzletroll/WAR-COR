import { adjustEpochLine } from '../../components/timeline/epoch_line_adjust.js';
import { marginFix } from '../../components/timeline/margin_fix.js';


adjustEpochLine();

// Fix timeline element negative margins on safari iOS
window.addEventListener("resize", marginFix);
window.addEventListener("DOMContentLoaded", marginFix());

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
  var downArrowArea = downArrow.parentElement;
  
  if (window.scrollY == 0) {
    navbar.style.boxShadow = "none";
    downArrow.style.opacity = "";
    downArrow.style.display = "flex";
    downArrowArea.setAttribute("tabIndex", 0);

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
      downArrowArea.setAttribute("tabIndex", -1);
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

function checkHeaderVisible() {
  const elementPosition = header.getBoundingClientRect().top;
  const windowHeight = window.innerHeight;

  if (elementPosition < windowHeight) {
    header.classList.add("hero-fade");
    animateTimelineDemo();
  }
}

checkHeaderVisible();
window.addEventListener("scroll", checkHeaderVisible);


// Scale down timeline demo if features page larger that viewport
function checkTimelineDemoHeight() {

  var featuresArea = document.getElementById("features-upper");
  var timelineDemo = document.getElementById("timeline-showcase");
  var screenHeight = window.innerHeight - 54;
  
  if (screenHeight < featuresArea.offsetHeight) {

    // Apply transform scale
    // Excludes firefox as it is bugged when rendering 1px lines
    if (!navigator.userAgent.includes("Firefox")) {
      timelineDemo.classList.add("timeline-showcase-scaledown");
    }
    
  }
  else {
    timelineDemo.classList.remove("timeline-showcase-scaledown");
  }

}

checkTimelineDemoHeight();
window.addEventListener("resize", checkTimelineDemoHeight);


// Typewriter text effect
function typewritingAnimation(element, delay) {

  // Wrap all characters in span tags
  var originalHTML = element.textContent;
  element.innerHTML = element.textContent.replace(/\w/g, "<span>$&</span>");
  // Set all inner characters to appear hidden
  var innerElements = element.children;
  Array.from(innerElements).forEach(character => {
    character.style.visibility = "hidden";
  })

  var index = 0;
  function addNextCharacter() {
    if (index < innerElements.length) {
      innerElements[index].style.visibility = "visible";
      index++;
      setTimeout(addNextCharacter, delay);
    }
    if (index == innerElements.length) {
      // Remove all spans after animation finishes
      element.innerHTML = originalHTML;
      element.style.visibility = "visible";
    }
  }
  addNextCharacter();
}

function handleIntersection(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const article = entry.target;
      const title = article.querySelector(".feature-title");
      const img = article.querySelector("img");
      const text = article.querySelector("p");
      img.classList.add("hero-fade");
      typewritingAnimation(title, 30);
      text.classList.add("hero-fade");
      // Remove the observer after animation is triggered
      observer.unobserve(article);
    }
  });
}

const observer = new IntersectionObserver(handleIntersection, {
  root: null, // Use the viewport as the root
  threshold: 0.75,
});

const articles = document.getElementsByClassName("features-lower");
Array.from(articles).forEach(article => {
  observer.observe(article);
});
