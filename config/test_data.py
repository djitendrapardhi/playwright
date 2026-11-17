"""Synthetic test data for EDTCTS-3176 Knowledge Search Phase 2.

Story: EDTCTS-3176 Knowledge Search Phase 2:
Search from the article page within the same article's categories.

Note: Manual Setup steps (login → Setup → All Sites) are skipped in automation.
The Experience Cloud URL is taken from the approved test case Expected Result.
"""

HELP_SITE_URL = "https://adt--test3.sandbox.my.site.com/help"
HELP_HOME_URL = f"{HELP_SITE_URL}/s/"

SEARCH_KEYWORD = "ADT"

# Category tile used in TC_02
CATEGORY_NAME = "ADT smart home security"
CATEGORY_PATH = "adtsmarthomesecurity"
CATEGORY_DEV_NAME = "ADT_smart_home_security"

# Articles discovered in sandbox during locator exploration
MULTI_CATEGORY_ARTICLE_TITLE = "Second ADT article in Smart home security and Pulse"
MULTI_CATEGORY_ARTICLE_PATH = "Second-ADT-article-in-Smart-home-security-and-Pulse"
MULTI_CATEGORY_PARAM = "ADT_smart_home_security%2CPulse"  # comma-separated / URL-encoded

NO_CATEGORY_ARTICLE_TITLE = "ADT article NO category"
NO_CATEGORY_ARTICLE_PATH = "ADT-article-NO-category"

SINGLE_CATEGORY_ARTICLE_TITLE = "ADT Smart Home Security- Arming Your System"
SINGLE_CATEGORY_ARTICLE_PATH = "ADT-Smart-Home-Security-Arming-Your-System"
