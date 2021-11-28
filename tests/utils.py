"""test suite utility functions."""
import pathlib
import time
import requests
import zticketviewer
from zticketviewer.config import TEST_AUTH


# Directory containing unit tests
TEST_DIR = pathlib.Path(__file__).parent

def wait_job_done(job_status, waiting_period=3):
    while job_status['status'] != 'completed':
        time.sleep(waiting_period)
        x = requests.get(
            job_status['url'],
            auth=TEST_AUTH
        )
        job_status = x.json()['job_status']
