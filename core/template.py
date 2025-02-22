"""
Core template processing functionality for the intention framework.
This module handles the creation, validation, and processing of templates,
which are the fundamental building blocks for generating structured content.
It includes the Template class and related helper functions.
"""

from typing import Any, Dict, Optional, Type
from dataclasses import dataclass
from ..exceptions import ValidationError

@dataclass
class TemplateMetadata:
    """Metadata for template registration and management"""
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    tags: list[str] = None

class Template:
    """Base template class for defining input/output schemas and prompt formatting"""
    
    # Class-level attributes for schema definition
    input_schema: Dict[str, Type] = {}
    output_schema: Dict[str, Type] = {}
    metadata: TemplateMetadata = None
    
    def __init__(self, name: str, description: Optional[str] = None):
        """Initialize template with name and optional description"""
        self.metadata = TemplateMetadata(
            name=name,
            description=description
        )
        self._validate_schemas()
    
    def _validate_schemas(self) -> None:
        """Validate that required schemas are defined"""
        if not self.input_schema:
            raise ValidationError("Input schema must be defined")
        if not self.output_schema:
            raise ValidationError("Output schema must be defined")
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data against input_schema
        
        Args:
            data: Dictionary of input data
            
        Returns:
            bool: True if valid, raises ValidationError if invalid
        """
        for field, field_type in self.input_schema.items():
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
            if not isinstance(data[field], field_type):
                raise ValidationError(
                    f"Invalid type for {field}. Expected {field_type}, got {type(data[field])}"
                )
        return True
    
    def validate_output(self, data: Dict[str, Any]) -> bool:
        """
        Validate output data against output_schema
        
        Args:
            data: Dictionary of output data
            
        Returns:
            bool: True if valid, raises ValidationError if invalid
        """
        for field, field_type in self.output_schema.items():
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
            if not isinstance(data[field], field_type):
                raise ValidationError(
                    f"Invalid type for {field}. Expected {field_type}, got {type(data[field])}"
                )
        return True
    
    def format_prompt(self, data: Dict[str, Any]) -> str:
        """
        Convert input data to LLM prompt
        
        Args:
            data: Dictionary of input data
            
        Returns:
            str: Formatted prompt
            
        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement format_prompt")
    
    def format_output(self, response: str) -> Dict[str, Any]:
        """
        Convert LLM response to structured output
        
        Args:
            response: Raw LLM response
            
        Returns:
            dict: Structured output data
            
        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement format_output")

# Template registry for storing and retrieving templates
class TemplateRegistry:
    """Registry for storing and retrieving templates"""
    
    _templates: Dict[str, Template] = {}
    
    @classmethod
    def register(cls, template: Template) -> None:
        """Register a template"""
        cls._templates[template.metadata.name] = template
    
    @classmethod
    def get(cls, name: str) -> Template:
        """Get a template by name"""
        if name not in cls._templates:
            raise KeyError(f"Template not found: {name}")
        return cls._templates[name]
    
    @classmethod
    def list(cls) -> list[str]:
        """List all registered templates"""
        return list(cls._templates.keys())

# Decorator for registering templates
def template(name: str, description: Optional[str] = None):
    """Decorator for registering templates"""
    def decorator(cls):
        template_instance = cls(name=name, description=description)
        TemplateRegistry.register(template_instance)
        return cls
    return decorator
