"""
Test the Studio help links.
"""

from flaky import flaky
from bok_choy.web_app_test import WebAppTest

from common.test.acceptance.tests.studio.base_studio_test import StudioCourseTest
from common.test.acceptance.pages.studio.index import DashboardPage
from common.test.acceptance.pages.studio.utils import click_studio_help, studio_help_links, get_element
from common.test.acceptance.pages.studio.index import IndexPage, HomePage, DashboardPageWithPrograms
from common.test.acceptance.tests.studio.base_studio_test import StudioLibraryTest
from common.test.acceptance.pages.studio.utils import click_css
from common.test.acceptance.pages.studio.library import LibraryPage
from common.test.acceptance.pages.studio.users import LibraryUsersPage
from common.test.acceptance.tests.helpers import (
    assert_links,
    assert_help_is_open
)
from common.test.acceptance.pages.studio.import_export import ExportLibraryPage, ImportLibraryPage
from common.test.acceptance.pages.studio.auto_auth import AutoAuthPage


NAV_HELP_CSS = '.nav-item.nav-account-help a'
SIDE_BAR_HELP_CSS = '.bit.external-help a'


class StudioHelpTest(StudioCourseTest):
    """Tests for Studio help."""

    @flaky  # TODO: TNL-4954
    def test_studio_help_links(self):
        """Test that the help links are present and have the correct content."""
        page = DashboardPage(self.browser)
        page.visit()
        click_studio_help(page)
        links = studio_help_links(page)
        expected_links = [{
            'href': u'http://docs.edx.org/',
            'text': u'edX Documentation',
            'sr_text': u'Access documentation on http://docs.edx.org'
        }, {
            'href': u'https://open.edx.org/',
            'text': u'Open edX Portal',
            'sr_text': u'Access the Open edX Portal'
        }, {
            'href': u'https://www.edx.org/course/overview-creating-edx-course-edx-edx101#.VO4eaLPF-n1',
            'text': u'Enroll in edX101',
            'sr_text': u'Enroll in edX101: Overview of Creating an edX Course'
        }, {
            'href': u'https://www.edx.org/course/creating-course-edx-studio-edx-studiox',
            'text': u'Enroll in StudioX',
            'sr_text': u'Enroll in StudioX: Creating a Course with edX Studio'
        }, {
            'href': u'mailto:partner-support@example.com',
            'text': u'Contact Us',
            'sr_text': 'Send an email to partner-support@example.com'
        }]
        for expected, actual in zip(expected_links, links):
            self.assertEqual(expected['href'], actual.get_attribute('href'))
            self.assertEqual(expected['text'], actual.text)
            self.assertEqual(
                expected['sr_text'],
                actual.find_element_by_xpath('following-sibling::span').text
            )


class SignInAndSignUpHelpTest(WebAppTest):
    """
    Tests help links on 'Sign In' and 'Sign Up' pages.
    """
    def setUp(self):
        super(SignInAndSignUpHelpTest, self).setUp()
        self.index_page = IndexPage(self.browser)

    def test_help_links_on_signup_and_sign_in_pages(self):
        """
        Scenario: Help link in navigation bar is working on
        'Sign Up' and 'Sign In' page.
        Given that I am on the 'Sign Up' or 'Sign In' page.
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'getting_started/get_started.html'

        """
        expected_links = [
            {
                'element_css': '.nav-item.nav-not-signedin-help a',
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff'
                       '/en/latest/getting_started/get_started.html',
                'page': 'index-sign-in'
            },
            {
                'element_css': '.nav-item.nav-not-signedin-help a',
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html',
                'page': 'index-sign-up'
            }
        ]

        for expected_link in expected_links:
            self.index_page.visit()
            page = expected_link['page']

            if page == 'index-sign-in':
                page = self.index_page.click_sign_in()
            else:
                page = self.index_page.click_sign_up()

            element_css = expected_link['element_css']
            actual_link = get_element(page, element_css)
            # Assert that link on DOM element are same as expected.
            assert_links(self, expected_link, actual_link)
            # Click the help link and assert that correct link is opened.
            click_css(page, element_css, 0, False)
            assert_help_is_open(self, expected_link['url'])


