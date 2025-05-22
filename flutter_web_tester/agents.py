import autogen
from .browser_controller import BrowserController
from selenium.webdriver.common.by import By # Required for function annotations and type hints

# Instantiate the BrowserController globally.
# TestManagerAgent will use this instance to register its methods.
browser_instance = BrowserController()

# Define the SeleniumAgent - Now an intelligent assistant proposing function calls
selenium_agent = autogen.AssistantAgent(
    name="SeleniumExpert", # Changed name for clarity of its new role
    system_message="You are a helpful assistant that helps the TestManager to control a web browser. Based on the TestManager's request, identify the appropriate browser control function and parameters, then instruct the TestManager to call it. Only suggest functions that are available to the TestManager. Ensure you provide all necessary parameters for the functions, including selectors and values.",
    # llm_config will be provided from main.py, as it uses the shared config_list
)

# Define the TestManagerAgent - Executes functions based on SeleniumExpert's proposals
test_manager_agent = autogen.UserProxyAgent(
    name="TestManager",
    system_message="I am a Test Manager. I will receive instructions from the SeleniumExpert on which browser functions to call. I will execute these functions using my available tools and report the results back. I can execute code and call predefined functions. I will wait for the SeleniumExpert to tell me what to do next.",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding", "use_docker": False}, # Confirmed
)

# Register functions for TestManagerAgent to execute
# These are the tools TestManagerAgent can use when SeleniumExpert suggests their use.
test_manager_agent.register_function(
    function_map={
        "login_to_website": browser_instance.login,
        "get_page_title": browser_instance.get_title,
        "get_page_current_url": browser_instance.get_current_url,
        "open_web_url": browser_instance.open_url, # Retaining for flexibility, though login handles it
        "click_web_element": browser_instance.click_element,
        "type_into_web_element": browser_instance.type_into_element,
        "close_the_browser": browser_instance.close_browser,
    }
)

# Helper function to access the browser instance for cleanup from main.py
def get_browser_instance():
    return browser_instance
