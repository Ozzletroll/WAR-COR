const searchBar = document.getElementById("search-bar");
const hitsCounter = document.getElementById("hits-counter");
const initialValue = hitsCounter.innerText;

/**
* Function to filter campaigns page elements based on search bar query.
* Hides elements that do not contain a matching query by setting "display: none".
*/
function campaignSearch() {
  var searchQuery = searchBar.value.toLowerCase();
  var campaignElements = document.getElementsByClassName("campaign-header");
  var results = campaignElements.length;

  for (var index = 0; index < campaignElements.length; index++) {

    var elementText = campaignElements[index].innerText.toLowerCase();
    var campaignCard = document.getElementsByClassName("campaign-entry")[index];

    if (elementText.includes(searchQuery)) {
      // Reset styling to undo any changes made by search function
      campaignCard.style.display = "flex";

    }
    else {
      campaignCard.style.display = "none";
      results -= 1;
    }
  }

  // Update hits counter
  hitsCounter.innerText = `${results} Campaigns`;

}


// Add event listener to the input field
searchBar.addEventListener("input", campaignSearch);