class HomeHelpTest(StudioCourseTest):
    """
    Tests help links on 'Home'(Courses tab) page.
    """
    def setUp(self):  # pylint: disable=arguments-differ
        super(HomeHelpTest, self).setUp()
        self.home_page = HomePage(self.browser)

    def test_course_home_help(self):
        """
        Scenario: Help link in navigation and side bar is working on 'Home'(Courses tab) page.
        Given that I am on the 'Home'(Courses tab) page.
        And I click the 'Help' in the navigation bar
        Then help link should open.
        And help url should contain 'getting_started/get_started.html'

        Given that I am on the 'Home'(Courses tab) page.
        And I want help about the courses
        And I click the 'Getting Started with edX Studio' in the sidebar links
        Then Help link should open.
        And help url should contain 'getting_started/get_started.html'

        """
        expected_links = [
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html'
            },
            {
                'element_css': '.bit li.action-item a',
                'text': 'Getting Started with edX Studio',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html'
            }
        ]

        for expected_link in expected_links:
            self.home_page.visit()
            element_css = expected_link['element_css']
            actual_link = get_element(self.home_page, element_css)
            # Assert that link on DOM element are same as expected.
            assert_links(self, expected_link, actual_link)
            # Click the help link and assert that correct link is opened.
            click_css(self.home_page, element_css, 0, False)
            assert_help_is_open(self, expected_link['url'])


class NewCourseAndNewLibraryHelpTest(WebAppTest):
    """
    Test help links while creating new course and new library
    """
    def setUp(self):
        super(NewCourseAndNewLibraryHelpTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)
        self.program_page = DashboardPageWithPrograms(self.browser)

    def test_new_course_and_new_library_help(self):
        """
        Scenario: Help link in navigation bar and sidebar is working on 'Create a New Course'
        and 'Create a new Library' page in the dashboard. Also Help link in navigation bar
        on 'Library tab' at dashboard page should be working.

        Given that I am on the 'Create a New Course' page in the dashboard.
        And I want help about the process
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'getting_started/get_started.html'

        Given that I am on the 'Create a New Course' page in the dashboard.
        And I want help about the process
        And I click the 'Getting Started with edX Studio' in the sidebar links
        Then Help link should open.
        And help url should contain 'getting_started/get_started.html'

        Given that I am on the 'Create a New Library' page in the dashboard.
        And I want help about the process
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'getting_started/get_started.html'

        Given that I am on the 'Create a New Library' page in the dashboard.
        And I want help about the process
        And I click the 'Getting Started with edX Studio' in the sidebar links
        Then Help link should open.
        And help url should contain with 'getting_started/get_started.html'

        Given that I am on the 'Home'(Courses tab) page.
        And I want help about the process
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'getting_started/get_started.html'
        """
        expected_links = [
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff'
                       '/en/latest/getting_started/get_started.html',
                'type': 'course'
            },
            {
                'element_css': '.bit li.action-item a',
                'text': 'Getting Started with edX Studio',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html',
                'type': 'course'
            },
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html',
                'type': 'library'
            },
            {
                'element_css': '.bit li.action-item a',
                'text': 'Getting Started with edX Studio',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html',
                'type': 'library'
            },
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/getting_started/get_started.html',
                'type': 'library tab'
            }
        ]
        for expected_link in expected_links:
            self.auth_page.visit()
            self.dashboard_page.visit()
            if expected_link['type'] == 'course':
                self.dashboard_page.click_new_course_button()
            elif expected_link['type'] == 'library':
                self.dashboard_page.click_new_library()
            else:
                self.assertTrue(self.dashboard_page.has_new_library_button)
                click_css(self.dashboard_page, '#course-index-tabs .libraries-tab', 0, False)

            element_css = expected_link['element_css']
            # Assert that link on DOM element are same as expected.
            actual_link = get_element(self.dashboard_page, element_css)
            assert_links(self, expected_link, actual_link)
            # Click the help link and assert that correct link is opened.
            click_css(self.dashboard_page, element_css, 0, False)
            assert_help_is_open(self, expected_link['url'])


