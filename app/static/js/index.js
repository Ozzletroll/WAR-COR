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

// Fade in feature header when visible
const header = document.getElementById("features-header")
const flavourText = document.getElementById("flavour-typewriter")

function checkHeaderVisible() {
  const elementPosition = header.getBoundingClientRect().top;
  const windowHeight = window.innerHeight;

  if (elementPosition < windowHeight) {
    header.classList.add("hero-fade");
    flavourText.classList.add("flavour-typewriter");
  }
}

checkHeaderVisible();
window.addEventListener('scroll', checkHeaderVisible);
