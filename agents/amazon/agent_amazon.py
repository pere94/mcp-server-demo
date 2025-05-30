import os
import sys
import logging

# Configure logging to stderr at module level
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

import typer
from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from tools.amazon.tool_amazon_search_items import tool_amazon_search_items
# from agno.tools.thinking import ThinkingTools
# from agno.storage.postgres import PostgresStorage
from pydantic import BaseModel, Field
from typing import List, Optional

# db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
# storage = PostgresStorage(table_name="pdf_agent", db_url=db_url)

class PrettyCategoryModel(BaseModel):
    name: str = Field(..., description="Name of the category")
    id: str = Field(..., description="Unique identifier for the category")

class SearchItemModel(BaseModel):
    title: str = Field(..., description="Title of the product")
    asin: str = Field(..., description="Amazon Standard Identification Number (ASIN)")
    affiliate_link: str = Field(..., description="URL to the product page on Amazon")
    price: float = Field(..., description="Price of the product")
    old_price: float = Field(..., description="Previous price of the product, if not available set 0")
    image_url: str = Field(..., description="URL of the product image")
    description: str = Field(..., description="Description of the product")
    features: str = Field(..., description="Processed keywords summary of main product characteristics")
    brand: str = Field(..., description="Brand of the product")
    discount: float = Field(..., description="Discount percentage of the product, if not available set 0")
    categories: List[PrettyCategoryModel] = Field(default_factory=list, description="List of categories the product belongs to")
    eans: Optional[List[str]] = Field(default=None, description="List of EANs (European Article Numbers) for the product, if available")
    availability: Optional[str] = Field(default=None, description="Availability status of the product, if available")

class AgentAmazonResponseModel(BaseModel):
    search_results: list[SearchItemModel] = Field(default_factory=list)

# Initialize the research agent with advanced journalistic capabilities
agent_amazon = Agent(
    name="Amazon API Search Agent",
    # # Faster, more affordable reasoning model
    # # Reasoning=4pts | Speed=3pts
    # model=OpenAIChat(id="o4-mini"),
    # # Balanced for intelligence, speed, and cost ( Not reasoning model )
    # # Reasoning=3pts | Speed=4pts
    model=OpenAIChat(id="gpt-4.1-mini"),
    reasoning_max_steps= 3,
    # storage=storage,
    # read_chat_history=True,
    # add_history_to_messages=True,
    # num_history_responses=3,
    tools=[
        # ThinkingTools(add_instructions=True),
        tool_amazon_search_items
    ],
    # use_json_mode=True,
    # response_model=AgentAmazonResponseModel,
    description=dedent("""\
        You are an Amazon Product Search Agent that specializes in finding products on Amazon based on keywords.
    """),
    instructions=dedent("""\
        🎯 YOUR MISSION: Search for products on Amazon using the provided keywords and return ALL API results with processed features.
        RESPONSE LANGUAGE: Spanish

        1. Product Search Tools 🔍
            - Use the tool_amazon_search_items tool to search for products

        2. Features processing 🛠️
            - Process the features field of the search results to extract and summarize the main characteristics of each product from the `title` and `description` fields.

        3. Return info
            - Return all the products found in the search results, avoid filter any results. I want all the results.
            - Return the results in the format specified in the response format example below.
            - Avoid return duplicated results in the final list.

    """),
    expected_output=dedent("""\
        The following is the response from Amazon's API with processed features field:

        *** The field `features` should contain a summary of the main characteristics of the product, extracted from the `title` and `description` fields. ***

        *** Response Format example (mandatory), min 10 results: ***
        ```json
            {
                "search_results": [
                    {
                        "title": "Example Product Title 1",
                        "asin": "B000123456",
                        "affiliate_link": "https://www.amazon.com/dp/B000123456",
                        "price": 99.99,
                        "old_price": 129.99,
                        "image_url": "https://images-na.ssl-images-amazon.com/images/I/81xw2Y1z5lL._AC_SL1500_.jpg",
                        "description": "This is an example product description that includes various features and specifications.",
                        "brand": "Example Brand",
                        "discount": 23.07,
                        "features": "Smart home, energy-efficient, compatible with Alexa and Google Assistant, easy installation, sleek design",
                        "categories": [
                            {
                                "name": "Electronics",
                                "id": "123"
                            },
                            {
                                "name": "Smart Home",
                                "id": "456"
                            }
                        ],
                        "eans": ["1234567890123", "9876543210987"]
                    }
                    ...,
                    {
                        "title": "Another Product Title 10",
                        "asin": "B000654321",
                        "affiliate_link": "https://www.amazon.com/dp/B000654321",
                        "price": 49.99,
                        "old_price": 59.99,
                        "image_url": "https://images-na.ssl-images-amazon.com/images/I/81xw2Y1z5lL._AC_SL1500_.jpg",
                        "description": "This is another example product description that includes various features and specifications.",
                        "brand": "Another Brand",
                        "discount": 16.67,
                        "features": "Outdoor, waterproof, solar-powered, motion sensor, easy to install",
                        "categories": [
                            {
                                "name": "Home & Kitchen",
                                "id": "789"
                            },
                            {
                                "name": "Outdoor",
                                "id": "101112"
                            }
                        ],
                        "eans": ["1234567890123", "9876543210987"]
                    }
                ]
            }
        ```

        ---
        *Amazon API data with intelligent feature keyword extraction*
    """),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    debug_mode=False,  # IMPORTANTE: Desactivar debug_mode para evitar contaminar stdout
)

if __name__ == "__main__":
    # Clear console output for clarity
    os.system('cls' if os.name == 'nt' else 'clear')

    # Code Example Test
    logger.info("Running Amazon API Search Agent...")
    def agent_runner(new: bool = False, user: str = "user"):
        # session_id: Optional[str] = None
        
        # if not new:
        #     existing_sessions: List[str] = storage.get_all_session_ids(user)
        #     if len(existing_sessions) > 0:
        #         session_id = existing_sessions[0]

        #     if session_id is None:
        #         session_id = agent_amazon.session_id
        #         print(f"Started Session: {session_id}\n")
        #     else:
        #         print(f"Continuing Session: {session_id}\n")

        # Runs the agent as a cli app
        agent_amazon.cli_app(markdown=True)


    typer.run(agent_runner)
    # # Run the agent with a sample query
    # response = agent_amazon.print_response(
    #     "Buscar productos de tecnología en Amazon relacionados con 'smart home devices' y con precios mayor que 50 euros, ordenalos por precio de manera ascendente. Refina un poco ams la busqueda usando los departamentos de amazon, puedes probar varios para ver cual es el mas adecuado para esat busqueda."
    # )