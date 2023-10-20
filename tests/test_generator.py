
# Test random event name generator
def test_campaign_scroll_target(client):
    response = client.get("generate/random-event-title")

    assert response.status_code == 200

    # Check if returned result is a string that is a length greater than 0
    assert isinstance(response.json['Result'], str)
    assert len(response.json['Result']) > 0
