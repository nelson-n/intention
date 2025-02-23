"""
Output processing functionality for the intention framework.
Handles the post-processing and formatting of generated content
after it's been processed by the template system.
"""

from typing import Dict, Any, Optional, List
from ..core.types import ProcessorConfig, ValidationResult, ProcessingMode, JsonType
from ..exceptions import ValidationError, ProcessingError
from ..utils import validate_schema, validate_json
import json

class OutputProcessor:
    """Handle output validation and formatting"""
    
    def __init__(self, config: Optional[ProcessorConfig] = None):
        """
        Initialize output processor with configuration.
        
        Args:
            config: Optional processor configuration
        """
        self.config = config or ProcessorConfig(
            validate_schema=True,
            strict_mode=True,
            custom_validators=None,
            error_handling=ProcessingMode.STRICT
        )
        
    def validate(self, data: str, schema: Dict[str, Any]) -> ValidationResult:
        """
        Validate output against schema.
        
        Args:
            data: Raw output data to validate
            schema: Schema to validate against
            
        Returns:
            ValidationResult: Validation results with status and errors
            
        Raises:
            ValidationError: If validation fails in strict mode
        """
        errors: List[str] = []
        
        # First validate JSON format
        if not validate_json(data):
            errors.append("Invalid JSON format")
            if self.config["error_handling"] == ProcessingMode.STRICT:
                raise ValidationError("Invalid JSON format in output")
            return {"valid": False, "errors": errors}
            
        # Parse JSON for further validation
        try:
            parsed_data = self.format(data)
            
            # Print parsed data for debugging
            print("\nParsed response data:")
            print("=" * 50)
            print(json.dumps(parsed_data, indent=2))
            print("=" * 50)
            
        except ProcessingError as e:
            errors.append(str(e))
            if self.config["error_handling"] == ProcessingMode.STRICT:
                raise
            return {"valid": False, "errors": errors}
            
        # Validate against schema
        if not validate_schema(parsed_data, schema):
            errors.append("Output does not match schema structure")
            
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
        
    def format(self, data: str) -> Dict[str, Any]:
        """
        Format output according to schema.
        
        Args:
            data: Raw output data to format
            
        Returns:
            dict: Formatted output data
            
        Raises:
            ProcessingError: If formatting fails
        """
        try:
            formatted_data = json.loads(data)
            
            # Ensure we have a dictionary
            if not isinstance(formatted_data, dict):
                raise ProcessingError("Output must be a JSON object")
                
            # Process nested structures
            formatted_data = self._process_nested_structures(formatted_data)
            
            return formatted_data
            
        except json.JSONDecodeError as e:
            raise ProcessingError(f"Failed to parse JSON: {str(e)}")
            
    def _process_nested_structures(self, data: JsonType) -> JsonType:
        """
        Recursively process nested data structures.
        
        Args:
            data: Data to process
            
        Returns:
            Processed data maintaining the same structure
        """
        if isinstance(data, dict):
            return {k: self._process_nested_structures(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._process_nested_structures(item) for item in data]
        elif isinstance(data, str):
            # Try to convert string numbers to actual numbers
            try:
                if "." in data:
                    return float(data)
                return int(data)
            except ValueError:
                return data.strip()
        return data
        
    def enrich_output(self, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Enrich output data with additional context or computed values.
        
        Args:
            data: Output data to enrich
            context: Optional context data for enrichment
            
        Returns:
            dict: Enriched output data
        """
        enriched_data = data.copy()
        
        if context:
            # Add any relevant context data
            enriched_data["_context"] = context
            
        # Add metadata
        enriched_data["_metadata"] = {
            "timestamp": self._get_timestamp(),
            "version": "1.0.0",
            # Add other metadata as needed
        }
        
        return enriched_data
        
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
