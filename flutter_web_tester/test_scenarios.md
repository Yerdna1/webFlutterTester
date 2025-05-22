# Initial Test Scenarios for Unilabs Flutter Web App

## 1. Authentication
    - **TC1.1: Successful Login:**
        - Navigate to the login page.
        - Enter valid credentials (admin@unilabs.sk / malina).
        - Click the login button.
        - *Expected Result:* User is redirected to the dashboard/main page, and a welcome message or user-specific element is visible.
    - **TC1.2: Failed Login - Invalid Password:**
        - Navigate to the login page.
        - Enter valid username (admin@unilabs.sk) and an invalid password.
        - Click the login button.
        - *Expected Result:* An error message regarding incorrect credentials is displayed. User remains on the login page.
    - **TC1.3: Failed Login - Invalid Username:**
        - Navigate to the login page.
        - Enter an invalid username and a valid password.
        - Click the login button.
        - *Expected Result:* An error message regarding incorrect credentials is displayed. User remains on the login page.
    - **TC1.4: Successful Logout:**
        - (Assuming user is logged in)
        - Find and click the logout button/link.
        - *Expected Result:* User is redirected to the login page or a logged-out confirmation page.

## 2. Basic Navigation (Placeholder - Requires knowledge of actual site structure)
    - **TC2.1: Navigate to Main Sections:**
        - (Assuming user is logged in)
        - Identify main navigation links/menus (e.g., Dashboard, Settings, Profile, Reports).
        - For each main link:
            - Click the link.
            - *Expected Result:* The corresponding page loads successfully, and the title or a key header element matches the expected section.
    - **TC2.2: Breadcrumb Navigation (If applicable):**
        - (Assuming user is logged in and navigated to a sub-page)
        - If breadcrumbs exist, click on a parent link in the breadcrumb trail.
        - *Expected Result:* User is navigated to the correct parent page.

## 3. Form Interaction (Placeholder - Requires knowledge of forms on the site)
    - **TC3.1: Submit a Valid Form:**
        - (Assuming user is logged in and on a page with a form)
        - Fill all required fields with valid data.
        - Submit the form.
        - *Expected Result:* A success message is displayed, or data is updated/created as expected.
    - **TC3.2: Form Validation - Empty Required Fields:**
        - (Assuming user is logged in and on a page with a form)
        - Attempt to submit the form with one or more required fields left empty.
        - *Expected Result:* Validation error messages are displayed for the respective empty fields. Form submission is prevented.

## 4. Basic UI Checks
    - **TC4.1: Verify Page Titles:**
        - For each main page navigated to, verify that the page title (in the browser tab) is descriptive and correct.
    - **TC4.2: Check for Broken Images (Basic):**
        - (Requires enhancement later for comprehensive check)
        - On key pages, check if `<img>` tags have valid `src` attributes (superficial check, not checking if image actually loads yet).
    - **TC4.3: Check for JavaScript Console Errors (Basic):**
        - After page loads and basic interactions, check the browser's JavaScript console for any severe errors. (This will require Selenium to be configured to capture console logs).
