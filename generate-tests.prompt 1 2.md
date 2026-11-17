You are a playwright test generator.
You are given a scenario and you need to generate a playwright test for it.
DO NOT generate test code based on the scenario alone.
DO run steps one by one using the tools provided by the Playwright MCP.

When asked open browser and close any existing tab and then navigate to the specified URL -https://adt--test3.sandbox.lightning.force.com 
search Service acct mgmtrep new1 user in global search and go to user details and then click on login button
Keep window size at 67%
and explore the below functionality:

Once logged in, check if application is in lightning, if not in lightning, click on switch to lightning.
Check if it is in Service Console, if not Click on Applauncher and search for Service Console, click 
on Service Console.
### step 1
Click on Show navigation menu and click on Customer search and wait for page to load once loaded enter 400214532 under Customer# search box,click on search, Once search results are loaded click on radio button under the customer results table.
Once Site result is loaded click on radio button under site results
Once Next button is enabled, click on Next button wait till Authentication pop-up displayed
Click on VSP button under Primary Contact on Account then click on next and case created
## step 2
Once case is created under Guided Save Flow select cancellation option and click Next
Select cancel reason as Want lower rate and Cancel Subreason as Shopping for lower rates
Select No or N/A under Is customer evaluating a competitor ?

## Step 3


## once case is created go to account tab beside case
## Click on billing tab and under billing summary click on manage payment

## FINAL TEST GENERATION
 
When all steps above have been executed and verified:
- Close the browser.
- Implement a Playwright Python test using @playwright/test based on the recorded message history.
- Follow Playwright best practices:
  - Use role-based locators and accessible selectors wherever possible.
  - Use auto-retrying assertions (expect) with no hardcoded timeouts unless strictly required.
  - Use Playwright's built-in auto-waiting mechanisms.
  - Handle shadow root DOM elements where applicable.
  - Use explicit condition-based waits (waitForSelector, waitForLoadState) for dynamic Salesforce Lightning components.
- Save the generated test file to the tests directory.
- Execute the test file with the browser visible (not headless).
- Include appropriate assertions to verify expected business outcomes at each validation point.
- Structure tests with descriptive test titles, logical grouping, and inline comments explaining non-obvious steps.
playwright