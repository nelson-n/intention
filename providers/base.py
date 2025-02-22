"""
Base provider interface for the intention framework.
Defines the abstract base class and common interfaces that all providers
must implement to integrate with the framework.
"""

class BaseProvider:
    """Base interface for LLM providers"""
    async def complete(self, prompt: str) -> str:
        """Send prompt to LLM and get response"""
    
    def validate_response(self, response: str) -> bool:
        """Validate LLM response"""