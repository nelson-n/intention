"""
OpenAI provider implementation for the intention framework.
Implements the provider interface for OpenAI's language models,
handling API communication and response processing.
"""

import json
from typing import Optional, Dict, Any
import aiohttp
from .base import BaseProvider
from ..core.types import IntentionResponse
from ..exceptions import (
    ProviderError,
    AuthenticationError,
    RateLimitError,
    ResponseFormatError
)

class OpenAIProvider(BaseProvider):
    """OpenAI-specific implementation"""
    
    API_BASE = "https://api.openai.com/v1"
    DEFAULT_MODEL = "gpt-4-turbo-preview"
    
    def __init__(
        self,
        api_key: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (defaults to gpt-4-turbo-preview)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, **kwargs)
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    async def complete(self, prompt: str) -> IntentionResponse:
        """
        Send prompt to OpenAI API and get response.
        
        Args:
            prompt: The formatted prompt to send
            
        Returns:
            IntentionResponse: Provider response with raw and formatted data
            
        Raises:
            ProviderError: If the request fails
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that provides accurate, structured information."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.API_BASE}/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError("Invalid API key")
                    elif response.status == 429:
                        raise RateLimitError("Rate limit exceeded")
                    elif response.status != 200:
                        raise ProviderError(f"API request failed with status {response.status}")
                    
                    result = await response.json()
                    
                    if not result.get("choices"):
                        raise ResponseFormatError("No choices in response")
                    
                    raw_response = result["choices"][0]["message"]["content"]
                    
                    return IntentionResponse(
                        raw_response=raw_response,
                        formatted_response=json.loads(raw_response),
                        metadata={
                            "model": self.model,
                            "usage": result.get("usage", {}),
                            "finish_reason": result["choices"][0].get("finish_reason")
                        }
                    )
                    
        except aiohttp.ClientError as e:
            raise ProviderError(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ResponseFormatError(f"Invalid JSON in response: {str(e)}")
            
    def validate_response(self, response: IntentionResponse) -> bool:
        """
        Validate OpenAI response format and content.
        
        Args:
            response: Response to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not response.raw_response or not response.formatted_response:
            return False
            
        if not isinstance(response.formatted_response, dict):
            return False
            
        if not response.metadata.get("model"):
            return False
            
        return True
        
    async def validate_connection(self) -> bool:
        """
        Validate connection to OpenAI API.
        
        Returns:
            bool: True if connection is valid
            
        Raises:
            AuthenticationError: If authentication fails
            ProviderError: If connection test fails
        """
        try:
            # Simple model list request to validate API access
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.API_BASE}/models",
                    headers=headers
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError("Invalid API key")
                    elif response.status != 200:
                        raise ProviderError(f"API request failed with status {response.status}")
                    return True
                    
        except aiohttp.ClientError as e:
            raise ProviderError(f"Network error: {str(e)}")
            
        return False