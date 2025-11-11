import requests 
from typing import Union, Any, Generator
from Config.config import BOLD_BRIGHT_RED, RESET

class Sambanova:
    """
    A class to interact with the Sambanova API.
    Attributes:
        AVAILABLE_MODELS (list): List of available models for chat completions.
    Methods:
        generate(prompt): Sends a prompt to the Sambanova API and returns the generated response.
    """
    AVAILABLE_MODELS = [
        "Meta-Llama-3.1-8B-Instruct",
        "Meta-Llama-3.1-70B-Instruct",
        "Meta-Llama-3.1-405B-Instruct",
        "DeepSeek-R1-Distill-Llama-70B",
        "Llama-3.1-Tulu-3-405B",
        "Meta-Llama-3.2-1B-Instruct",
        "Meta-Llama-3.2-3B-Instruct",
        "Meta-Llama-3.3-70B-Instruct",
        "Qwen2.5-72B-Instruct",
        "Qwen2.5-Coder-32B-Instruct",
        "QwQ-32B-Preview"
    ]

    def __init__(
        self,
        api_key: str,
        max_tokens: int = 4096,
        timeout: int = 30,
        model: str = "Meta-Llama-3.3-70B-Instruct",
        temperature: float = 0.75,
        top_p: float = 0.9,
        system_prompt: str = "You are a helpful AI assistant.",
    ):
        """
        Initializes the Sambanova API with given parameters.
        Parameters:
            - api_key (str): The API key for authentication.
            - max_tokens (int): Maximum number of tokens in the response.
            - timeout (int): Timeout for API requests in seconds.
            - model (str): Model to use for chat completions.
            - temperature (float): Sampling temperature for response generation.
            - top_p (float): Nucleus sampling parameter.
            - system_prompt (str): System prompt to guide the model's behavior.
        """
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Invalid model: {model}. Choose from: {self.AVAILABLE_MODELS}")

        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.top_p = top_p

        # Configure the API base URL and headers
        self.base_url = "https://api.sambanova.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def generate(
        self,
        prompt: str,
    ) -> Union[Any, Generator[Any, None, None]]:
        """Chat with AI using the Sambanova API.
        Parameters:
            - prompt (str): The user prompt to send to the model.
        Returns:
            - str: The generated response from the model.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status() # Check for HTTP errors
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"{BOLD_BRIGHT_RED}❌ Error while generating output: {e}{RESET}")
            return ""

if __name__ == "__main__":
    ai = Sambanova(api_key='49exxxx')
    response = ai.generate("what is Thermodynamics?")
    print(f"Response: {response}")