"""
Custom exception classes for the intention framework.
These exceptions help provide clear error messages and proper error handling
throughout the application.
"""

class IntentionError(Exception):
    """Base exception for all intention errors"""
    pass

class ValidationError(IntentionError):
    """Raised when validation fails for inputs, outputs, or schemas"""
    pass

class ProviderError(IntentionError):
    """Raised when provider interaction fails"""
    pass

class TemplateError(IntentionError):
    """Raised when template processing or registration fails"""
    pass

class ConfigurationError(IntentionError):
    """Raised when there are configuration issues"""
    pass

class ProcessingError(IntentionError):
    """Raised when processing of inputs or outputs fails"""
    pass

class AuthenticationError(ProviderError):
    """Raised when authentication with a provider fails"""
    pass

class RateLimitError(ProviderError):
    """Raised when provider rate limits are exceeded"""
    pass

class ResponseFormatError(ProviderError):
    """Raised when provider response format is invalid"""
    pass
