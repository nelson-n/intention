"""
Base provider interface for the intention framework.
Defines the abstract base class and common interfaces that all providers
must implement to integrate with the framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..core.types import ProviderConfig, IntentionResponse
from ..exceptions import ProviderError, AuthenticationError

class BaseProvider(ABC):
    """Base interface for LLM providers"""
    
    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the provider with authentication and configuration.
        
        Args:
            api_key: Provider API key
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.config = self._validate_config(kwargs)
        
    @abstractmethod
    async def complete(self, prompt: str) -> IntentionResponse:
        """
        Send prompt to LLM and get response.
        
        Args:
            prompt: The formatted prompt to send to the LLM
            
        Returns:
            IntentionResponse: Provider response with raw and formatted data
            
        Raises:
            ProviderError: If the request fails
            AuthenticationError: If authentication fails
        """
        raise NotImplementedError
        
    @abstractmethod
    def validate_response(self, response: IntentionResponse) -> bool:
        """
        Validate provider response format and content.
        
        Args:
            response: Response to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        raise NotImplementedError
        
    def _validate_config(self, config: Dict[str, Any]) -> ProviderConfig:
        """
        Validate provider configuration.
        
        Args:
            config: Provider configuration dictionary
            
        Returns:
            ProviderConfig: Validated configuration
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Base configuration validation
        required_fields = {"api_key"}
        for field in required_fields:
            if not getattr(self, field, None):
                raise ConfigurationError(f"Missing required configuration field: {field}")
                
        return ProviderConfig(
            api_key=self.api_key,
            base_url=config.get("base_url"),
            # Add other common config options here
        )
        
    @abstractmethod
    async def validate_connection(self) -> bool:
        """
        Validate connection to provider API.
        
        Returns:
            bool: True if connection is valid
            
        Raises:
            AuthenticationError: If authentication fails
            ProviderError: If connection test fails
        """
        raise NotImplementedError