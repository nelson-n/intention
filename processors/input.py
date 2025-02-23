"""
Input processing functionality for the intention framework.
Handles the preprocessing and validation of input data before it's
passed to the template processing system.
"""

from typing import Dict, Any, Optional, List
from ..core.types import ProcessorConfig, ValidationResult, ProcessingMode
from ..exceptions import ValidationError
from ..utils import validate_schema

class InputProcessor:
    """Handle input validation and processing"""
    
    def __init__(self, config: Optional[ProcessorConfig] = None):
        """
        Initialize input processor with configuration.
        
        Args:
            config: Optional processor configuration
        """
        self.config = config or ProcessorConfig(
            validate_schema=True,
            strict_mode=True,
            custom_validators=None,
            error_handling=ProcessingMode.STRICT
        )
        
    def validate(self, data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
        """
        Validate input against schema.
        
        Args:
            data: Input data to validate
            schema: Schema to validate against
            
        Returns:
            ValidationResult: Validation results with status and errors
            
        Raises:
            ValidationError: If validation fails in strict mode
        """
        errors: List[str] = []
        
        # Basic schema validation
        if not validate_schema(data, schema):
            errors.append("Data does not match schema structure")
            
        # Run custom validators if configured
        if self.config["custom_validators"]:
            for validator in self.config["custom_validators"]:
                # In a real implementation, we would load and run custom validators
                pass
                
        # Handle validation results based on error handling mode
        if errors and self.config["error_handling"] == ProcessingMode.STRICT:
            raise ValidationError("\n".join(errors))
            
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
        
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-process input data.
        
        Args:
            data: Input data to process
            
        Returns:
            dict: Processed input data
            
        This method can be extended to:
        - Normalize values
        - Convert data types
        - Apply default values
        - Remove unnecessary fields
        """
        processed_data = data.copy()
        
        # Example processing steps:
        for key, value in processed_data.items():
            # Convert string values to lowercase if they're strings
            if isinstance(value, str):
                processed_data[key] = value.lower()
                
            # Convert numeric strings to numbers where appropriate
            if isinstance(value, str) and value.replace(".", "").isdigit():
                try:
                    processed_data[key] = float(value) if "." in value else int(value)
                except ValueError:
                    pass
                    
        return processed_data
        
    def sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize input data for security.
        
        Args:
            data: Input data to sanitize
            
        Returns:
            dict: Sanitized input data
        """
        sanitized_data = data.copy()
        
        # Example sanitization rules:
        for key, value in sanitized_data.items():
            if isinstance(value, str):
                # Remove potential SQL injection patterns
                value = value.replace("'", "").replace('"', "").replace(";", "")
                # Remove potential script tags
                value = value.replace("<script>", "").replace("</script>", "")
                sanitized_data[key] = value
                
        return sanitized_data
