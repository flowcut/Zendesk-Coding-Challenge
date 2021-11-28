"""Test log in and log out."""
from urllib.parse import urlparse

import bs4


def test_index_redirect(client):
    """GET /tickets_page/1 redirects to /accounts/login/ when user is not logged in."""
    response = client.get("/tickets_page/1/")
    assert response.status_code == 302
    urlpath = urlparse(response.location).path
    assert urlpath == "/accounts/login/"


def test_login(client):
    """Login umink."""
    response = client.post(
        "/accounts/login/",
        data={
            "emailaddress": "umink@umich.edu",
            "password": "Awin1m2n3b"
        },
    )
    assert response.status_code == 302
    urlpath = urlparse(response.location).path
    assert urlpath == "/tickets_page/1/"

def test_bad_login(client):
    """Login umink with wrong auth."""
    response = client.post(
        "/accounts/login/",
        data={
            "emailaddress": "umink@umich.edu",
            "password": "what?"
        },
    )
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "Authentication Failed." in text


def test_logout(client):
    """Logout after log in. """
    # Login
    response = client.post(
        "/accounts/login/",
        data={
            "emailaddress": "umink@umich.edu",
            "password": "Awin1m2n3b"
        },
    )
    assert response.status_code == 302
    urlpath = urlparse(response.location).path
    assert urlpath == "/tickets_page/1/"

    # Should be able to load the index page
    response = client.get("/tickets_page/1/")
    assert response.status_code == 200

    # Log out
    response = client.post("/accounts/logout/")
    assert response.status_code == 302
    urlpath = urlparse(response.location).path
    assert urlpath == "/accounts/login/"

    # Index should redirect to login
    response = client.get("/tickets_page/1/")
    assert response.status_code == 302
    urlpath = urlparse(response.location).path
    assert urlpath == "/accounts/login/"
