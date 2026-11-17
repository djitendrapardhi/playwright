"""Page object for ADT Help Experience Cloud site (Knowledge Search)."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, unquote, urlparse

from playwright.sync_api import Page, expect


class HelpSitePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    # --- Locators ---

    @property
    def search_textbox(self):
        return self.page.get_by_role("textbox", name="Search")

    @property
    def search_button(self):
        return self.page.get_by_role("button", name="Search")

    @property
    def results_summary(self):
        return self.page.get_by_text(re.compile(r"\d+\s*Results"))

    @property
    def article_titles(self):
        return self.page.locator("a.article-title")

    # --- Navigation ---

    def open_home(self) -> None:
        self.page.goto(f"{self.base_url}/s/", wait_until="domcontentloaded")
        expect(
            self.page.locator("div.searchHeader").filter(
                has_text="ADT Home Security Support Center"
            )
        ).to_be_visible(timeout=30000)
        expect(self.search_textbox).to_be_visible(timeout=30000)
        expect(self.search_textbox).to_be_enabled()

    def open_category(self, href_fragment: str, heading_text: str | None = None) -> None:
        # Prefer direct navigation: home tiles also link to prod help.adt.com articles
        # with similar labels, which makes click-based selection brittle.
        # Experience Cloud pages often never reach full "load"; use domcontentloaded.
        self.page.goto(
            f"{self.base_url}/s/{href_fragment}",
            wait_until="domcontentloaded",
        )
        assert re.search(href_fragment, self.page.url, re.I), (
            f"Expected URL to contain '{href_fragment}', got: {self.page.url}"
        )
        expect(self.search_textbox).to_be_visible(timeout=30000)
        if heading_text:
            # Category pages may repeat the label in nav and body; first match is enough.
            expect(self.page.get_by_text(heading_text, exact=False).first).to_be_visible(
                timeout=30000
            )

    def open_article_by_path(self, article_path: str) -> None:
        self.page.goto(
            f"{self.base_url}/s/article/{article_path}",
            wait_until="domcontentloaded",
        )
        expect(self.search_textbox).to_be_visible(timeout=30000)

    # --- Search actions ---

    def search(self, keyword: str) -> None:
        expect(self.search_textbox).to_be_visible(timeout=30000)
        self.search_textbox.click()
        self.search_textbox.fill("")
        self.search_textbox.press_sequentially(keyword, delay=40)
        self.search_button.click()
        # Prefer condition-based wait on results UI; avoid wait_for_url(load) on LWR/Aura.
        expect(self.page).to_have_url(re.compile(r"global-search"), timeout=30000)
        expect(self.results_summary.first).to_be_visible(timeout=30000)

    def open_article_from_results(self, title: str) -> None:
        expect(self.article_titles.first).to_be_visible(timeout=30000)
        self.article_titles.filter(has_text=title).first.click()
        expect(self.page).to_have_url(re.compile(r"/article/"), timeout=30000)
        expect(self.search_textbox).to_be_visible(timeout=30000)
        expect(self.search_textbox).to_be_enabled()

    # --- Assertions / helpers ---

    def result_title_texts(self) -> list[str]:
        expect(self.article_titles.first).to_be_visible(timeout=30000)
        return [t.strip() for t in self.article_titles.all_text_contents()]

    def assert_no_duplicate_titles(self) -> None:
        titles = self.result_title_texts()
        assert titles, "Expected at least one article title in search results"
        duplicates = sorted({t for t in titles if titles.count(t) > 1})
        assert not duplicates, f"Duplicate article labels found: {duplicates}"

    def assert_results_count_visible(self) -> None:
        expect(self.results_summary.first).to_be_visible(timeout=30000)

    def category_query_values(self) -> list[str]:
        parsed = urlparse(self.page.url)
        values = parse_qs(parsed.query).get("category", [])
        if not values:
            return []
        # Support comma-separated or %2C-separated developer names
        raw = unquote(values[0])
        return [part.strip() for part in raw.split(",") if part.strip()]

    def assert_url_has_category(self, *expected_dev_names: str) -> None:
        actual = set(self.category_query_values())
        expected = set(expected_dev_names)
        assert actual == expected, (
            f"Expected category param {sorted(expected)}, got {sorted(actual)} "
            f"from URL: {self.page.url}"
        )

    def assert_url_has_no_category(self) -> None:
        assert "category=" not in self.page.url, (
            f"Expected no category parameter, got URL: {self.page.url}"
        )
        assert not self.category_query_values()
