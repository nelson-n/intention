"""
Type definitions and custom types used throughout the intention framework.
This module defines the core type system and type hints that ensure
type safety and proper interface definitions across the codebase.
"""
from typing import TypedDict, Optional

class ProviderConfig(TypedDict):
    api_key: str
    base_url: Optional[str]
    # Other provider settings

class IntentionResponse(TypedDict):
    raw_response: str
    formatted_response: dict
    metadata: dict
