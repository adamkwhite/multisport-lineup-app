"""
Visual regression tests for login page
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.skip(reason="Visual tests require app to be running - run manually")
class TestLoginPageVisuals:
    """Visual regression tests for login page"""

    def test_login_page_initial_state(self, page: Page, base_url):
        """Test login page initial state screenshot"""
        page.goto(base_url)

        # Wait for page to load
        page.wait_for_load_state("networkidle")

        # Take screenshot
        expect(page).to_have_screenshot("login-page-initial.png")

    def test_demo_mode_button_visible(self, page: Page, base_url):
        """Test that demo mode button is visible"""
        page.goto(base_url)

        # Wait for page to load
        page.wait_for_load_state("networkidle")

        # Check for demo button or TeamSnap login
        page_content = page.content()
        assert "demo" in page_content.lower() or "teamsnap" in page_content.lower()

        # Take screenshot showing button state
        expect(page).to_have_screenshot("login-page-with-buttons.png")

    def test_login_page_responsive_mobile(self, page: Page, base_url):
        """Test login page on mobile viewport"""
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})

        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Take screenshot
        expect(page).to_have_screenshot("login-page-mobile.png")

    def test_login_page_responsive_tablet(self, page: Page, base_url):
        """Test login page on tablet viewport"""
        # Set tablet viewport
        page.set_viewport_size({"width": 768, "height": 1024})

        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Take screenshot
        expect(page).to_have_screenshot("login-page-tablet.png")
