# Test 400 page
def test_bad_request_error(client):
    response = client.get("/test/bad_request_route", follow_redirects=True)
    assert response.status_code == 400
    assert b'<h3 class="campaigns-heading">400 Bad Request</h3>' in response.data


# Test 403 page
def test_access_denied_error(client):
    response = client.get("/test/restricted_route", follow_redirects=True)
    assert response.status_code == 403
    assert b'<h3 class="campaigns-heading">403 Forbidden</h3>' in response.data


# Test 404 page
def test_not_found_error(client):
    response = client.get("/test/nonexistent_route")
    assert response.status_code == 404
    assert b'<h3 class="campaigns-heading">404 Not Found</h3>' in response.data


# Test 429 page
def test_too_many_requests_error(client):
    response = client.get("/test/too_many_requests_route")
    assert response.status_code == 429
    assert b'<h3 class="campaigns-heading">429 Too Many Requests</h3>' in response.data


# Test 500 page
def test_internal_error(client):
    response = client.get("/test/server_error_route")
    assert response.status_code == 500
    assert b'<h3 class="campaigns-heading">500 Internal Server Error</h3>' in response.data
