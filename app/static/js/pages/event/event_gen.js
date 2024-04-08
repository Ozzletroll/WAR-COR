// Generate random event name
function getRequest(url) {

  var target_url = url

// Send fetch request to target url

  fetch(target_url)
    .then(response => response.json())
    .then(data => {

        // Update form input to use result
        const titleInput = document.getElementById("event-form-title");
        titleInput.value = data["Result"];

    })

}
