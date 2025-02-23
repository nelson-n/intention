"""
Intention Framework
A framework for template-based content generation using language models.
"""

from .core.client import IntentionClient
from .core.template import Template, template, TemplateRegistry
from .core.types import ProviderType, ProcessingMode
from .exceptions import IntentionError, ValidationError, ProviderError

__version__ = "0.1.0"
__all__ = [
    "IntentionClient",
    "Template",
    "template",
    "TemplateRegistry",
    "ProviderType",
    "ProcessingMode",
    "IntentionError",
    "ValidationError",
    "ProviderError"
]
