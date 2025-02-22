"""
This is a demonstration file that showcases the usage of the intention framework.
It provides examples of how to use the core functionality, including template processing,
provider integration, and error handling. Use this as a reference for implementing
your own applications using the framework.
"""

from intention import Template, template

@template(
    name="product_search",
    description="Template for searching products with specific criteria"
)
class ProductSearchTemplate(Template):
    input_schema = {
        "product_type": str,
        "location": str,
        "price_range": str
    }
    
    output_schema = {
        "products": list,
        "total_found": int
    }
    
    def format_prompt(self, data: dict) -> str:
        return f"""Find products matching these criteria:
                  - Type: {data['product_type']}
                  - Location: {data['location']}
                  - Price Range: {data['price_range']}
                  
                  Return results in JSON format with products list and total_found count."""
    
    def format_output(self, response: str) -> dict:
        # Convert the LLM's response to structured data
        # This is a simplified example - you'd want more robust JSON parsing
        import json
        return json.loads(response)
