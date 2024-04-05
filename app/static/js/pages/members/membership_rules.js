// Function to get current campaign settings
function checkCurrentSettings(private, acceptingApplications, commentStatus) {

    var visibility;
    if (private == "True") {
        visibility = "visibility-private";
    }
    else {
        visibility = "visibility-public";
    }

    document.getElementById(visibility).checked = true;

    var membership;
    if (acceptingApplications == "True") {
        membership = "membership-open";
    }
    else {
        membership = "membership-invite";
    }

    document.getElementById(membership).checked = true;

    var comment;
    if (commentStatus == "private") {
        comment = "comment-private";
    }
    else if (commentStatus == "open") {
        comment = "comment-open";
    }
    else {
        comment= "comment-disabled";
    }

    document.getElementById(comment).checked = true;

}

// Function to update campaign membership rules via fetch request
function updateMembershipSettings(target_url, csrfToken) {

    var target_url = target_url;
    var visibility = document.querySelector('input[name="visibility"]:checked').value;
    var membership = document.querySelector('input[name="membership"]:checked').value;
    var comment = document.querySelector('input[name="comment"]:checked').value;

    var data = new FormData();
    data.append("visibility", visibility);
    data.append("membership", membership);
    data.append("comment", comment);

    // Send fetch request to target url
    fetch(target_url, {
        "method": "POST",
        "headers": {
        'X-CSRF-TOKEN': csrfToken,
        },
        "body" : data,
    })
    .then(function(response) {
        return
    })
}
