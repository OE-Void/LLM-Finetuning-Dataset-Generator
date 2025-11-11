from Config.config import generate_dynamic_headers, BOLD_BRIGHT_RED, BOLD_BRIGHT_GREEN, BOLD_BRIGHT_CYAN, RESET
import requests
from typing import Optional

class DeepInfra:
    """Client for interacting with the DeepInfra Chat Completions API.

    This client supports non-streaming chat completions. It reuses a single
    HTTP session for efficiency and allows configuration of model, decoding
    parameters, and timeouts.

    Attributes:
        AVAILABLE_MODELS (list): List of available models for chat completions.
    Methods:
        generate(prompt): Generate a chat completion for the given prompt.
    """
    AVAILABLE_MODELS = [
        "deepseek-ai/DeepSeek-R1-0528",
        "deepseek-ai/DeepSeek-R1",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "deepseek-ai/DeepSeek-R1-Turbo",
        "deepseek-ai/DeepSeek-V3",
        "deepseek-ai/DeepSeek-Prover-V2-671B",
        "google/gemma-2-27b-it",
        "google/gemma-2-9b-it",
        "google/gemma-3-12b-it",
        "google/gemma-3-27b-it",
        "google/gemma-3-4b-it",
        "meta-llama/Llama-3.3-70B-Instruct",
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "meta-llama/Llama-4-Scout-17B-16E-Instruct",
        "meta-llama/Llama-Guard-4-12B",
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "microsoft/Phi-4-multimodal-instruct",
        "microsoft/WizardLM-2-8x22B",
        "microsoft/phi-4",
        "microsoft/phi-4-reasoning-plus",
        "mistralai/Mistral-Small-24B-Instruct-2501",
        "nvidia/Llama-3.1-Nemotron-70B-Instruct",
        "Qwen/QwQ-32B",
        "Qwen/Qwen2.5-72B-Instruct",
        "Qwen/Qwen2.5-Coder-32B-Instruct",
        "Qwen/Qwen3-14B",
        "Qwen/Qwen3-30B-A3B",
        "Qwen/Qwen3-32B",
        "Qwen/Qwen3-235B-A22B",
    ]
 
    def __init__(
        self,
        api_key: Optional[str] = None,
        max_tokens: int = 2048,
        timeout: int = 30,
        model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        temperature: float = 0.75,
        top_p: float = 0.9,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        """Initialize the DeepInfra client.

        Args:
            api_key: Optional API key. If not provided, dynamic headers are used.
            max_tokens: Maximum number of tokens to generate in the response.
            timeout: Request timeout in seconds.
            model: Model identifier from AVAILABLE_MODELS.
            temperature: Sampling temperature for generation.
            top_p: Nucleus sampling parameter.
            system_prompt: System role prompt to steer behavior.
        """

        # Configure authentication headers: prefer explicit API key; otherwise fall back
        # to dynamic headers sourced from the environment/config.
        if api_key:
            print(f"{BOLD_BRIGHT_GREEN}Initialized the DeepInfra API Client using API Key.{RESET}")
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
        else:
            print(f"{BOLD_BRIGHT_GREEN}Initialized the DeepInfra API Client without API Key.{RESET}")
            self.headers = generate_dynamic_headers()

        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Invalid model: {model}. Choose from: {self.AVAILABLE_MODELS}")

        self.api_url = "https://api.deepinfra.com/v1/openai/chat/completions"

        # Core generation parameters
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.top_p = top_p
        self.model = model

        # Reuse an HTTP session for connection pooling and lower latency.
        self.session = requests.Session()

    def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate a non-streaming chat completion.

        Args:
            prompt: The user prompt content.

        Returns:
            The assistant message content on success; empty string on error.
        """

        if not prompt or not prompt.strip():
            return ""

        # Build request payload according to OpenAI-compatible schema
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt.strip()},
            ],
            "stream": False,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

        try:
            response = self.session.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            # Safely extract content; fall back to empty string if not present
            choices = data.get("choices") or []
            if not choices:
                return ""
            message = choices[0].get("message") or {}
            return message.get("content", "") or ""
        except requests.exceptions.HTTPError as http_err:
            # Include server response text if available for easier debugging
            err_text = getattr(http_err.response, "text", "") if hasattr(http_err, "response") else ""
            print(f"{BOLD_BRIGHT_RED}❌ HTTP error: {http_err} {err_text}{RESET}")
            return ""
        except requests.exceptions.RequestException as req_err:
            print(f"{BOLD_BRIGHT_RED}❌ Request error: {req_err}{RESET}")
            return ""
        except Exception as err:
            print(f"{BOLD_BRIGHT_RED}❌ Unexpected error: {err}{RESET}")
            return ""

if __name__ == "__main__":
    ai = DeepInfra()
    response = ai.generate("what is Thermodynamics?")
    print(f"Response: {response}")