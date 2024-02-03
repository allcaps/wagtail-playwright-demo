from playwright.sync_api import Page
from django.urls import reverse

from .conftest import USERNAME, PASSWORD


def test_one(live_server, page: Page, admin_user):
    # Pause, and start recording your browser interactions.
    # page.pause()

    url = live_server.url + reverse("wagtailadmin_login")
    page.goto(url)

    page.get_by_placeholder("Enter your username").fill(USERNAME)
    page.get_by_placeholder("Enter password").fill(PASSWORD)
    page.get_by_role("button", name="Sign in").click()

    expected = 'Welcome to the pytestplaywrightproject Wagtail CMS\njos'
    assert page.locator("#main").inner_text() == expected
