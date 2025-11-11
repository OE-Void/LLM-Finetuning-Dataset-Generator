import requests
from Config.config import BOLD_BRIGHT_RED, RESET

class Nvidia:
    """
    A class to interact with the Nvidia API.

    Attributes:
        AVAILABLE_MODELS (list): List of available models for chat completions.
    Methods:
        generate(prompt): Sends a prompt to the Nvidia API and returns the generated response.
    """
    AVAILABLE_MODELS = [
        "meta/llama3-70b-instruct",
    ]
 
    def __init__(
        self,
        api_key:str,
        max_tokens: int = 4096,
        timeout: int = 30,
        model: str = "meta/llama3-70b-instruct",
        temperature: float = 0.75,
        top_p: float = 0.9,
        system_prompt: str = "You are a helpful assistant.",
    ):
        """Initializes the Nvidia API client.
        Parameters:
            - api_key (str): The API key for authentication.
            - max_tokens (int): Maximum number of tokens in the response.
            - timeout (int): Timeout for API requests in seconds.
            - model (str): Model to use for chat completions.
            - temperature (float): Sampling temperature for response generation.
            - top_p (float): Nucleus sampling parameter.
            - system_prompt (str): System prompt to guide the model's behavior.
        """
        if not api_key:
            raise ValueError("Please provide the API Key to use this provider.")
        
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Invalid model: {model}. Choose from: {self.AVAILABLE_MODELS}")

        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.top_p = top_p
        self.model = model

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    def generate(
        self,
        prompt: str,
    ) -> str:
        """Generates a response from the Nvidia API based on the provided prompt.
        Parameters:
            - prompt (str): The user prompt to send to the model.
        Returns:
            - str: The generated response from the model.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt.strip()}
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, data=payload)
            response.raise_for_status() # Check for HTTP errors
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"{BOLD_BRIGHT_RED}❌ Error while generating output: {e}{RESET}")
            return ""

if __name__ == "__main__":
    ai = Nvidia(api_key="nvapi-AOxxxx")
    response = ai.generate("what is Thermodynamics?")
    print(f"Response: {response}")