class LibraryHelpTest(StudioLibraryTest):
    """
    Test help links on a Library page.
    """
    def setUp(self):
        super(LibraryHelpTest, self).setUp()
        self.library_page = LibraryPage(self.browser, self.library_key)
        self.library_user_page = LibraryUsersPage(self.browser, self.library_key)

    def test_library_content_and_library_user_access_help(self):
        """
        Scenario: Help links in navigation bar and sidebar are working on content
        library page(click a library on the Library list page). Also Help link in
        navigation bar is working on 'User Access' settings page of library.

        Given that I am on the content library page(click a library on the Library list page).
        And I want help
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'course/components/libraries.html'

        Given that I am on the content library page(click a library on the Library list page).
        And I want help
        And I click the 'Learn more about content libraries' in the sidebar links
        Then Help link should open.
        And help url should contain 'course/components/libraries.html'

        Given that I am on the 'User Access' settings page of library.
        And I want help
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain
        'creating_content/libraries.html#give-other-users-access-to-your-library'
        """
        expected_links = [
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/course_components/libraries.html',
                'page': self.library_page
            },
            {
                'element_css': SIDE_BAR_HELP_CSS,
                'text': 'Learn more about content libraries',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/'
                       'en/latest/course_components/libraries.html',
                'page': self.library_page
            },
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/latest'
                       '/course_components/libraries.html#give-other-users-access-to-your-library',
                'page': self.library_user_page
            }
        ]
        for expected_link in expected_links:
            page = expected_link['page']
            page.visit()
            element_css = expected_link['element_css']
            # Assert that link on DOM element are same as expected.
            actual_link = get_element(page, element_css)
            assert_links(self, expected_link, actual_link)
            # Click the help link and assert that correct link is opened.
            click_css(page, element_css, 0, False)
            assert_help_is_open(self, expected_link['url'])


class LibraryImportAndExportHelpTest(StudioLibraryTest):
    """
    Test help links on a Library import and export pages.
    """
    def setUp(self):
        super(LibraryImportAndExportHelpTest, self).setUp()
        self.library_import_page = ImportLibraryPage(self.browser, self.library_key)
        self.library_export_page = ExportLibraryPage(self.browser, self.library_key)

    def test_library_import_and_export_help(self):
        """
        Scenario: Help links in navigation and side bar are working on Library import
        and export pages.

        Given that I am on the Library import page.
        And I want help about the process
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'creating_content/libraries.html#import-a-library'

        Given that I am on the Library import page.
        And I want help about the process
        And I click the 'Learn more about importing a library' in the sidebar links
        Then Help link should open.
        And help url should contain 'creating_content/libraries.html#import-a-library'

        Given that I am on the Library export page.
        And I want help about the process
        And I click the 'Help' in the navigation bar
        Then Help link should open.
        And help url should contain 'creating_content/libraries.html#export-a-library'

        Given that I am on the Library export page.
        And I want help about the process
        And I click the 'Learn more about exporting a library' in the sidebar links
        Then Help link should open.
        And help url should contain 'creating_content/libraries.html#export-a-library'
        """
        expected_links = [
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/'
                       'latest/course_components/libraries.html#import-a-library',
                'page': self.library_import_page
            },
            {
                'element_css': SIDE_BAR_HELP_CSS,
                'text': 'Learn more about importing a library',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/'
                       'latest/course_components/libraries.html#import-a-library',
                'page': self.library_import_page
            },
            {
                'element_css': NAV_HELP_CSS,
                'text': 'Help',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/'
                       'latest/course_components/libraries.html#export-a-library',
                'page': self.library_export_page
            },
            {
                'element_css': SIDE_BAR_HELP_CSS,
                'text': 'Learn more about exporting a library',
                'url': 'http://edx.readthedocs.org/projects/edx-partner-course-staff/en/'
                       'latest/course_components/libraries.html#export-a-library',
                'page': self.library_export_page
            }
        ]
        for expected_link in expected_links:
            page = expected_link['page']
            page.visit()
            element_css = expected_link['element_css']
            # Assert that link on DOM element are same as expected.
            actual_link = get_element(page, element_css)
            assert_links(self, expected_link, actual_link)
            # Click the help link and assert that correct link is opened.
            click_css(page, element_css, 0, False)
            assert_help_is_open(self, expected_link['url'])
