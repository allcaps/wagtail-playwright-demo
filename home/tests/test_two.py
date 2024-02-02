from playwright.sync_api import Page
from django.urls import reverse
from wagtail.models import Locale
from django.conf import settings
from .conftest import USERNAME, PASSWORD
from django.contrib.auth.models import Permission


def test_two(live_server, page: Page, admin_user):
    """
    `live_server` triggers the transactional_db fixture,
    which flushes the db at the end of each test.

    Page objects are created via the `page` fixture,
    https://playwright.dev/python/docs/test-runners
    I'd like to think of Playwright page as 'browser' or 'client',
    and am tempted to rename it as such.
    """
    # url = live_server.url + reverse("wagtailadmin_login")
    # page.goto(url)
    #
    # page.get_by_placeholder("Enter your username").fill(USERNAME)
    # page.get_by_placeholder("Enter password").fill(PASSWORD)
    # page.get_by_role("button", name="Sign in").click()

    # Same as `test_one`, but now it fails! :/
    # expected = 'Welcome to the playwritedemoproject Wagtail CMS\njos'
    # assert page.locator("#main").inner_text() == expected

    # Seems that Wagtail creates content via data migrations,
    # and this content is flushed after the first test. :/
    from wagtail.models import Page as WagtailPage, Site
    assert WagtailPage.objects.count() == 0
    assert Site.objects.count() == 0

    # The permissions are available.
    assert Permission.objects.filter(name="Can access Wagtail admin").exists()

    # And the admin user has the permission.
    permission = Permission.objects.get(name="Can access Wagtail admin")
    assert admin_user.user_permissions.filter(pk=permission.pk).exists()

    """
    So, let's create the expected Wagtail content.
    
    This code should live in a fixture, so it can be reused in other tests. 
    This fixture shouldn't do anything if the content is already available.  
    
    // Begin of fixture  
    """
    Locale.objects.create(language_code=settings.LANGUAGE_CODE)
    # From `wagtail/migrations/0001_squashed_0016_change_page_url_path_to_text_field.py:9`
    from django.apps import apps  # noqa
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")

    # Create page content type
    page_content_type, created = ContentType.objects.get_or_create(
        model="page", app_label="wagtailcore"
    )

    # Create root page
    root = Page.objects.create(
        title="Root",
        slug="root",
        content_type=page_content_type,
        path="0001",
        depth=1,
        numchild=1,
        url_path="/",
    )

    # Create homepage
    homepage = Page.objects.create(
        title="Welcome to your new Wagtail site!",
        slug="home",
        content_type=page_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/home/",
    )

    # Create default site
    Site.objects.get_or_create(
        hostname="localhost", root_page_id=homepage.id, is_default_site=True
    )
    """
    // End of fixture
    """

    # Now, the expected Wagtail content is available.
    # Let's try the test again.
    url = live_server.url + reverse("wagtailadmin_login")
    page.goto(url)

    page.get_by_placeholder("Enter your username").fill(USERNAME)
    page.get_by_placeholder("Enter password").fill(PASSWORD)
    page.get_by_role("button", name="Sign in").click()

    expected = 'Welcome to the pytestplaywrightproject Wagtail CMS\njos'
    assert page.locator("#main").inner_text() == expected
