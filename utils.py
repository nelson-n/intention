"""
Utility functions used throughout the intention framework.
Contains helper functions for common operations and shared functionality.
"""

import json
from typing import Any, Dict, Optional, Union, Type, get_args, get_origin
from .exceptions import ValidationError

def validate_json(data: str) -> bool:
    """
    Validate if a string is valid JSON.
    
    Args:
        data: String to validate as JSON
        
    Returns:
        bool: True if valid JSON, False otherwise
    """
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False

def format_json(data: str) -> Dict[str, Any]:
    """
    Format and validate JSON string to dictionary.
    
    Args:
        data: JSON string to format
        
    Returns:
        dict: Parsed JSON data
        
    Raises:
        ValidationError: If JSON is invalid
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON format: {str(e)}")

def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate that a dictionary matches a given schema.
    
    Args:
        data: Dictionary to validate
        schema: Schema to validate against
        
    Returns:
        bool: True if valid, False otherwise
    """
    def is_valid_type(value: Any, expected_type: Any) -> bool:
        # Handle Union types (e.g., Optional)
        if get_origin(expected_type) is Union:
            return any(is_valid_type(value, t) for t in get_args(expected_type))
            
        # Handle Dict types
        if get_origin(expected_type) is dict:
            return isinstance(value, dict)
            
        # Handle basic types
        if isinstance(expected_type, type):
            return isinstance(value, expected_type)
            
        # Handle nested dictionaries
        if isinstance(expected_type, dict):
            if not isinstance(value, dict):
                return False
            return all(
                k in value and is_valid_type(value[k], v)
                for k, v in expected_type.items()
            )
            
        return False

    try:
        for field, field_type in schema.items():
            if field not in data:
                return False
            if not is_valid_type(data[field], field_type):
                return False
        return True
    except Exception:
        return False

def format_error_message(error: Exception, context: Optional[str] = None) -> str:
    """
    Format error message with optional context.
    
    Args:
        error: Exception to format
        context: Optional context to add to message
        
    Returns:
        str: Formatted error message
    """
    message = str(error)
    if context:
        message = f"{context}: {message}"
    return message
