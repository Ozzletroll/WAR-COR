
# Test if the home page is reachable
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>WAR/COR</title>" in response.data


# Test if the about page is reachable
def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b'<h3 class="campaigns-heading">About</h3>' in response.data


# Test if the contact page is reachable
def test_contact(client):
    response = client.get("/contact")
    assert response.status_code == 200
    assert b'<h3 class="campaigns-heading">Contact</h3>' in response.data


# Test campaign scroll target route
def test_campaign_scroll_target(client):
    response = client.get("/session/campaign-scroll-target")
    # Response should be 204 as session variable does not exist
    assert response.status_code == 204

    # Set session var and retry test
    with client.session_transaction() as session:
        session["campaign_scroll_target"] = "campaign-1"

    response = client.get("/session/campaign-scroll-target")
    assert response.status_code == 200
    assert response.json == {"Message": "Session variable cleared", "target": "campaign-1"}


# Test timeline scroll target route
def test_timeline_scroll_target(client):
    response = client.get("/session/timeline-scroll-target")
    # Response should be 204 as session variable does not exist
    assert response.status_code == 204

    # Set session var and retry test
    with client.session_transaction() as session:
        session["timeline_relative_scroll"] = "event-1"

    response = client.get("/session/timeline-scroll-target")
    assert response.status_code == 200
    assert response.json == {"Message": "Session variable cleared",
                             "type": "relative",
                             "target": "event-1"}

    with client.session_transaction() as session:
        session["timeline_scroll_target"] = "event-1"

    response = client.get("/session/timeline-scroll-target")
    assert response.status_code == 200
    assert response.json == {"Message": "Session variable cleared",
                             "type": "element",
                             "target": "event-1"}
