
// Continously check screen size
function handleResize() {
  let newHeight = window.innerHeight;
  let newWidth = window.innerWidth;
  var menu = document.getElementById("hamburgerMenu");

  // Hide hamburger menu if screen has been resized beyond 700px
  if (newWidth >= 700) {
    menu.style.display = "none"
  }

}

window.addEventListener("resize", handleResize);

// calling the resize function for the first time
handleResize();

// Display the hamburger menu on click
function hamburgerClick() {
  var menu = document.getElementById("hamburgerMenu");
  if (menu.style.display === "flex") {
    menu.style.display = "none";
  } else {
    menu.style.display = "flex";
  }
}
