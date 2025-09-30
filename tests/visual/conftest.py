"""
Playwright fixtures for visual regression tests
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for visual tests"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,  # For self-signed certs in dev
    }


@pytest.fixture
def page(page: Page):
    """Configure page for visual tests"""
    # Set default timeout
    page.set_default_timeout(10000)  # 10 seconds

    # Set viewport
    page.set_viewport_size({"width": 1280, "height": 720})

    return page


@pytest.fixture
def base_url():
    """Base URL for the application"""
    return "http://localhost:5001"


@pytest.fixture
def authenticated_page(page: Page, base_url):
    """Page with authenticated session"""
    # Navigate to demo mode to get auth
    page.goto(f"{base_url}/demo")

    # Should redirect to dashboard with auth
    page.wait_for_url(f"{base_url}/")

    return page
