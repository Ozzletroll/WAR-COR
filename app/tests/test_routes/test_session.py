from flask import url_for


# Test cookie consent form context injection
def test_check_consent(client, captured_templates):

    # Clear cookie for testing
    response = client.get("/")
    response.set_cookie("warcor_consent", "", expires=0)

    # Test route excluded from showing cookie consent form
    client.get("/")
    template_1, context_1 = captured_templates[1]

    assert "consent" in context_1
    assert context_1["consent"] is True

    # Test that included route shows cookie form
    client.get(url_for('user.register'))
    template_2, context_2 = captured_templates[2]

    assert "consent" in context_2
    assert context_2["consent"] is False


# Test cookie acceptance route
def test_accept_cookie(client):

    # Clear cookie for testing
    response_1 = client.get("/")
    response_1.set_cookie("warcor_consent", "", expires=0)

    response_2 = client.post(url_for("session.accept_cookies"))
    assert response_2.status_code == 302
    assert "warcor_consent" in response_2.headers["Set-Cookie"]


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
