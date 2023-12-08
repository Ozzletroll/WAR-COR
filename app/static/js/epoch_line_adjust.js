const dayLineFollowed = document.getElementsByClassName("day-line-followed");
const startingMargins = []
Array.from(dayLineFollowed).forEach(element => {

    var computedStyle = window.getComputedStyle(element);
    var marginBottom = parseFloat(computedStyle.getPropertyValue("margin-bottom"));
    startingMargins.push(marginBottom)

});

function epochLineAdjust() {

    Array.from(dayLineFollowed).forEach((element, index) => {
        
        var dayElement = element.parentNode;
        var currentElement = dayElement.nextElementSibling;
        var epochElements = [];

        while (currentElement) {
            if (currentElement.classList.contains("epoch-start-group") 
            || currentElement.classList.contains("epoch-end-group")) {
              epochElements.push(currentElement);
            } else {
              break;
            }
            currentElement = currentElement.nextElementSibling;
          }

          var totalHeight = 0;
          for (var i = 0; i < epochElements.length; i++) {
            totalHeight += epochElements[i].offsetHeight;
          }

        var newMargin = startingMargins[0] - totalHeight;
        element.style.marginBottom = newMargin + "px";
        
    });

}

window.addEventListener("resize", epochLineAdjust);
window.addEventListener("load", epochLineAdjust);
