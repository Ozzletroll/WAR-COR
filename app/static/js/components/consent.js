// Function to accept cookies in gdpr consent form
function acceptCookies() {

    const consentForm = document.getElementById("consent-form");
    const csrf = consentForm.dataset.csrf;
    const URL = consentForm.dataset.url;

    // Send to server via fetch request
    fetch(URL, {
      method: "POST",
      headers: {
        "X-CSRF-TOKEN": csrf,
      },
    })
    .then((response)=>{       
        if(response.status == 200){
            consentForm.remove();
        } 
    })
  };
  
// Add event listener to consent form
document.getElementById("consent-form").addEventListener("submit", function(event) {
  event.preventDefault();
  acceptCookies();
});
