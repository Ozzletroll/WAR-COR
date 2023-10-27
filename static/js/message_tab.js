// Message tab class
class messageTab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = button;
    this.state = false

    document.getElementById(this.button).onclick = event => {

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
  }

  closeTab() {
    this.tab.style.marginBottom = "0"
    this.tab.style.height = "0"
    this.tab.style.borderBottom = "0px solid var(--dark_red)"

    this.state = false
  }

}

// Create messages tab
const messages_tab = new messageTab({
  tab: "messages-tab",
  button: "messages-button",
})


function acceptInvite(event) {

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

}
