import { CampaignLayout} from './campaign_base_layout.js';


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