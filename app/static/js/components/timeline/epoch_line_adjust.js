export function adjustEpochLine() {
  const dayLineFollowed = document.getElementsByClassName("day-line-followed");
  const startingMargins = []
  Array.from(dayLineFollowed).forEach(element => {
      var computedStyle = window.getComputedStyle(element);
      var marginBottom = parseFloat(computedStyle.getPropertyValue("margin-bottom"));
      startingMargins.push(marginBottom)
  });

  function epochLineAdjust() {

    // Adjust day vertical line lengths to compensate for epoch elements
    Array.from(dayLineFollowed).forEach((element, index) => {

      var dayElement = element.parentNode;
      var currentElement = dayElement.nextElementSibling;
      // Skip to next element if .event-between element present
      if (currentElement.classList.contains("event-between")) {
        var currentElement = currentElement.nextElementSibling;
      }

      var epochElements = [];

      while (currentElement) {
        if (currentElement.classList.contains("epoch-start-group")) {
            epochElements.push(currentElement);
          } 
        else {
          break;
        }
          currentElement = currentElement.nextElementSibling;
        }

      var totalHeight = 0;
      for (var i = 0; i < epochElements.length; i++) {
        totalHeight += epochElements[i].getBoundingClientRect().height;;
      }

      var newMargin = startingMargins[index] - totalHeight;
      element.style.marginBottom = newMargin + "px";
        
    });

    // Adjust month connector margin-top to compensate for epoch elements
    var monthConnectors = document.getElementsByClassName("month-connector-offset");
    Array.from(monthConnectors).forEach(element => {
        
      var nextElement = element.nextElementSibling;
      var epochElement = nextElement.querySelector(".epoch-start-group");
      var epochHeight = epochElement.getBoundingClientRect().height;

      element.style.marginTop = epochHeight + "px";

    });
  }

  const epochEndGroups = document.getElementsByClassName("epoch-end-group");
  const rightBranchLabel = document.getElementsByClassName("right-branch-label")[0];

  function offsetEndEpochMargin() {
    if (rightBranchLabel != null) {
      var offsetWidth = rightBranchLabel.getBoundingClientRect().width * -1;
      Array.from(epochEndGroups).forEach(element => {
    
        if (window.innerWidth > 650) {
          element.style.marginLeft = offsetWidth + "px";
        }
        else {
          element.style.marginLeft = "0px";
        }
      })
    }
  }

  // Trigger margin adjust on sidebar page element resize (usually from sidebar deployment)
  const element = document.getElementById("scrollpage") || document.getElementById("main-features");

  const resizeObserver = new ResizeObserver(entries => {
    entries.forEach(entry => {
      epochLineAdjust();
    });
  });

  // Start observing the target element
  resizeObserver.observe(element);

  // Add conventional event listeners for page load and resize
  window.addEventListener("resize", epochLineAdjust);
  window.addEventListener("load", epochLineAdjust);
  window.addEventListener("resize", offsetEndEpochMargin);
  window.addEventListener("load", offsetEndEpochMargin);

}
