import { Toolbar } from '../../components/ui/ui_toolbar.js';
import { SortToggle } from '../../components/ui/sort_toggle.js';
import { LayoutManager } from '../../components/layout/layout_manager.js';
import { ListLayout } from '../../components/layout/layouts/campaign/campaign_list_layout.js';
import { GridLayout } from '../../components/layout/layouts/campaign/campaign_grid_layout.js';
import { initialiseCampaignMobileTabs } from '../../pages/campaign/campaign_mobile_tabs.js';
import { initialiseDropdownMenus } from '../../pages/campaign/dropdown_menu.js';


// Add tooltips to ui toolbar
const toolbar = new Toolbar();

// Configure date/title sort
const sortToggle = new SortToggle({
  dateButton: "sort-toggle-date",
  titleButton: "sort-toggle-az"
})

// Configure list/grid layout manager
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
        minAllowedScreenWidth: 1250,
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
