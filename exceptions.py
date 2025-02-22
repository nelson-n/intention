"""
Custom exception classes for the intention framework.
These exceptions help provide clear error messages and proper error handling
throughout the application.
"""

class IntentionError(Exception):
    """Base exception for all intention errors"""

class ValidationError(IntentionError):
    """Raised when validation fails"""

class ProviderError(IntentionError):
    """Raised when provider interaction fails"""
