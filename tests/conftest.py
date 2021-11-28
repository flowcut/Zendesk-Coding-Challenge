"""Shared test fixtures."""
import requests
import pytest
from tests.utils import wait_job_done
import zticketviewer
from zticketviewer.config import TEST_AUTH


@pytest.fixture(name="client")
def client_setup_teardown():

    # Configure Flask test server
    zticketviewer.app.config["TESTING"] = True

    with zticketviewer.app.test_client() as client:
        yield client

    clean_tickets()

def clean_tickets():

    ticket_id2delete_str = ""
    url = "https://zccumink.zendesk.com/api/v2/tickets.json?page=1"    
    r = requests.get(url, auth=TEST_AUTH)
    while r.json()["count"] != 0:        

        for ticket in r.json()["tickets"]:
            ticket_id2delete_str += str(ticket["id"]) + ","
        
        ticket_id2delete_str = ticket_id2delete_str[:-1]

        x = requests.delete(
            "https://zccumink.zendesk.com/api/v2/tickets/destroy_many.json?ids=%s" % ticket_id2delete_str,
            auth=TEST_AUTH
        )

        wait_job_done(x.json()['job_status'])

        r = requests.get(url, auth=TEST_AUTH)
        ticket_id2delete_str = ""

