from playwright.sync_api import Page
from django.urls import reverse

from .conftest import USERNAME, PASSWORD


def test_one(live_server, page: Page, admin_user):
    """
    `live_server` triggers the transactional_db fixture,
    which flushes the db at the end of each test.

    Page objects are created via the `page` fixture,
    https://playwright.dev/python/docs/test-runners

    I'd like to think of Playwright 'page' as 'browser' or 'client',
    and am tempted to rename it as such.
    """
    url = live_server.url + reverse("wagtailadmin_login")
    page.goto(url)

    page.get_by_placeholder("Enter your username").fill(USERNAME)
    page.get_by_placeholder("Enter password").fill(PASSWORD)
    page.get_by_role("button", name="Sign in").click()

    # Just FYI, debugging is easy with Playwright:

    # Pause, and start recording your browser interactions.
    # page.pause()

    # Or set a breakpoint and interact with the browser through the console.
    # breakpoint()

    # Execute management commands.
    # from django.core.management import call_command
    # call_command('showmigrations')

    expected = 'Welcome to the pytestplaywrightproject Wagtail CMS\njos'
    assert page.locator("#main").inner_text() == expected
