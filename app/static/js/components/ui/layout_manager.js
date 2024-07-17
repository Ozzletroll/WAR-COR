export class LayoutManager {
  constructor({
    layoutLocalStorage,
    layouts,
    defaultLayout,
  })
  {
    layouts.forEach(layout => {
      layout.layoutManager = this;
    });
    this.layouts = layouts;
    this.defaultLayout = defaultLayout;
    this.storedLayout = this.getLayout(localStorage.getItem(layoutLocalStorage) || defaultLayout);
    this.selectedLayout = this.storedLayout;
    this.setLayout(this.storedLayout);

    window.addEventListener("resize", () => {
      this.checkLayoutWidth();
    });
  }

  setLayout(layout) {
    if (window.innerWidth < layout.minAllowedScreenWidth) {
      layout = this.getLayout(this.defaultLayout);
    }
    this.selectedLayout = layout;
    layout.resetButtonStyle();
    layout.applyButtonStyle();
    layout.applyLayoutStyle();
  }

  getLayout(layoutName) {
    for (let layout of this.layouts) {
      if (layout.localStorageName == layoutName) {
        return layout;
      }
    }
  }

  checkLayoutWidth() {
    if (window.innerWidth < this.storedLayout.minAllowedScreenWidth) {
      this.setLayout(this.getLayout(this.defaultLayout));
    }
    else {
      this.setLayout(this.storedLayout);
    }
  }
}


class Layout {
  constructor({
    localStorageName,
    button,
    minAllowedScreenWidth
  })
  {
    this.layoutManager;
    this.localStorageName = localStorageName;
    this.button = button;
    this.minAllowedScreenWidth = minAllowedScreenWidth;
    this.allButtons = document.querySelectorAll(".radio");
    this.button.addEventListener("click", () => {
      localStorage.setItem("campaignLayout", this.localStorageName);
      this.layoutManager.storedLayout = this;
      this.layoutManager.setLayout(this);
    });
    this.resetButtonStyle();
  }

  resetButtonStyle() {
    this.allButtons.forEach(button => {
      button.parentElement.style.backgroundColor = "";
    })
  }

  applyButtonStyle() {
    this.button.checked = true;
    this.button.parentElement.style.backgroundColor = "var(--elem_dark)";
  }

  applyLayoutStyle() {
    // This is overridden by individual layouts
  }
}


class CampaignLayout extends Layout {

  matchOverviewHeight() {

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

  undoOverviewHeight() {
    // Reset height of overview elements for each pair of campaign cards
    var campaignOverviewElements = document.querySelectorAll(".campaign-entry-container .campaign-overview");
    for (var index = 0; index < campaignOverviewElements.length; index ++) {
      campaignOverviewElements[index].style.minHeight = "0px";
    }

    // Reset height of header elements for each campaign card
    var campaignHeaderElements = document.querySelectorAll(".campaign-header");
    for (var index = 0; index < campaignHeaderElements.length; index ++) {
      campaignHeaderElements[index].style.height = "";
    }

    // Rest height of all members lists
    var membersListElements = document.querySelectorAll(".campaign-members-system-row");
    for (var index = 0; index < membersListElements.length; index ++) {
      membersListElements[index].style.minHeight = "";
    }
  }
}


export class ListLayout extends CampaignLayout {

  applyLayoutStyle() {

    var buttonAreas = document.querySelectorAll(".campaign-entry-buttons");
    var campaignsList = document.getElementById("campaigns-list");
    var campaignsEntries = document.getElementsByClassName("campaign-entry")

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
    this.undoOverviewHeight();
  }

}

export class GridLayout extends CampaignLayout {

  applyLayoutStyle() {
    
    var buttonAreas = document.querySelectorAll(".campaign-entry-buttons");
    var campaignsList = document.getElementById("campaigns-list");
    var campaignsEntries = document.getElementsByClassName("campaign-entry")

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
    this.matchOverviewHeight();
  }

}

