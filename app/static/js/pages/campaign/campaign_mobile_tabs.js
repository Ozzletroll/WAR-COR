import { CampaignCard } from "../../components/campaign_card.js";


export function initialiseCampaignMobileTabs() {

  // Create mobile tabs for all campaigns
  const campaigns = [];
  var tabs = document.getElementsByClassName("campaign-entry");
  Array.from(tabs).forEach((element) => {

    if (element.classList.contains("campaign-new-user-entry")) {
      return
    }
    else {
      var buttonElement = element.querySelector(".campaign-header");
      var tabElement = element.querySelector(".campaign-body");
    
      var tab = new CampaignCard({
        tab: tabElement,
        button: buttonElement,
      })
    
      campaigns.push(tab);
    }

  })

  // If resizing above 500px, open all tabs again
  window.addEventListener("resize", function() {
    if (window.innerWidth > 500) {
      Array.from(campaigns).forEach((tab) => {
        tab.openTab();
      })
    }
    else {
      Array.from(campaigns).forEach((tab) => {
        tab.closeTab();
        tab.checkStatus();
      })
    }
  });

  window.addEventListener("DOMContentLoaded", function() {
    Array.from(campaigns).forEach((tab) => {
      tab.checkStatus();
    })
  });

}
