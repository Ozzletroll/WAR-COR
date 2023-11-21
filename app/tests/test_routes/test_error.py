# Test 403 page
def test_access_denied_error(client):
    response = client.get("/test/restricted_route", follow_redirects=True)
    assert response.status_code == 403
    assert b'<h3 class="campaigns-heading">ERROR 403 ACCESS DENIED</h3>' in response.data


# Test 404 page
def test_not_found_error(client):
    response = client.get("/test/nonexistent_route")
    assert response.status_code == 404
    assert b'<h3 class="campaigns-heading">ERROR 404 NOT FOUND</h3>' in response.data


# Test 500 page
def test_internal_error(client):
    response = client.get("/test/server_error_route")
    assert response.status_code == 500
    assert b'<h3 class="campaigns-heading">ERROR 500 INTERNAL SERVER ERROR</h3>' in response.data
