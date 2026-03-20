import os
import yaml
from pathlib import Path

import ollama
from google import genai
from groq import Groq


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "model.yaml"


class LLMClient:
    """
    Unified LLM interface.

    Supports:
    - Local models (Ollama)
    - Gemini API
    - Groq API

    Provider selected via config/model.yaml
    """

    def __init__(self):

        if not CONFIG_PATH.exists():
            raise RuntimeError("model.yaml not found inside config")

        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)

        self.provider = config.get("provider")
        self.model_name = config.get("model_name")
        self.api_key_env = config.get("api_key_env")

        if not self.provider:
            raise RuntimeError("provider missing in model.yaml")

        self._initialize_provider()

    # ---------------------------
    # Provider Initialization
    # ---------------------------

    def _initialize_provider(self):

        if self.provider == "gemini":

            api_key = os.getenv(self.api_key_env)

            if not api_key:
                raise RuntimeError("Gemini API key missing")

            self.client = genai.Client(api_key=api_key)

        elif self.provider == "groq":

            api_key = os.getenv(self.api_key_env)

            if not api_key:
                raise RuntimeError("Groq API key missing")

            self.client = Groq(api_key=api_key)

        elif self.provider == "local":

            # Ollama requires no API key
            self.client = None

        else:
            raise ValueError("Unsupported provider")

    # ---------------------------
    # Generate Response
    # ---------------------------

    def generate(self, prompt: str) -> str:

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:

            if self.provider == "local":

                response = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                return response["message"]["content"]

            elif self.provider == "gemini":

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

                return response.text

            elif self.provider == "groq":

                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )

                return completion.choices[0].message.content

        except Exception as e:

            raise RuntimeError(f"LLM generation failed: {e}")