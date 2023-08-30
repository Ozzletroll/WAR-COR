// Get the radio buttons
const radioList = document.getElementById("campaign-toggle-list");
const radioGrid = document.getElementById("campaign-toggle-grid");

// Get campaigns list elements
const campaignsList = document.getElementById("campaigns-list");
const campaignsEntries = document.getElementsByClassName("campaign-entry")

// Add event listener to each radio button
radioList.addEventListener("click", toggleLayout);
radioGrid.addEventListener("click", toggleLayout);

// Add event listener for page load
document.addEventListener("DOMContentLoaded", toggleLayout);

// Add event listener on page resize
window.addEventListener("resize", toggleLayout);


function getLocalStorage() {

    // Check localstorage for previous set layout
    previousLayout = localStorage.getItem('campaign_layout');

    if (previousLayout == "grid") {
      console.log("grid set")
      radioList.checked = false;
      radioGrid.checked = true;
    }
    else if (previousLayout == "list") {
      console.log("list set")
      radioList.checked = true;
      radioGrid.checked = false;
    }
}

getLocalStorage();

// Function to toggle label background
function toggleLayout() {

  // Get the labels
  const labelList = document.querySelector('label[for="campaign-toggle-list"]');
  const labelGrid = document.querySelector('label[for="campaign-toggle-grid"]');

  function setListLayout() {
    // Set button style
    labelList.style.backgroundColor = "var(--elem_dark)";
    labelGrid.style.backgroundColor = "";

    // Set layout style
    campaignsList.style.flexDirection = "column"
    Array.from(campaignsEntries).forEach((entry) => {
      entry.style.width = "100%";
    });
  }

  function setGridLayout() {
    // Set button style
    labelList.style.backgroundColor = "";
    labelGrid.style.backgroundColor = "var(--elem_dark)";

    // Set layout style
    campaignsList.style.flexDirection = "row"
    Array.from(campaignsEntries).forEach((entry) => {
      entry.style.width = "45%";
    });
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
    }
    

  }


}