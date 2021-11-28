"""Check index pages."""
import re
import bs4
import requests
from tests.utils import wait_job_done
from tests import utils
from requests.auth import HTTPBasicAuth
import json

from zticketviewer.config import TEST_AUTH

def test_nonsense(client):
    """Verify error message when getting wrong url."""
    response = client.post(
        "/accounts/login/",
        data={
            "emailaddress": "umink@umich.edu",
            "password": "Awin1m2n3b"
        },
    )
    assert response.status_code == 302

    response = client.get("/tickets_page/what/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "404" in text

    response = client.get("/tickets_page/1.2/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "404" in text

    response = client.get("/zendesk/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "404" in text

def test_list(client):
    """
    Verify expected lists of tickets present in /tickets_page/ URL.
    To save bulk import limit, the single ticket test is included here.
    """
    # Log in
    response = client.post(
        "/accounts/login/",
        data={
            "emailaddress": "umink@umich.edu",
            "password": "Awin1m2n3b"
        },
    )
    assert response.status_code == 302

    # Load and parse index page
    response = client.get("/tickets_page/1/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "Page # 1 | Total 0 tickets" in text

    tickets = [x for x in soup.find_all("div", "ticket")]
    assert len(tickets) == 0

    x = requests.post(
        "https://zccumink.zendesk.com/api/v2/imports/tickets/create_many.json",
        json=json.load(open(utils.TEST_DIR/"data/tickets.json")),
        auth=TEST_AUTH
    )

    wait_job_done(x.json()['job_status'])

    response = client.get("/tickets_page/1/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    tickets = [x for x in soup.find_all("div", "ticket")]
    assert len(tickets) == 25

    response = client.get("/tickets_page/2/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    tickets = [x for x in soup.find_all("div", "ticket")]
    assert len(tickets) == 5

    # Check nonexisting display page
    response = client.get("/tickets_page/3/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "404" in text

    # Check nonexisting api page
    response = client.get("/tickets_page/88888888888/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "404" in text

    url = "https://zccumink.zendesk.com/api/v2/tickets.json?page=1"
    r = requests.get(url, auth=TEST_AUTH)
    tickets = r.json()["tickets"]
    print(tickets)

    response = client.get("/ticket/%d/" % tickets[0]["id"])
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "Aute ex sunt" in text

    response = client.get("/ticket/%d/" % tickets[-1]["id"])
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "Laborum non est" in text

    response = client.get("/ticket/8888888888/")
    assert response.status_code == 200
    soup = bs4.BeautifulSoup(response.data, "html.parser")
    text = soup.get_text()
    assert "404" in text

    