"""
Type definitions and custom types used throughout the intention framework.
This module defines the core type system and type hints that ensure
type safety and proper interface definitions across the codebase.
"""

from typing import TypedDict, Optional, Dict, Any, List, Union

class ProviderConfig(TypedDict):
    """Configuration for LLM providers"""
    api_key: str
    base_url: Optional[str]
    model: Optional[str]
    temperature: Optional[float]
    max_tokens: Optional[int]
    additional_params: Optional[Dict[str, Any]]

class IntentionResponse(TypedDict):
    """Structured response from LLM providers"""
    raw_response: str
    formatted_response: Dict[str, Any]
    metadata: Dict[str, Any]

class TemplateSchema(TypedDict):
    """Schema definition for templates"""
    name: str
    description: Optional[str]
    version: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    metadata: Optional[Dict[str, Any]]

class ProcessorConfig(TypedDict):
    """Configuration for input/output processors"""
    validate_schema: bool
    strict_mode: bool
    custom_validators: Optional[List[str]]
    error_handling: str  # 'strict' | 'lenient' | 'ignore'

# Type aliases for common types
JsonType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
SchemaType = Dict[str, Union[type, Dict[str, Any]]]
ValidationResult = Dict[str, Union[bool, List[str]]]

# Enums as string literals (for better JSON serialization)
class ProcessingMode:
    """Processing modes for the framework"""
    STRICT = "strict"
    LENIENT = "lenient"
    IGNORE = "ignore"

class ProviderType:
    """Supported LLM provider types"""
    OPENAI = "openai"
    PERPLEXITY = "perplexity"
    # Add other providers as needed
