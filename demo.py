"""
This is a demonstration file that showcases the usage of the intention framework.
It provides examples of how to use the core functionality, including template processing,
provider integration, and error handling. Use this as a reference for implementing
your own applications using the framework.
"""

from intention import Template, template
from typing import List, Dict, Optional

@template(
    name="restaurant_search",
    description="Template for finding restaurants based on location, cuisine, and price preferences"
)
class RestaurantSearchTemplate(Template):
    input_schema = {
        "location": str,        # e.g. "San Francisco, CA"
        "cuisine": str,         # e.g. "Italian"
        "price_range": str,     # e.g. "$$$" (1-4 dollar signs)
    }
    
    output_schema = {
        "restaurant": {
            "name": str,
            "address": str,
            "cuisine": str,
            "price_range": str,
            "rating": float,
            "description": str,
            "hours": Dict[str, str],  # e.g. {"Monday": "11:00 AM - 10:00 PM"}
            "phone": Optional[str],
            "website": Optional[str]
        },
        "match_score": float    # How well this matches the criteria (0-1)
    }
    
    def format_prompt(self, data: dict) -> str:
        return f"""Find a highly-rated restaurant matching these criteria:
                  - Location: {data['location']}
                  - Cuisine Type: {data['cuisine']}
                  - Price Range: {data['price_range']}
                  
                  Please provide detailed information about the best matching restaurant.
                  Include the restaurant name, full address, exact cuisine type, price range,
                  rating (out of 5 stars), a brief description, operating hours, phone number,
                  and website if available.
                  
                  Return the information in a JSON format with the following structure:
                  {{
                    "restaurant": {{
                      "name": "Restaurant Name",
                      "address": "Full Address",
                      "cuisine": "Specific Cuisine Type",
                      "price_range": "Price Range ($-$$$$)",
                      "rating": 4.5,
                      "description": "Brief description of the restaurant",
                      "hours": {{
                        "Monday": "11:00 AM - 10:00 PM",
                        "Tuesday": "11:00 AM - 10:00 PM",
                        "Wednesday": "11:00 AM - 10:00 PM",
                        "Thursday": "11:00 AM - 10:00 PM",
                        "Friday": "11:00 AM - 11:00 PM",
                        "Saturday": "12:00 PM - 11:00 PM",
                        "Sunday": "12:00 PM - 9:00 PM"
                      }},
                      "phone": "Phone number or null",
                      "website": "Website URL or null"
                    }},
                    "match_score": 0.95
                  }}"""
    
    def format_output(self, response: str) -> dict:
        """Convert the LLM's response to structured data"""
        import json
        from ..utils import validate_json
        
        if not validate_json(response):
            raise ValueError("Invalid JSON response from LLM")
            
        data = json.loads(response)
        
        # Validate required fields
        required_fields = ["name", "address", "cuisine", "price_range", "rating", "description", "hours"]
        for field in required_fields:
            if field not in data["restaurant"]:
                raise ValueError(f"Missing required field in response: {field}")
        
        # Validate rating range
        if not (0 <= data["restaurant"]["rating"] <= 5):
            raise ValueError("Rating must be between 0 and 5")
            
        # Validate match score range
        if not (0 <= data["match_score"] <= 1):
            raise ValueError("Match score must be between 0 and 1")
            
        return data

async def main():
    """Example usage of the restaurant search template"""
    from intention import IntentionClient
    import os
    from dotenv import load_dotenv
    
    # Load API key from environment
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    # Initialize the client with OpenAI provider
    client = IntentionClient(
        provider="openai",
        api_key=api_key
    )
    
    # Example search criteria
    search_data = {
        "location": "San Francisco, CA",
        "cuisine": "Italian",
        "price_range": "$$$"
    }
    
    try:
        # Process the search request
        result = await client.process("restaurant_search", search_data)
        
        # Print the results in a formatted way
        restaurant = result["restaurant"]
        print("\nRestaurant Found!")
        print("=" * 50)
        print(f"Name: {restaurant['name']}")
        print(f"Cuisine: {restaurant['cuisine']}")
        print(f"Price Range: {restaurant['price_range']}")
        print(f"Rating: {restaurant['rating']:.1f}/5.0")
        print(f"Match Score: {result['match_score']:.2%}")
        print("\nDescription:")
        print(restaurant['description'])
        print("\nAddress:", restaurant['address'])
        if restaurant.get('phone'):
            print("Phone:", restaurant['phone'])
        if restaurant.get('website'):
            print("Website:", restaurant['website'])
        print("\nHours:")
        for day, hours in restaurant['hours'].items():
            print(f"{day}: {hours}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
