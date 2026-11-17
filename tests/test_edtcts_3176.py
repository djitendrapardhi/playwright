"""
Automated tests for EDTCTS-3176 Knowledge Search Phase 2.

Traceability:
  Story: EDTCTS-3176
  Subject: Knowledge Search Phase 2: Search from the article page
           within the same article's categories
  Source: EDTCTS-3176.xlsx (manual design steps)

Automation note:
  Manual Steps 2–6 (Salesforce login → Setup → All Sites → copy URL)
  are replaced by direct navigation to the documented Experience Cloud URL.
  Needs Clarification if ADT Help User auth is required for gated content.
"""

import pytest
from playwright.sync_api import expect

from config import test_data as data


@pytest.mark.edtcts_3176
def test_tc01_article_appears_once_and_search_on_article_page(help_site):
    """
    EDTCTS-3176 TC_01: Article appears once and Search field appears on the article page
    AC coverage: global search results unique by label; article page exposes Search.
    """
    help_site.open_home()
    help_site.search(data.SEARCH_KEYWORD)

    help_site.assert_results_count_visible()
    help_site.assert_no_duplicate_titles()
    help_site.assert_url_has_no_category()

    titles = help_site.result_title_texts()
    first_title = titles[0]
    help_site.open_article_from_results(first_title)

    expect(help_site.search_textbox).to_be_visible()
    expect(help_site.search_textbox).to_be_enabled()
    assert "/article/" in help_site.page.url


@pytest.mark.edtcts_3176
def test_tc02_single_category_global_results_and_suggestions(help_site):
    """
    EDTCTS-3176 TC_02: Single-category global results and suggestions
    AC coverage: search from category home and from categorized article
    limits results via category query parameter.
    """
    help_site.open_home()
    help_site.search(data.SEARCH_KEYWORD)
    help_site.assert_results_count_visible()

    help_site.open_category(data.CATEGORY_PATH, heading_text=data.CATEGORY_NAME)
    help_site.search(data.SEARCH_KEYWORD)
    help_site.assert_results_count_visible()
    help_site.assert_url_has_category(data.CATEGORY_DEV_NAME)

    help_site.open_article_from_results(data.SINGLE_CATEGORY_ARTICLE_TITLE)
    expect(help_site.search_textbox).to_be_visible()
    expect(help_site.search_textbox).to_be_enabled()

    help_site.search(data.SEARCH_KEYWORD)
    help_site.assert_results_count_visible()
    help_site.assert_url_has_category(data.CATEGORY_DEV_NAME)


@pytest.mark.edtcts_3176
def test_tc03_article_matches_two_or_more_metadata_categories(help_site):
    """
    EDTCTS-3176 TC_03: The article matches two or more metadata categories
    AC coverage: site result URL has one category parameter with developer
    names separated by comma / %2C.
    """
    help_site.open_home()
    help_site.search(data.SEARCH_KEYWORD)
    help_site.open_article_from_results(data.MULTI_CATEGORY_ARTICLE_TITLE)

    expect(help_site.search_textbox).to_be_visible()
    help_site.search(data.SEARCH_KEYWORD)
    help_site.assert_results_count_visible()

    categories = help_site.category_query_values()
    assert len(categories) >= 2, (
        f"Expected 2+ category developer names, got {categories} "
        f"from URL: {help_site.page.url}"
    )
    assert "ADT_smart_home_security" in categories
    assert "Pulse" in categories
    assert help_site.page.url.count("category=") == 1


@pytest.mark.edtcts_3176
def test_tc04_article_without_metadata_category(help_site):
    """
    EDTCTS-3176 TC_04: The article doesn’t belong to any metadata category
    AC coverage: results include all categories; URL has no category parameter.
    """
    help_site.open_home()
    help_site.search(data.SEARCH_KEYWORD)
    help_site.open_article_from_results(data.NO_CATEGORY_ARTICLE_TITLE)

    expect(help_site.search_textbox).to_be_visible()
    help_site.search(data.SEARCH_KEYWORD)
    help_site.assert_results_count_visible()
    help_site.assert_url_has_no_category()
