import autogen
# Ensure the correct agent names are imported from agents.py
from flutter_web_tester.agents import test_manager_agent, selenium_agent as selenium_expert_agent, get_browser_instance
# selenium_agent from agents.py is the AssistantAgent, now named SeleniumExpert internally.
# For clarity in main.py, let's use selenium_expert_agent.

# For placeholder config_list
# import os 

def main():
    # 1. Set up Autogen config for Ollama with api_type="openai"
    config_list = [
        {
            "model": "llama3.2",  # Model name provided by the user
            "base_url": "http://localhost:11434/v1",  # Standard Ollama API base URL
            "api_type": "openai",  # Use "openai" for Ollama's OpenAI-compatible endpoint
            "api_key": "ollama",    # Or "NULL", "None" - usually a dummy string for local
        }
    ]
    
    # 2. Ensure agents have their necessary configurations
    # TestManagerAgent (UserProxyAgent)
    test_manager_agent.llm_config = {
        "config_list": config_list,
    }
    
    # SeleniumExpertAgent (AssistantAgent)
    selenium_expert_agent.llm_config = {
        "config_list": config_list,
        "functions": test_manager_agent.function_map # Expose TestManager's functions to SeleniumExpert
    }

    # TestManagerAgent's code_execution_config is already set in agents.py.
    # test_manager_agent.code_execution_config = {"work_dir": "coding", "use_docker": False}

    # 3. Define the revised higher-level task message for TC1.1
    tc1_1_message = (
        "Execute Test Case TC1.1: Successful Login to 'https://testsk.unilabs.pro/' "
        "with username 'admin@unilabs.sk' and password 'malina'.\n"
        "The necessary XPaths are: email_field='//input[@type=\\'email\\']', "
        "password_field='//input[@type=\\'password\\']', "
        "login_button='//button[@type=\\'submit\\'] | //button[contains(.,\\'Login\\')] | //button[contains(.,\\'Sign in\\')]."
        "After the login attempt, please report the page title and current URL. Then, close the browser."
    )
    
    browser_controller_instance = get_browser_instance()

    try:
        # 4. Initiate the chat
        print(f"Initiating chat for Test Case TC1.1 (using Ollama model: {config_list[0]['model']} with api_type: {config_list[0]['api_type']})...")
        chat_result = test_manager_agent.initiate_chat(
            recipient=selenium_expert_agent, 
            message=tc1_1_message,
        )
        
        print("\nAgent chat finished for TC1.1.")
        
        if chat_result and chat_result.chat_history:
            print("\nLast message from the chat:")
            # Iterate backwards to find the last message from TestManager, which should summarize the findings.
            for i in range(len(chat_result.chat_history) - 1, -1, -1):
                msg = chat_result.chat_history[i]
                if msg['role'] == 'user' and msg.get('name') == test_manager_agent.name:
                    print(msg['content'])
                    break
            else: # If no message from TestManager found (should not happen in successful flow)
                print(chat_result.chat_history[-1]['content'])


        # print("\nFull conversation history:") # Uncomment for detailed debugging
        # for msg_idx, msg in enumerate(chat_result.chat_history):
        #     print(f"\n--- Message {msg_idx} ---")
        #     print(f"Role: {msg.get('role')}")
        #     print(f"Name: {msg.get('name')}")
        #     print(f"Content: {msg.get('content')}")
        #     if msg.get('tool_calls'):
        #         print(f"Tool Calls: {msg.get('tool_calls')}")


    except Exception as e:
        print(f"An error occurred during the agent interaction for TC1.1: {e}")

    finally:
        print("Ensuring browser is closed (main.py finally block)...")
        if browser_controller_instance and browser_controller_instance.driver:
            status = browser_controller_instance.close_browser()
            print(status)
        else:
            print("Browser was already closed or not initialized.")

if __name__ == "__main__":
    main()
