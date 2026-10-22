import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "codellama"  # أو llama3 حسب المتوفر محلياً لديك

class LocalCodeAgent:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name

    def _call_ollama(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json().get("response", "No response generated.")
            else:
                return f"Error from Ollama: {response.text}"
        except Exception as e:
            return f"Connection error with Ollama (Ensure it is running locally): {str(e)}"

    def review_code(self, code: str) -> dict:
        prompt = f"""
You are an expert Autonomous Code Review Agent. Analyze the following source code for bugs, security vulnerabilities, and code smells. 
Provide a clean JSON-like structured response or clear sections containing:
1. Code Quality Score (out of 10)
2. Issues Found
3. Suggested Improvements

Source Code:
```python
{code}