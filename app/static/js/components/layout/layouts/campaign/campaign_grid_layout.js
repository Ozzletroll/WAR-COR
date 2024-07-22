import { CampaignLayout} from './campaign_base_layout.js';


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
  