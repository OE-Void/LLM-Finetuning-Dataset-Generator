import os
import json
import requests
from typing import Optional
from Config.config import generate_dynamic_headers, BOLD_BRIGHT_RED, BOLD_BRIGHT_GREEN, BOLD_BRIGHT_YELLOW, BOLD_BRIGHT_CYAN, RESET

class Cerebras:
    """
    Client to interact with the Cerebras AI API for chat completions.
    Attributes:
        AVAILABLE_MODELS (list): List of available models for chat completions.
    Methods:
        refresh_api_key(): Refreshes the API key by making a request to the Cerebras API endpoint.
        generate(message, system_prompt, model, temperature, max_tokens, timeout): Sends a chat message to the model and returns the response.
    """
    AVAILABLE_MODELS = [
        "llama3.1-8b",
        "llama-3.3-70b",
        "qwen-3-32b",
        "qwen-3-235b-a22b-instruct-2507",
        "qwen-3-235b-a22b-thinking-2507",
        "gpt-oss-120b",
        "zai-glm-4.6"
    ]

    def __init__(
        self, 
        cookies_or_api_key: Optional[str],
        max_tokens: int = 2048,
        timeout: int = 30,
        model: str = "llama-3.3-70b",
        temperature: float = 0.75,
        top_p: float = 0.9,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        """Initialize the Cerebras client.
        
        Parameters:
            - cookies_or_api_key (str, optional): Cookies string or API key for authentication.
            - max_tokens (int): Maximum number of tokens in the response.
            - timeout (int): Timeout for API requests in seconds.
            - model (str): Model to use for chat completions.
            - temperature (float): Sampling temperature for response generation.
            - top_p (float): Nucleus sampling parameter.
            - system_prompt (str): System prompt to guide the model's behavior.
        """

        self.cookies_or_api_key = cookies_or_api_key
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.top_p = top_p
        self.model = model
        self.config_file_path = os.path.abspath(os.path.join("Config", "Cerebras-Config.json"))

        # --- Main initialization logic ---
        if cookies_or_api_key and cookies_or_api_key.startswith('cookieyes-consent'):
            # Priority: Cookies
            print(f"{BOLD_BRIGHT_CYAN}Initializing Cerebras client using COOKIES...{RESET}")
            try:
                if not os.path.exists(self.config_file_path):
                    # Create config file if missing
                    with open(self.config_file_path, 'w') as config_file:
                        json.dump({}, config_file)
                    print(f"{BOLD_BRIGHT_GREEN}New config file created at {self.config_file_path}\n{RESET}")
                    self.refresh_api_key()
                else:
                    # Load API key from existing config
                    with open(self.config_file_path, 'r') as f:
                        data = json.load(f)
                        self.api_key = data.get("data", {}).get("GetMyDemoApiKey")

                    # If key not found in config, refresh it
                    if not self.api_key:
                        print(f"{BOLD_BRIGHT_YELLOW}API key not found in config. Refreshing...{RESET}")
                        self.refresh_api_key()

            except (FileNotFoundError, json.JSONDecodeError, KeyError, AttributeError) as e:
                print(f"{BOLD_BRIGHT_RED}Error encountered while initializing with cookies: {e}{RESET}")
                self.refresh_api_key()

        elif cookies_or_api_key and cookies_or_api_key.startswith('csk-'):
            # Initialize with API key
            print(f"{BOLD_BRIGHT_CYAN}Initializing Cerebras client using API KEY...{RESET}")
            self.api_key = cookies_or_api_key

        else:
            # If neither cookies nor valid API key provided
            raise ValueError("Cookies or API Key must be provided to initialize the class.")

    def refresh_api_key(self) -> None:
        """
        Refreshes the API key by making a request to the Cerebras API endpoint.

        This method sends a POST request to the Cerebras API to obtain a new demo API key.
        The response is then saved to a JSON configuration file located in the user's home directory.
        If the request is successful, the new API key is stored and a success message is returned.
        In case of any errors, appropriate error messages are printed and the method retries the request.

        Returns:
            str: A message indicating the result of the API key refresh operation.
        """
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'cookie': self.cookies_or_api_key,
            'dnt': '1',
            'origin': 'https://inference.cerebras.ai',
            'priority': 'u=1, i',
            'referer': 'https://inference.cerebras.ai/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': generate_dynamic_headers()['User-Agent']
        }
        json_data = {
            'operationName': 'GetMyDemoApiKey',
            'variables': {},
            'query': 'query GetMyDemoApiKey {\n  GetMyDemoApiKey\n}',
        }
        try:
            response = requests.post('https://chat.cerebras.ai/api/graphql', headers=headers, json=json_data)
            response.raise_for_status()
            if response.status_code == 200 and response.ok:
                # Writing to a JSON file with human-readable date format
                with open(self.config_file_path, 'w') as json_file:
                    json.dump(response.json(), json_file, indent=4)
                print(f"{BOLD_BRIGHT_YELLOW}API key updated successfully!\n{RESET}")
            else:
                print(f"{BOLD_BRIGHT_RED}Unexpected response status: {response.status_code}. Please check the API endpoint or your request parameters.{RESET}")
                print("{BOLD_BRIGHT_RED}Failed to update API key due to unexpected response.\n{RESET}")
        except FileNotFoundError:
            print(f"{BOLD_BRIGHT_RED}{self.config_file_path} not found, creating a new file.{RESET}")
            with open(self.config_file_path, 'w') as json_file:
                json.dump(response.json(), json_file, indent=4)
            print(f"{BOLD_BRIGHT_YELLOW}New file created and data written successfully to {self.config_file_path}{RESET}")
            print(f"{BOLD_BRIGHT_GREEN}API key updated successfully!\n{RESET}")
        except requests.exceptions.RequestException as e:
            print(f"🔄 Demo API key refresh failed due to network error: {e}. Retrying... 🔄")
            print(self.refresh_api_key())
        except Exception as e:
            print(f"🔄 Demo API key refresh failed due to an unexpected error: {e}. Retrying... 🔄")
            print(self.refresh_api_key())
    
    def generate(self, prompt: str) -> str:
        """
        Sends a chat message to the model and returns the response.

        Parameters:
            - prompt (str): The user message to send to the model.

        Returns:
            - str: The response from the model.
        """
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.api_key}'
        }
        json_data = {
            'messages': [
                {
                    'content': self.system_prompt,
                    'role': 'system',
                },
                {
                    'content': prompt,
                    'role': 'user',
                },
            ],
            'model': self.model,
            'stream': False,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'max_completion_tokens': self.max_tokens,
        }
        try:
            response = requests.post('https://api.cerebras.ai/v1/chat/completions', headers=headers, json=json_data, timeout=None)
            response.raise_for_status()
            if response.status_code==401:
                print("🚨 Alert: Your demo API key has expired. 🕰️ Reinitializing the system To Generate New Demo Api Key... 🔄")
                print(self.refresh_api_key())
                self.__init__(self.cookies_or_api_key, self.max_tokens, self.timeout, self.model, self.temperature, self.top_p, self.system_prompt)
                return self.generate(prompt)
            if response.status_code==200 and response.ok:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"🚨 Alert: Received unexpected status code {response.status_code}. Please check the request and try again."
        except Exception as e:
            return f"🚨 An error occurred: {e}"

if __name__ == "__main__":
    ai = Cerebras('cookieyes-consent=consentid:U1xxxxx')
    response = ai.generate("what is Thermodynamics?")
    print(f"Response: {response}")

    ai = Cerebras('csk-cytxxxxx')
    response = ai.generate("what is Thermodynamics?")
    print(f"Response: {response}")