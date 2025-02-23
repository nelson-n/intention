"""
Client interface for the intention framework.
Provides the main entry point for applications to interact with the framework,
managing provider connections and template processing operations.
"""

from typing import Dict, Any, Optional, Type
from ..providers.base import BaseProvider
from ..providers.openai import OpenAIProvider
from ..providers.perplexity import PerplexityProvider
from ..processors.input import InputProcessor
from ..processors.output import OutputProcessor
from ..core.types import ProviderType, ProcessorConfig
from ..exceptions import ConfigurationError, ValidationError

class IntentionClient:
    """Main client class for the intention framework"""
    
    _provider_map = {
        ProviderType.OPENAI: OpenAIProvider,
        ProviderType.PERPLEXITY: PerplexityProvider
    }
    
    def __init__(
        self,
        provider: str,
        api_key: str,
        processor_config: Optional[ProcessorConfig] = None,
        **provider_kwargs
    ):
        """
        Initialize the client with a provider and configuration.
        
        Args:
            provider: Provider type (e.g., "openai", "perplexity")
            api_key: Provider API key
            processor_config: Optional configuration for processors
            **provider_kwargs: Additional provider-specific configuration
        """
        self.provider = self._initialize_provider(provider, api_key, **provider_kwargs)
        self.input_processor = InputProcessor(processor_config)
        self.output_processor = OutputProcessor(processor_config)
        
    def _initialize_provider(
        self,
        provider_type: str,
        api_key: str,
        **kwargs
    ) -> BaseProvider:
        """
        Initialize the specified provider.
        
        Args:
            provider_type: Type of provider to initialize
            api_key: Provider API key
            **kwargs: Additional provider configuration
            
        Returns:
            BaseProvider: Initialized provider instance
            
        Raises:
            ConfigurationError: If provider type is invalid
        """
        provider_class = self._provider_map.get(provider_type)
        if not provider_class:
            raise ConfigurationError(f"Unsupported provider type: {provider_type}")
            
        return provider_class(api_key=api_key, **kwargs)
        
    async def process(
        self,
        template_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process data through a template and return formatted results.
        
        Args:
            template_name: Name of the template to use
            data: Input data to process
            
        Returns:
            dict: Processed and formatted output
            
        Raises:
            ValidationError: If input/output validation fails
            ProviderError: If provider interaction fails
        """
        from .template import TemplateRegistry
        
        # Get template
        template = TemplateRegistry.get(template_name)
        
        # Validate and process input
        self.input_processor.validate(data, template.input_schema)
        processed_input = self.input_processor.process(data)
        
        # Format prompt using template
        prompt = template.format_prompt(processed_input)
        
        # Get response from provider
        response = await self.provider.complete(prompt)
        
        # Validate and format output
        self.output_processor.validate(response["raw_response"], template.output_schema)
        formatted_output = template.format_output(response["raw_response"])
        
        # Enrich output with metadata
        enriched_output = self.output_processor.enrich_output(
            formatted_output,
            context={
                "template": template_name,
                "provider": self.provider.__class__.__name__,
                "input": processed_input
            }
        )
        
        return enriched_output
        
    async def validate_setup(self) -> bool:
        """
        Validate client setup including provider connection.
        
        Returns:
            bool: True if setup is valid
            
        Raises:
            ConfigurationError: If setup validation fails
        """
        # Validate provider connection
        if not await self.provider.validate_connection():
            raise ConfigurationError("Failed to validate provider connection")
            
        return True
