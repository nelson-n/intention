"""
Perplexity provider implementation for the intention framework.
Implements the provider interface for Perplexity's language models.
"""

import json
from typing import Optional, Dict, Any, cast
import aiohttp
from .base import BaseProvider
from ..core.types import IntentionResponse
from ..exceptions import (
    ProviderError,
    AuthenticationError,
    RateLimitError,
    ResponseFormatError
)

class PerplexityProvider(BaseProvider):
    """Perplexity-specific implementation"""
    
    API_BASE = "https://api.perplexity.ai"
    DEFAULT_MODEL = "sonar"
    
    def __init__(
        self,
        api_key: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """Initialize Perplexity provider."""
        super().__init__(api_key, **kwargs)
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    async def complete(self, prompt: str) -> IntentionResponse:
        """Send prompt to Perplexity API and get response"""
        # Print the prompt being sent to the LLM
        print("\nSending prompt to LLM:")
        print("=" * 50)
        print(prompt)
        print("=" * 50)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Format for Perplexity API
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides accurate, structured information in JSON format. Always ensure your responses are valid JSON objects."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.API_BASE}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError("Invalid API key")
                    elif response.status == 429:
                        raise RateLimitError("Rate limit exceeded")
                    elif response.status != 200:
                        response_text = await response.text()
                        raise ProviderError(f"API request failed with status {response.status}: {response_text}")
                    
                    result = await response.json()
                    
                    if not result.get("choices"):
                        raise ResponseFormatError("No choices in response")
                    
                    raw_response = result["choices"][0]["message"]["content"]
                    
                    # Print raw response for debugging
                    print("\nRaw response from LLM:")
                    print("=" * 50)
                    print(raw_response)
                    print("=" * 50)
                    
                    # Ensure the response is valid JSON
                    try:
                        formatted_response = json.loads(raw_response)
                    except json.JSONDecodeError:
                        # If the response isn't valid JSON, try to extract JSON from it
                        import re
                        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
                        if json_match:
                            raw_response = json_match.group(0)
                            formatted_response = json.loads(raw_response)
                        else:
                            raise ResponseFormatError("Could not parse JSON from response")
                    
                    # Create a proper IntentionResponse dictionary
                    response_dict = {
                        "raw_response": raw_response,
                        "formatted_response": formatted_response,
                        "metadata": {
                            "model": self.model,
                            "usage": result.get("usage", {}),
                            "finish_reason": result["choices"][0].get("finish_reason")
                        }
                    }
                    
                    return cast(IntentionResponse, response_dict)
                    
        except aiohttp.ClientError as e:
            raise ProviderError(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ResponseFormatError(f"Invalid JSON in response: {str(e)}")
            
    def validate_response(self, response: IntentionResponse) -> bool:
        """Validate Perplexity response format and content"""
        if "raw_response" not in response or "formatted_response" not in response:
            return False
            
        if not isinstance(response["formatted_response"], dict):
            return False
            
        if "metadata" not in response or "model" not in response["metadata"]:
            return False
            
        return True
        
    async def validate_connection(self) -> bool:
        """Validate connection to Perplexity API"""
        try:
            # For Perplexity, we'll just try a simple completion as they don't have a models endpoint
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            test_data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "test"
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.API_BASE}/chat/completions",
                    headers=headers,
                    json=test_data
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError("Invalid API key")
                    elif response.status != 200:
                        raise ProviderError(f"API request failed with status {response.status}")
                    return True
                    
        except aiohttp.ClientError as e:
            raise ProviderError(f"Network error: {str(e)}")
            
        return False 