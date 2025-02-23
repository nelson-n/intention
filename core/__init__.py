"""
Core functionality for the intention framework.
"""

from .client import IntentionClient
from .template import Template, template, TemplateRegistry
from .types import (
    ProviderConfig,
    IntentionResponse,
    TemplateSchema,
    ProcessorConfig,
    JsonType,
    SchemaType,
    ValidationResult,
    ProcessingMode,
    ProviderType
)

__all__ = [
    "IntentionClient",
    "Template",
    "template",
    "TemplateRegistry",
    "ProviderConfig",
    "IntentionResponse",
    "TemplateSchema",
    "ProcessorConfig",
    "JsonType",
    "SchemaType",
    "ValidationResult",
    "ProcessingMode",
    "ProviderType"
]
