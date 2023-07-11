// Generate random event name
function user_search(url) {

  var target_url = url

  // Send fetch request to target url
  fetch(target_url, {
    "method": "GET"
  })
  .then(function(response) {
    if (response.status == 200){
      
      // Get the form event title div element
      const titleInput = document.getElementById("event-title");
      titleInput.value = response;

    }
    
  })

}
