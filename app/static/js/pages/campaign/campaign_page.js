import { Toolbar } from '../../components/ui/ui_toolbar.js';
import { initialiseCampaignLayout } from '../../pages/campaign/campaign_layout.js';
import { initialiseCampaignMobileTabs } from '../../pages/campaign/campaign_mobile_tabs.js';
import { initialiseDropdownMenus } from '../../pages/campaign/dropdown_menu.js';


// Add tooltips to ui toolbar
const toolbar = new Toolbar();

initialiseCampaignLayout();
initialiseCampaignMobileTabs();
initialiseDropdownMenus();