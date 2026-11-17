/**
 * EDTCTS-3176 Knowledge Search Phase 2
 * Story: Search from the article page within the same article's categories
 * Source: EDTCTS-3176.xlsx
 *
 * Manual Setup (login → Setup → All Sites) is skipped; tests open the
 * documented Experience Cloud URL directly.
 */
import { test, expect, type Page, type Locator } from '@playwright/test';

const HELP_SITE_URL = 'https://adt--test3.sandbox.my.site.com/help';
const SEARCH_KEYWORD = 'ADT';
const CATEGORY_NAME = 'ADT smart home security';
const CATEGORY_PATH = 'adtsmarthomesecurity';
const CATEGORY_DEV_NAME = 'ADT_smart_home_security';
const MULTI_CATEGORY_ARTICLE_TITLE =
  'Second ADT article in Smart home security and Pulse';
const NO_CATEGORY_ARTICLE_TITLE = 'ADT article NO category';
const SINGLE_CATEGORY_ARTICLE_TITLE =
  'ADT Smart Home Security- Arming Your System';

class HelpSitePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  get searchTextbox(): Locator {
    return this.page.getByRole('textbox', { name: 'Search' });
  }

  get searchButton(): Locator {
    return this.page.getByRole('button', { name: 'Search' });
  }

  get resultsSummary(): Locator {
    return this.page.getByText(/\d+\s*Results/);
  }

  get articleTitles(): Locator {
    return this.page.locator('a.article-title');
  }

  async openHome(): Promise<void> {
    await this.page.goto(`${HELP_SITE_URL}/s/`, { waitUntil: 'domcontentloaded' });
    await expect(
      this.page.locator('div.searchHeader').filter({
        hasText: 'ADT Home Security Support Center',
      }),
    ).toBeVisible({ timeout: 30_000 });
    await expect(this.searchTextbox).toBeVisible({ timeout: 30_000 });
    await expect(this.searchTextbox).toBeEnabled();
  }

  async openCategory(hrefFragment: string, headingText?: string): Promise<void> {
    // Direct nav avoids brittle home tiles that also link to prod help.adt.com.
    // Experience Cloud often never reaches full "load"; use domcontentloaded.
    await this.page.goto(`${HELP_SITE_URL}/s/${hrefFragment}`, {
      waitUntil: 'domcontentloaded',
    });
    expect(this.page.url()).toMatch(new RegExp(hrefFragment, 'i'));
    await expect(this.searchTextbox).toBeVisible({ timeout: 30_000 });
    if (headingText) {
      await expect(this.page.getByText(headingText).first()).toBeVisible({
        timeout: 30_000,
      });
    }
  }

  async search(keyword: string): Promise<void> {
    await expect(this.searchTextbox).toBeVisible({ timeout: 30_000 });
    await this.searchTextbox.click();
    await this.searchTextbox.fill('');
    await this.searchTextbox.pressSequentially(keyword, { delay: 40 });
    await this.searchButton.click();
    await expect(this.page).toHaveURL(/global-search/, { timeout: 30_000 });
    await expect(this.resultsSummary.first()).toBeVisible({ timeout: 30_000 });
  }

  async openArticleFromResults(title: string): Promise<void> {
    await expect(this.articleTitles.first()).toBeVisible({ timeout: 30_000 });
    await this.articleTitles.filter({ hasText: title }).first().click();
    await expect(this.page).toHaveURL(/\/article\//, { timeout: 30_000 });
    await expect(this.searchTextbox).toBeVisible({ timeout: 30_000 });
    await expect(this.searchTextbox).toBeEnabled();
  }

  async resultTitleTexts(): Promise<string[]> {
    await expect(this.articleTitles.first()).toBeVisible({ timeout: 30_000 });
    const titles = await this.articleTitles.allTextContents();
    return titles.map((t) => t.trim());
  }

  async assertNoDuplicateTitles(): Promise<void> {
    const titles = await this.resultTitleTexts();
    expect(titles.length, 'Expected at least one article title').toBeGreaterThan(0);
    const duplicates = [...new Set(titles.filter((t) => titles.filter((x) => x === t).length > 1))];
    expect(duplicates, `Duplicate article labels: ${duplicates.join(', ')}`).toEqual([]);
  }

  async assertResultsCountVisible(): Promise<void> {
    await expect(this.resultsSummary.first()).toBeVisible({ timeout: 30_000 });
  }

  categoryQueryValues(): string[] {
    const url = new URL(this.page.url());
    const raw = url.searchParams.get('category');
    if (!raw) return [];
    return raw
      .split(',')
      .map((part) => part.trim())
      .filter(Boolean);
  }

  assertUrlHasCategory(...expectedDevNames: string[]): void {
    const actual = new Set(this.categoryQueryValues());
    const expected = new Set(expectedDevNames);
    expect(
      [...actual].sort(),
      `Category mismatch for URL: ${this.page.url()}`,
    ).toEqual([...expected].sort());
  }

  assertUrlHasNoCategory(): void {
    expect(this.page.url(), `Expected no category param: ${this.page.url()}`).not.toContain(
      'category=',
    );
    expect(this.categoryQueryValues()).toEqual([]);
  }
}

