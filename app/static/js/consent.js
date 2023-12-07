// Function to accept cookies in gdpr consent form
function acceptCookies(event) {

    const button = event.target;
    const consentForm = document.getElementById("consent-form");
  
    const csrf = button.dataset.csrf;
    const URL = button.dataset.url;

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
  