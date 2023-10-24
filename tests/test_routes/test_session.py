
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
    assert response.json == {"Message": "Session variable cleared",
                             "type": "element",
                             "target": "campaign-1"}


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