test.describe('EDTCTS-3176 Knowledge Search Phase 2', () => {
  test.use({
    viewport: { width: 1280, height: 800 },
    ignoreHTTPSErrors: true,
  });

  test('TC_01 Article appears once and Search field appears on the article page', async ({
    page,
  }) => {
    const help = new HelpSitePage(page);

    await help.openHome();
    await help.search(SEARCH_KEYWORD);
    await help.assertResultsCountVisible();
    await help.assertNoDuplicateTitles();
    help.assertUrlHasNoCategory();

    const titles = await help.resultTitleTexts();
    await help.openArticleFromResults(titles[0]);

    await expect(help.searchTextbox).toBeVisible();
    await expect(help.searchTextbox).toBeEnabled();
    expect(page.url()).toContain('/article/');
  });

  test('TC_02 Single-category global results and suggestions', async ({ page }) => {
    const help = new HelpSitePage(page);

    await help.openHome();
    await help.search(SEARCH_KEYWORD);
    await help.assertResultsCountVisible();

    await help.openCategory(CATEGORY_PATH, CATEGORY_NAME);
    await help.search(SEARCH_KEYWORD);
    await help.assertResultsCountVisible();
    help.assertUrlHasCategory(CATEGORY_DEV_NAME);

    await help.openArticleFromResults(SINGLE_CATEGORY_ARTICLE_TITLE);
    await expect(help.searchTextbox).toBeVisible();
    await expect(help.searchTextbox).toBeEnabled();

    await help.search(SEARCH_KEYWORD);
    await help.assertResultsCountVisible();
    help.assertUrlHasCategory(CATEGORY_DEV_NAME);
  });

  test('TC_03 The article matches two or more metadata categories', async ({ page }) => {
    const help = new HelpSitePage(page);

    await help.openHome();
    await help.search(SEARCH_KEYWORD);
    await help.openArticleFromResults(MULTI_CATEGORY_ARTICLE_TITLE);

    await expect(help.searchTextbox).toBeVisible();
    await help.search(SEARCH_KEYWORD);
    await help.assertResultsCountVisible();

    const categories = help.categoryQueryValues();
    expect(
      categories.length,
      `Expected 2+ categories, got ${categories.join(',')} from ${page.url()}`,
    ).toBeGreaterThanOrEqual(2);
    expect(categories).toContain('ADT_smart_home_security');
    expect(categories).toContain('Pulse');
    expect(page.url().split('category=').length - 1).toBe(1);
  });

  test('TC_04 The article does not belong to any metadata category', async ({ page }) => {
    const help = new HelpSitePage(page);

    await help.openHome();
    await help.search(SEARCH_KEYWORD);
    await help.openArticleFromResults(NO_CATEGORY_ARTICLE_TITLE);

    await expect(help.searchTextbox).toBeVisible();
    await help.search(SEARCH_KEYWORD);
    await help.assertResultsCountVisible();
    help.assertUrlHasNoCategory();
  });
});
