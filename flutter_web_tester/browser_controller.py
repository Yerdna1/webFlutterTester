from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
# import time # For adding a pause - Removing for this attempt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException # Explicitly listed for clarity

class BrowserController:
    """
    Manages Selenium WebDriver interactions for browser automation.
    Designed for use in scripted (non-AI agent) tests.
    """
    def __init__(self):
        """Initializes the Chrome WebDriver with headless and common CI options."""
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu") 
            options.add_argument("--window-size=1920x1080")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            # Log error or handle more gracefully if needed in a larger framework
            # print(f"Critical error initializing WebDriver: {e}") 
            self.driver = None # Ensure driver is None if init fails
            raise # Re-raise to make it clear initialization failed

    def open_url(self, url: str) -> None:
        """
        Navigates the browser to the given URL.
        Args:
            url: The URL to navigate to.
        Raises:
            WebDriverException: If navigation fails.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot open URL.")
        self.driver.get(url) # Selenium's get itself doesn't return a value

    def get_title(self) -> str:
        """
        Returns the title of the current page.
        Returns:
            The title of the page.
        Raises:
            WebDriverException: If title cannot be retrieved.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot get title.")
        return self.driver.title

    def get_current_url(self) -> str:
        """
        Returns the current URL of the browser.
        Returns:
            The current URL.
        Raises:
            WebDriverException: If URL cannot be retrieved.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot get current URL.")
        return self.driver.current_url

    def find_element(self, by: str, value: str, timeout: int = 10) -> WebElement:
        """
        Uses WebDriverWait to find and return a web element.
        Args:
            by: The Selenium By strategy (e.g., By.XPATH, By.ID, or their string equivalents like "xpath", "id").
            value: The selector value.
            timeout: Maximum time (in seconds) to wait for the element.
        Returns:
            The found WebElement.
        Raises:
            TimeoutException: If the element is not found within the timeout.
            ValueError: If 'by' strategy is unsupported.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot find element.")
        
        actual_by: str # Selenium's By constants are strings (e.g., By.XPATH is "xpath")
        if not isinstance(by, str):
            raise ValueError(f"Invalid 'by' strategy type: {type(by)}. Must be a string (e.g., By.XPATH which is 'xpath').")

        # Ensure the provided 'by' string is a valid Selenium strategy.
        # These are the string values defined in selenium.webdriver.common.by.By
        valid_strategies = ["id", "xpath", "link text", "partial link text", 
                            "name", "tag name", "class name", "css selector"]
        if by.lower() not in valid_strategies:
            raise ValueError(f"Unsupported 'by' strategy string: '{by}'. Supported strategies are: {valid_strategies}")
        
        actual_by = by.lower() # Use the validated, lowercased string directly
        
        # WebDriverWait will raise TimeoutException if element not visible
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((actual_by, value))
        )
        return element

    def click_element(self, by: str, value: str, timeout: int = 10) -> None:
        """
        Finds an element and clicks it.
        Args:
            by: The Selenium By strategy or its string equivalent.
            value: The selector value.
            timeout: Maximum time to wait for the element to be clickable.
        Raises:
            TimeoutException: If the element is not found or not clickable within timeout.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot click element.")
        element = self.find_element(by, value, timeout) # find_element now raises TimeoutException
        # Consider waiting for clickability if issues arise with stale elements, etc.
        # WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
        element.click()

    def type_into_element(self, by: str, value: str, text: str, timeout: int = 10, press_enter_after: bool = False) -> None:
        """
        Finds an element, clears it, and types the given text into it.
        Optionally presses Enter after typing.
        Args:
            by: The Selenium By strategy or its string equivalent.
            value: The selector value.
            text: The text to type into the element.
            timeout: Maximum time to wait for the element.
            press_enter_after: If True, presses Enter key after sending text.
        Raises:
            TimeoutException: If the element is not found within timeout.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot type into element.")
        
        try:
            element = self.find_element(by, value, timeout=timeout)
            element.clear()  # Good practice before typing
            element.send_keys(text)
            if press_enter_after:
                element.send_keys(Keys.ENTER)
        except TimeoutException:
            # The print statement from the subtask description is good for debugging.
            print(f"Timeout: Element not found or not interactable by {by}='{value}' for typing.")
            raise


    def login(self, login_url: str, username: str, password: str, 
              email_field_by: str, email_field_value: str, 
              password_field_by: str, password_field_value: str, 
              login_button_by: str, login_button_value: str,
              press_enter_on_username: bool = False) -> None:
        """
        Performs a login sequence: navigates to URL, enters credentials, and clicks login.
        Success is implied by no exceptions. Test scripts should verify post-login state.
        Args:
            login_url: The URL of the login page.
            username: The username.
            password: The password.
            email_field_by: By strategy for email field.
            email_field_value: Selector for email field.
            password_field_by: By strategy for password field.
            password_field_value: Selector for password field.
            login_button_by: By strategy for login button.
            login_button_value: Selector for login button.
        Raises:
            TimeoutException: If any element in the login sequence is not found/interactable.
            WebDriverException: For other browser/navigation issues.
            RuntimeError: If WebDriver is not initialized.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot perform login.")
        
        self.open_url(login_url)
        self.type_into_element(email_field_by, email_field_value, username, press_enter_after=press_enter_on_username)

        if not press_enter_on_username: # Only try to type password and click button if not submitting via Enter on username
            if password:
                print(f"Attempting to set password for field {password_field_by}='{password_field_value}'.")
                # Using set_value_with_javascript for password as per previous state
                self.set_value_with_javascript(password_field_by, password_field_value, password)
            else:
                print("No password provided, skipping password entry.")
            
            print("Attempting to click login button.")
            self.click_element(login_button_by, login_button_value)
        else:
            print("Form submission attempted via 'Enter' key on username field. Skipping password and button click.")
        
        # For scripted tests, it's better to verify the outcome (e.g., URL change, element visibility)
        # explicitly in the test script after calling login(), rather than waiting here.
        # Example explicit wait that could be in a test:
        # WebDriverWait(controller.driver, 10).until(EC.url_changes(login_url))

    def close_browser(self) -> None:
        """Quits the WebDriver and closes all associated browser windows."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                # Log this error, but don't necessarily re-raise if cleanup is best-effort
                # print(f"Error during browser quit: {e}")
                pass # Allow script to continue if browser quit fails for some reason
            finally:
                self.driver = None # Ensure driver is marked as None
        # If driver was already None, do nothing.
    
    def wait_for_url_change(self, current_url_or_substring: str, timeout: int = 10) -> bool:
        """
        Waits for the URL to change from the given URL or to no longer contain a substring.
        Args:
            current_url_or_substring: The current full URL to change from, or a substring
                                      that the new URL should not contain.
            timeout: Maximum time (in seconds) to wait.
        Returns:
            True if the URL changed, False if a timeout occurred.
        Raises:
            RuntimeError: If WebDriver is not initialized.
            TimeoutException: If URL does not change within timeout.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot wait for URL change.")
        
        # Check if it's a full URL or a substring to avoid
        if "://" in current_url_or_substring: # Heuristic for full URL
            return WebDriverWait(self.driver, timeout).until(EC.url_changes(current_url_or_substring))
        else: # Assume it's a substring that the new URL should not contain
            return WebDriverWait(self.driver, timeout).until_not(EC.url_contains(current_url_or_substring))

    def check_element_exists(self, by: str, value: str, timeout: int = 2) -> bool:
        """
        Checks if an element exists and is visible without throwing an exception on failure.
        Args:
            by: The Selenium By strategy or its string equivalent.
            value: The selector value.
            timeout: Maximum time (in seconds) to wait for the element.
        Returns:
            True if the element is found and visible, False otherwise.
        Raises:
            RuntimeError: If WebDriver is not initialized.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot check element existence.")
        try:
            self.find_element(by, value, timeout=timeout)
            return True
        except TimeoutException:
            return False

    # Example of a method to get an attribute, useful for checks
    def get_element_attribute(self, by: str, value: str, attribute_name: str, timeout: int = 10) -> str | None:
        """
        Finds an element and returns the value of a given attribute.
        Args:
            by: The Selenium By strategy or its string equivalent.
            value: The selector value.
            attribute_name: The name of the attribute to get (e.g., 'href', 'class').
            timeout: Maximum time to wait for the element.
        Returns:
            The attribute's value, or None if the attribute is not found.
        Raises:
            TimeoutException: If the element is not found within timeout.
        """
        element = self.find_element(by, value, timeout)
        return element.get_attribute(attribute_name)

    # New method to set value using JavaScript
    def set_value_with_javascript(self, by, value, text_to_set, timeout: int = 10) -> bool:
        """Sets the value of an input field using JavaScript."""
        if not self.driver:
            raise RuntimeError("WebDriver not initialized. Cannot set value with JS.")
        try:
            element = self.find_element(by, value, timeout=timeout) # Use specified timeout
            self.driver.execute_script("arguments[0].value = arguments[1];", element, text_to_set)
            # Optionally, trigger input/change events if needed by the application
            # self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
            # self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
            print(f"Attempted to set value for element found by {by}='{value}' using JavaScript.")
            return True # Indicate JS execution was attempted
        except TimeoutException:
            print(f"JS Set Value: Element not found by {by}='{value}'.")
            raise # Re-raise TimeoutException so login method knows element wasn't found
        except JavascriptException as e:
            print(f"JavaScript error while setting value for {by}='{value}': {e}")
            # Re-raise as a runtime error to ensure test failure
            raise RuntimeError(f"JavaScript execution failed for {by}='{value}': {e}") from e
