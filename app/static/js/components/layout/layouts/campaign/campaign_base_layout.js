import { Layout } from '../base_layout.js';


// Base class for all campaigns page layouts
export class CampaignLayout extends Layout {

  constructor({
    localStorageName,
    button,
    minAllowedScreenWidth
  }) {
    super({
      localStorageName,
      button,
      minAllowedScreenWidth
    })
    // Display styled elements after initialising to avoid flicker on layout load
    this.campaignsList = document.getElementById("campaigns-list");
    this.campaignsList.style.display = "flex";
  }

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

