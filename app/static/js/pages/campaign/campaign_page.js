import { Toolbar } from '../../components/ui/ui_toolbar.js';
import { LayoutManager, ListLayout, GridLayout } from '../../components/ui/layout_manager.js';
import { initialiseCampaignMobileTabs } from '../../pages/campaign/campaign_mobile_tabs.js';
import { initialiseDropdownMenus } from '../../pages/campaign/dropdown_menu.js';



// Add tooltips to ui toolbar
const toolbar = new Toolbar();

const layoutManager = new LayoutManager({
  layoutLocalStorage: "campaignLayout",
  layouts: 
    [
    new ListLayout(
      {
        localStorageName: "list",
        button: document.getElementById("campaign-toggle-list"),
        minAllowedScreenWidth: 0,
      }),
    new GridLayout(
      {
        localStorageName: "grid",
        button: document.getElementById("campaign-toggle-grid"),
        minAllowedScreenWidth: 1200,
      })
    ],
    defaultLayout: "list",
});

initialiseCampaignMobileTabs();
initialiseDropdownMenus();

// Style all horus theme text elements
var horusElements = document.getElementsByClassName("summernote-horus");
Array.from(horusElements).forEach(element => {
  element.setAttribute("data-content", element.innerText);
});
