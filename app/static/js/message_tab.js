// Message tab class
class messageTab {
  constructor({
    tab,
    button,
  }) {
    this.tab = document.getElementById(tab);
    this.button = document.getElementById(button);
    this.childButtons = this.tab.getElementsByClassName("button");
    this.messages = this.tab.querySelectorAll(".message-item").length;
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
    this.tab.scrollTop = 50;
    this.state = true
    this.tab.setAttribute("aria-hidden", "false");
    Array.from(this.childButtons).forEach(element => {
      element.setAttribute("tabIndex", "0")
    })
    this.messages = this.tab.querySelectorAll(".message-item").length;
    if (this.messages >= 2) {
      document.getElementById("dismiss-all").focus();
      setTimeout(() => {
        this.tab.scrollTop = 0;
      }, 50);
    }
    else if (this.messages > 0) {
      this.childButtons = this.tab.getElementsByClassName("button");
      this.childButtons[0].focus();
    }
    this.button.setAttribute("aria-label", "Close Messages Tab");
    this.tab.style.backdropFilter = "blur(15px)";
    this.tab.style.webkitBackdropFilter = "blur(15px)";
    var noMessagesText = this.tab.querySelector("#no-messages-flavour-text");
    if (noMessagesText != null) {
      noMessagesText.style.display = "flex";
    }
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

    this.tab.style.backdropFilter = "";
    this.tab.style.webkitBackdropFilter = "";

    var noMessagesText = this.tab.querySelector("#no-messages-flavour-text");
    if (noMessagesText != null) {
      noMessagesText.style.display = "none";
    }

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

  function deleteMessage(messageID) {
    var messageElement = document.getElementById(`message-${messageID}`);
    if (messageElement != null) {
      messageElement.style.transition = "0.3s";
      messageElement.style.opacity = "0";
      setTimeout(() => {
        messageElement.remove();
      }, 300);
      var messageCount = document.getElementById("message-count");
      value = parseInt(messageCount.innerText);
      value--;
      messageCount.innerText = value; 
    }

    var messageTabCount = document.getElementById("message-tab-count");
    if (messageTabCount != null) {
      tabValue = parseInt(messageTabCount.innerText);
      tabValue--;
      messageTabCount.innerText = tabValue.toString();

      var messageText = messageTabCount.parentElement.querySelector("#message-count-text");
      if (value == 1) {
        messageText.innerText = "New Message";
      } 
      else {
        messageText.innerText = "New Messages";
      }
    }
  }

  function checkIfNoMessages() {
    var messagesArea = document.getElementById("notifications-list");
    var messages = messagesArea.querySelectorAll(".message-item");
    if (messages.length == 0) {
      const messagesTab = document.getElementById('messages-tab');
      const htmlString = `
        <div class="messages-upper no-messages-upper" aria-label="No Messages">
          <h5 id="no-messages" class="no-message-header" aria-label="No Messages">NO MESSAGES</h5>
          <div class="no-message-text-area">
            <div id="no-messages-flavour-text" class="no-messages-text" aria-label="Message flavour text">
              <h5 class="flavour-text typing-1 empty-search-header search-header-bold">Communications Online:</h5>
              <h5 class="flavour-text typing-2 empty-search-header search-header-bold">>Satellite::Lock</h5>
              <h5 class="flavour-text typing-3 empty-search-blink search-header-bold">>Awaiting Uplink</h5>
            </div>
            <div class="no-message-flavour no-message-spacer"></div>
          </div>
        </div>
      `;

      messagesTab.innerHTML = htmlString;
      document.getElementById("no-messages-flavour-text").style.display = "flex";
    }
  }

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
    if (response.redirected) {
      window.location.href = response.url;
    } 
    if (response.status == 200) {
      deleteMessage(messageID);
      checkIfNoMessages();
    }
  })
};
