"""
Client interface for the intention framework.
Provides the main entry point for applications to interact with the framework,
managing provider connections and template processing operations.
"""

class IntentionClient:
    """Main client class for the intention framework"""
    def __init__(self, provider: str, api_key: str)
    async def process(self, template: str, data: dict) -> dict:
        """Process data through a template and return formatted results"""
