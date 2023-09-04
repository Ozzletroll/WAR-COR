const searchBar = document.getElementById("search-bar");

/**
* Function to filter timeline page elements based on search bar query.
* Hides elements that do not contain a matching query by setting opacity to 50%.
*/
function timelineSearch() {
  var searchQuery = searchBar.value.toLowerCase();
  var monthOuters = document.getElementsByClassName("month-outer");

  // Iterate through all month-outer elements
  for (var index = 0; index < monthOuters.length; index++) {

    var containsResult = false;

    // Get the current month-outer element
    var container = monthOuters[index];

    // Find all the elements with the class "event-header" within the container
    var eventHeaders = container.querySelectorAll(".event-header");

    // Iterate through all the event-header elements
    for (var i = 0; i < eventHeaders.length; i++) {
      var eventHeader = eventHeaders[i];
      var elementText = eventHeader.innerText.toLowerCase();

      // Get event element and time label
      var outerContainer = eventHeaders[i].closest('.event-outer-container');
      var rightBranchLabel = outerContainer.previousElementSibling;

      // Positive search result
      if (elementText.includes(searchQuery)) {
        // Reset styling to undo any changes made by search function
        outerContainer.style.opacity = "100%";
        rightBranchLabel.style.opacity = "100%";
        containsResult = true;
      }
      // Negative search result
      else {
        outerContainer.style.opacity = "50%";
        rightBranchLabel.style.opacity = "50%";
      }
    }

    // If result not found in any sub elements, set opacity to 50%
    if (containsResult == false && searchBar.value != "") {
      monthOuters[index].style.opacity = "50%";
    }
    else {
      monthOuters[index].style.opacity = "100%";
    }

  }
}

// Add event listener to the input field
searchBar.addEventListener("input", timelineSearch);

