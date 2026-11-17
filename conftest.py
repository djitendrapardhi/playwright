"""Shared Playwright fixtures for ADT Help Experience Cloud tests."""

import pytest

from config.test_data import HELP_SITE_URL
from pages.help_site import HelpSitePage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True,
    }


@pytest.fixture
def help_site(page) -> HelpSitePage:
    return HelpSitePage(page, HELP_SITE_URL)
