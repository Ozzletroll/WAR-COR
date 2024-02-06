// Check for stored theme preferences
var storedTheme = localStorage.getItem('theme')
if (storedTheme) {
  document.documentElement.setAttribute('theme', storedTheme)

  // Get the stylesheet
  var stylesheet = document.styleSheets[1];
  var iconRule
  
  // Iterate through all the rules and get the icon rule
  for(let i = 0; i < stylesheet.cssRules.length; i++) {
    if(stylesheet.cssRules[i].selectorText === '.icon-invert') {
      iconRule = stylesheet.cssRules[i];
    }
  }

  // Set the icon rules to reflect the current theme
  if (storedTheme == "dark" || storedTheme == "ironbow" || storedTheme == "green" || storedTheme == "horus") {
    iconRule.style.setProperty("filter", "invert(100)");
  }
  else {
    iconRule.style.setProperty("filter", "none");
  }

}
else {
  document.documentElement.setAttribute('theme', null)
  localStorage.setItem('theme', null);
}


// Random number function for HORUS Styling
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

// Function to be called after page load
function setHORUSStyling() {
  // Add extra HORUS theme styling
  var storedTheme = localStorage.getItem('theme');

  if (storedTheme == "horus") {
    // Set additional HORUS theme styling
    var elements = document.querySelectorAll("p");

    Array.from(elements).forEach((element) => {
      if (element.tagName == "P" 
      && (element.parentElement.className != "note-editable" 
      && (element.querySelector("img") == null))) {
          // Split paragraph into words
          var paragraphText = element.textContent.split(" ");
          
          paragraphText.forEach((word, index) => {
            var randomNumber = getRandomInt(100);
            var castigateNumber = getRandomInt(100);
            // Set percentage chance for wrapping each word
            var percentageChance = 2;
            
            if (randomNumber < percentageChance) {
              var span = document.createElement("span");
              span.classList.add("horus");
              span.dataset.originalText = word;
              if (castigateNumber >= 95) {
                span.textContent = "CASTIGATE";
                span.dataset.content = "CASTIGATE";
              }
              else {
                span.textContent = word;
                span.dataset.content = word;
              }
              paragraphText[index] = span.outerHTML;
            }
          });

          var modifiedText = paragraphText.join(' ');
          element.innerHTML = modifiedText;
      }

    })
  }

  // Otherwise, undo any existing HORUS theme style changes
  else {
    var elements = document.getElementsByClassName("horus");
    Array.from(elements).forEach((element) => {

      var parentElement = element.parentElement;
      var oldText = document.createTextNode(element.dataset.originalText);
      parentElement.insertBefore(oldText, element)
      element.remove();

    })

  }
}

document.addEventListener("DOMContentLoaded", function() {
  
  // Call the function after the page has loaded
  setHORUSStyling();

  // Listen for local storage changes and call the function
  window.addEventListener("localstoragechange", function(event) {
    setHORUSStyling();
  });
});
