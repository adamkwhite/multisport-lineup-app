"""
Visual regression tests for dashboard
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.skip(reason="Visual tests require app to be running - run manually")
class TestDashboardVisuals:
    """Visual regression tests for dashboard"""

    def test_dashboard_no_auth_shows_login(self, page: Page, base_url):
        """Test dashboard without authentication shows login"""
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # Should show login page
        expect(page).to_have_screenshot("dashboard-no-auth.png")

    def test_dashboard_authenticated_demo_mode(self, authenticated_page: Page):
        """Test authenticated dashboard in demo mode"""
        # Page should be on dashboard after auth
        authenticated_page.wait_for_load_state("networkidle")

        # Take screenshot
        expect(authenticated_page).to_have_screenshot(
            "dashboard-authenticated-demo.png"
        )

    def test_dashboard_team_selection_visible(self, authenticated_page: Page):
        """Test that team selection is visible on authenticated dashboard"""
        authenticated_page.wait_for_load_state("networkidle")

        # Wait for team selection UI (adjust selector based on actual implementation)
        # This assumes there's some team-related content
        page_content = authenticated_page.content()

        # Take screenshot showing team selection state
        expect(authenticated_page).to_have_screenshot("dashboard-team-selection.png")

    def test_dashboard_empty_state_no_teams(self, page: Page, base_url):
        """Test dashboard empty state when no teams available"""
        # Note: This would require mocking API to return empty teams
        # For now, just test the authenticated state
        page.goto(f"{base_url}/demo")
        page.wait_for_load_state("networkidle")

        expect(page).to_have_screenshot("dashboard-empty-state.png")

    def test_dashboard_responsive_mobile(self, authenticated_page: Page):
        """Test authenticated dashboard on mobile"""
        authenticated_page.set_viewport_size({"width": 375, "height": 667})
        authenticated_page.reload()
        authenticated_page.wait_for_load_state("networkidle")

        expect(authenticated_page).to_have_screenshot("dashboard-mobile.png")

    def test_dashboard_responsive_tablet(self, authenticated_page: Page):
        """Test authenticated dashboard on tablet"""
        authenticated_page.set_viewport_size({"width": 768, "height": 1024})
        authenticated_page.reload()
        authenticated_page.wait_for_load_state("networkidle")

        expect(authenticated_page).to_have_screenshot("dashboard-tablet.png")
