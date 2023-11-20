
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


def test_cookie_policy(client):
    response = client.get("/cookie-policy")
    assert response.status_code == 200
    assert b'<h3 class="campaigns-heading">Cookie Policy</h3>' in response.data
