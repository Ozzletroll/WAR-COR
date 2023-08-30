// Get the radio buttons
const radioList = document.getElementById("campaign-toggle-list");
const radioGrid = document.getElementById("campaign-toggle-grid");

// Get campaigns list elements
const campaignsList = document.getElementById("campaigns-list");
const campaignsEntries = document.getElementsByClassName("campaign-entry")

// Add event listener to each radio button
radioList.addEventListener("click", toggleLayout);
radioGrid.addEventListener("click", toggleLayout);

// Add event listener for page load and page refresh
document.addEventListener("DOMContentLoaded", toggleLayout);
window.addEventListener("resize", toggleLayout);


// Function to toggle label background
function toggleLayout() {

  console.log("Function called")

  // Get the labels
  const labelList = document.querySelector('label[for="campaign-toggle-list"]');
  const labelGrid = document.querySelector('label[for="campaign-toggle-grid"]');

  function setListLayout() {
    // Set button style
    labelList.style.backgroundColor = "var(--elem_bright)";
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
    labelGrid.style.backgroundColor = "var(--elem_bright)";

    // Set layout style
    campaignsList.style.flexDirection = "row"
    Array.from(campaignsEntries).forEach((entry) => {
      entry.style.width = "45%";
    });
  }

  if (radioList.checked) {

    setListLayout();
    
  } else if (radioGrid.checked ) {

    // Check if screen is wide enough to allow grid layout
    if (window.innerWidth >= 1200) {
      setGridLayout();
    }
    // Otherwise, toggle back to list layout
    else {
      console.log("AAA")
      radioList.checked = true;
      radioGrid.checked = false;
      toggleLayout();
    }
    

  }


}