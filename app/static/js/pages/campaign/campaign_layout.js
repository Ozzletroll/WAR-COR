// Get the radio buttons
const radioList = document.getElementById("campaign-toggle-list");
const radioGrid = document.getElementById("campaign-toggle-grid");

// Get campaigns list elements
const campaignsList = document.getElementById("campaigns-list");
const campaignsEntries = document.getElementsByClassName("campaign-entry")

// Add event listener to each radio button
radioList.addEventListener("click", toggleLayout);
radioGrid.addEventListener("click", toggleLayout);

// Add event listeners for page load
window.addEventListener("load", toggleLayout);

// Add event listeners on page resize
window.addEventListener("resize", toggleLayout);
window.addEventListener("resize", function() {
  if (localStorage.getItem('campaign_layout') == "grid" && window.innerWidth >= 1200) {
    matchOverviewHeight();
  }
});

function getLocalStorage() {

    // Check localstorage for previous set layout
    previousLayout = localStorage.getItem('campaign_layout');

    if (previousLayout == "grid") {
      radioList.checked = false;
      radioGrid.checked = true;
    }
    else if (previousLayout == "list") {
      radioList.checked = true;
      radioGrid.checked = false;
    }
}

// Initial function call for localStorage
getLocalStorage();


/**
 * Function to set campaigns overviews to match heights
 */
function matchOverviewHeight() {

  // Set matching height of overview elements for each pair of campaign cards
  var campaignOverviewElements = document.querySelectorAll(".campaign-entry-container .campaign-overview");
  var campaignHeaderElements = document.querySelectorAll(".campaign-header");
  var campaignMemberElements = document.querySelectorAll(".campaign-members-system-row");

  for (var index = 0; index + 1 < campaignOverviewElements.length; index += 2) {
    var firstElement = campaignOverviewElements[index];
    var secondElement = campaignOverviewElements[index + 1];

    // Reset height values to default, for true comparison
    // This prevents the elements from never being able to shrink
    firstElement.style.minHeight = "";
    secondElement.style.minHeight = "";

    // Get the height of the campaign card headers
    var firstHeaderElement = campaignHeaderElements[index];
    var secondHeaderElement = campaignHeaderElements[index + 1];

    firstHeaderElement.style.height = "";
    secondHeaderElement.style.height = "";
    
    // Match the header element heights
    var firstHeaderHeight = firstHeaderElement.clientHeight;
    var secondHeaderHeight = secondHeaderElement.clientHeight;
    var maxHeaderHeight = Math.max(firstHeaderHeight, secondHeaderHeight);

    firstHeaderElement.style.height = maxHeaderHeight + "px";
    secondHeaderElement.style.height = maxHeaderHeight + "px";

    // Match card overview element heights
    var firstElementHeight = firstElement.clientHeight;
    var secondElementHeight = secondElement.clientHeight;
    var maxHeight = Math.max(firstElementHeight, secondElementHeight);

    firstElement.style.minHeight = maxHeight + "px";
    secondElement.style.minHeight = maxHeight + "px";

    // Match members list element heights
    var firstMembersList = campaignMemberElements[index];
    var secondMembersList = campaignMemberElements[index + 1];
    
    var firstMembersHeight = firstMembersList.clientHeight;
    var secondMembersHeight = secondMembersList.clientHeight;
    var maxMembersHeight = Math.max(firstMembersHeight, secondMembersHeight);

    firstMembersList.style.minHeight = maxMembersHeight + "px";
    secondMembersList.style.minHeight = maxMembersHeight + "px";
  }
}

function undoOverviewHeight() {

  // Reset height of overview elements for each pair of campaign cards
  var campaignOverviewElements = document.querySelectorAll(".campaign-entry-container .campaign-overview");

  for (var index = 0; index < campaignOverviewElements.length; index ++) {
    campaignOverviewElements[index].style.minHeight = "0px";
  }

  // Reset height of header elements for each campaign card
  campaignHeaderElements = document.querySelectorAll(".campaign-header");

  for (var index = 0; index < campaignHeaderElements.length; index ++) {
    campaignHeaderElements[index].style.height = "";
  }

  // Rest height of all members lists
  var membersListElements = document.querySelectorAll(".campaign-members");
  for (var index = 0; index < membersListElements.length; index ++) {
    membersListElements[index].style.minHeight = "";
  }

}


// Function to toggle label background
function toggleLayout() {

  // Get the labels
  const labelList = document.querySelector('label[for="campaign-toggle-list"]');
  const labelGrid = document.querySelector('label[for="campaign-toggle-grid"]');
  const buttonAreas = document.querySelectorAll(".campaign-entry-buttons");

  /**
   * Function to set campaigns page layout to "list" mode
   */
  function setListLayout() {
    // Set button style
    labelList.style.backgroundColor = "var(--elem_dark)";
    labelGrid.style.backgroundColor = "";

    // Set layout style
    campaignsList.style.flexDirection = "column"
    Array.from(campaignsEntries).forEach((entry) => {
      entry.style.width = "100%";
    });

    // Reset button area styling
    Array.from(buttonAreas).forEach((entry) => {
      entry.style.justifyContent = "flex-start";
    });

    // Reset banner images
    var campaignImages = document.getElementsByClassName("banner-image-area");
    Array.from(campaignImages).forEach(image => {
      image.style.display = "";
    })

    // Reset overview height matching
    undoOverviewHeight();

  }

  /**
   * Function to set campaigns page layout to "grid" mode
   */
  function setGridLayout() {

    // Set button style
    labelList.style.backgroundColor = "";
    labelGrid.style.backgroundColor = "var(--elem_dark)";

    // Set layout style
    campaignsList.style.flexDirection = "row"
    Array.from(campaignsEntries).forEach((entry) => {
      entry.style.width = "45%";
    });
    
    // Set button area styling
    Array.from(buttonAreas).forEach((entry) => {
        entry.style.justifyContent = "space-between";
    });

    // Hide banner images
    var campaignImages = document.getElementsByClassName("banner-image-area");
    Array.from(campaignImages).forEach(image => {
      image.style.display = "none";
    })

    // Make overview areas heights match
    matchOverviewHeight();
  }

  if (radioList.checked) {

    // Set user preference to "list"
    localStorage.setItem('campaign_layout', "list");
    setListLayout();
    
  } else if (radioGrid.checked ) {

    // Set user preference to "grid"
    localStorage.setItem('campaign_layout', "grid");

    // Check if screen is wide enough to allow grid layout
    if (window.innerWidth >= 1200) {
      setGridLayout();
    }
    // Otherwise, toggle back to list layout
    else {
      setListLayout();
      // Reset overview height matching
      undoOverviewHeight();
    }
  }


}