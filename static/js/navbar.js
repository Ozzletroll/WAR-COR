function hamburgerClick() {
  var x = document.getElementById("hamburgerMenu");
  if (x.style.display === "flex") {
    x.style.display = "none";
  } else {
    x.style.display = "flex";
  }
}
