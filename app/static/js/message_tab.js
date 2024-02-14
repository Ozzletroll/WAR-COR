// Message tab class
class messageTab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = document.getElementById(button);
    this.childButtons = this.tab.getElementsByClassName("button");
    this.state = false

    this.button.onclick = event => {

      if (this.state == false) {
        this.openTab(event)
      }
      else if (this.state == true) {
        this.closeTab(event)
      }
    }
  }

  openTab() {
    this.tab.style.marginBottom = "-400px"
    this.tab.style.height = "400px"
    this.tab.style.borderBottom = "1px solid var(--dark_red)"
    this.state = true
    this.tab.setAttribute("aria-hidden", "false");
    Array.from(this.childButtons).forEach(element => {
      element.setAttribute("tabIndex", "0")
    })
    this.button.setAttribute("aria-label", "Close Messages Tab");
  }

  closeTab() {
    this.tab.style.marginBottom = "0"
    this.tab.style.height = "0"
    this.tab.style.borderBottom = "0px solid var(--dark_red)"
    this.tab.setAttribute("aria-hidden", "true");
    Array.from(this.childButtons).forEach(element => {
      element.setAttribute("tabIndex", "-1")
    })
    this.button.setAttribute("aria-label", "Open Messages Tab: {{current_user.messages | length}} New Messages");
    this.state = false
  }

}

// Create messages tab
const messages_tab = new messageTab({
  tab: "messages-tab",
  button: "messages-button",
})


// Function to accept/decline campaign invite messages
function handleMessage(event) {

  const button = event.target;

  const csrf = button.dataset.csrf;
  const URL = button.dataset.url;
  const campaignID = button.dataset.campaignId;
  const messageID = button.dataset.messageId;

  // Create form and add data
  const formData = new FormData();
  formData.append("campaign_id", campaignID);
  formData.append("message_id", messageID);

  // Send to server via fetch request
  fetch(URL, {
    method: "POST",
    redirect: "follow",
    headers: {
      "X-CSRF-TOKEN": csrf,
    },
    body: formData
  })
  .then((response)=>{         
    if(response.redirected){
      window.location.href = response.url;
    } 
  })
};
