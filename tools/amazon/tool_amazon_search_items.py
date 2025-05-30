import os
import sys
import json

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from typing import List
from amazon_paapi.models import SearchResult, SortBy, Item, Availability
from amazon_paapi.models.item_result import ApiBrowseNodeInfo
from libs.amazon import AmazonAPISingleton
from libs.amazon.models import (SearchIndex,
    AmazonProductPrettyResponse,
    PrettyCategoriesListModel,
    PrettyCategoryModel
)
from agno.tools import tool
from utils.logger_hook import logger_hook


@tool(
    name="tool_amazon_search_items",            # Custom name for the tool (otherwise the function name is used)
    description="Search for items on Amazon",  # Custom description (otherwise the function docstring is used)
    show_result=False,                               # Show result after function call
    stop_after_tool_call=False,                      # Return the result immediately after the tool call and stop the agent
    tool_hooks=[logger_hook],                       # Hook to run before and after execution
    cache_results=True,                             # Enable caching of results
    cache_dir="/tmp/agno_cache",                    # Custom cache directory
    cache_ttl=3600                                  # Cache TTL in seconds (1 hour)
)
def tool_amazon_search_items(
    keywords: str,
    item_count: int = 10,
    search_index: str = SearchIndex.ALL,
    sort_by: str = SortBy.RELEVANCE,
    min_price: int = None,
    max_price: int = None,
    only_with_ean: bool = True,
    browse_node_id: str = None,
    availability: str = Availability.AVAILABLE  # Optional filter for item availability
) -> List[AmazonProductPrettyResponse]:
    """
    Search for items based on keywords and search index.

    Args:
        keywords (str): Keywords to search for.
        search_index (str): The category to search in (default is "All").
            - (str) "All" - Translate: Todos los departamentos
            - (str) "AlexaSkills" - Translate: "Alexa Skills"
            - (str) "AmazonVideo" - Translate: "Prime Video"
            - (str) "Appliances" - Translate: "Grandes electrodomésticos"
            - (str) "AppsGames" - Translate: "Appstore para Android"
            - (str) "Automotive" - Translate: "Coche y moto"
            - (str) "Baby" - Translate: "Bebé"
            - (str) "Beauty" - Translate: "Belleza"
            - (str) "Books" - Translate: "Libros"
            - (str) "Classical" - Translate: "Música clásica"
            - (str) "ClothingAccessories" - Translate: "Ropa y accesorios"
            - (str) "Collectibles" - Translate: "Coleccionables"
            - (str) "Computers" - Translate: "Informática"
            - (str) "DigitalMusic" - Translate: "Música Digital"
            - (str) "Electronics" - Translate: "Electrónica"
            - (str) "EverythingElse" - Translate: "Otros Productos"
            - (str) "Fashion" - Translate: "Moda"
            - (str) "GardenAndOutdoor" - Translate: "Jardín"
            - (str) "GiftCards" - Translate: "Cheques regalo"
            - (str) "GroceryAndGourmetFood" - Translate: "Alimentación y bebidas"
            - (str) "Handmade" - Translate: "Handmade"
            - (str) "HealthPersonalCare" - Translate: "Salud y cuidado personal"
            - (str) "HomeAndKitchen" - Translate: "Hogar y cocina"
            - (str) "Industrial" - Translate: "Industria y ciencia"
            - (str) "KindleStore" - Translate: "Tienda Kindle"
            - (str) "Luggage" - Translate: "Equipaje"
            - (str) "LuxuryBeauty" - Translate: "Belleza de lujo"
            - (str) "Magazines" - Translate: "Revistas"
            - (str) "MoviesTV" - Translate: "Películas y TV"
            - (str) "Music" - Translate: "Música"
            - (str) "MusicalInstruments" - Translate: "Instrumentos musicales"
            - (str) "OfficeProducts" - Translate: "Oficina y papelería"
            - (str) "PetSupplies" - Translate: "Productos para mascotas"
            - (str) "Photo" - Translate: "Fotografía"
            - (str) "Software" - Translate: "Software"
            - (str) "SportsOutdoors" - Translate: "Deportes y aire libre"
            - (str) "ToolsAndHomeImprovement" - Translate: "Bricolaje y herramientas"
            - (str) "ToysAndGames" - Translate: "Juguetes y juegos"
            - (str) "VideoGames" - Translate: "Videojuegos"
        item_count (int): Number of items to return (default is 10, maximum is 10 due to Amazon API limitations).
        sort_by (SortBy): Sorting criteria for the results (default is SortBy.RELEVANCE).
            - (str) "AvgCustomerReviews": Sorts results according to average customer reviews
            - (str) "Featured": Sorts results with featured items having higher rank. Recomended for search with search_index and without keywords.
            - (str) "NewestArrivals": Sorts results with according to newest arrivals
            - (str) "Price:HighToLow": Sorts results according to most expensive to least expensive
            - (str) "Price:LowToHigh": Sorts results according to least expensive to most expensive
            - (str) "Relevance": Sorts results with relevant items having higher rank. Recomended for search with keywords.
        min_price (int, optional): Minimum price € filter (default is None).
        max_price (int, optional): Maximum price € filter (default is None).
        only_with_ean (bool): If True, only returns items with EANs (European Article Numbers) (default is True).
        browse_node_id (str, optional): Specific browse node ID to filter results (default is None).
        availability (Availability): Filter for item availability (default is Availability.AVAILABLE).
            - (str) "Available": Translate: "Disponible"
            - (str) "IncludeOutOfStock": Translate: "Incluir sin stock"

    Returns:
        AmazonProductPrettyResponse: Search results containing items matching the criteria.
            - title: str = {title of the product}
            - asin: str = {Amazon Standard Identification Number}
            - affiliate_link: str = {URL to the product page on Amazon}
            - price: float = {price of the product}
            - old_price: float = {previous price of the product, if available}
            - image_url: str = {URL of the product image}
            - description: str = {description of the product}
            - features: str = {summary features of the product}
            - brand: str = {brand of the product}
            - discount: float = {discount percentage of the product, if available}
            - categories: List[PrettyCategoryModel] = {list of categories the product belongs to}
                * PrettyCategoryModel:
                    - name: str = {name of the category}
                    - id: str = {ID of the category}
            - eans: List[str] = {list of EANs (European Article Numbers) of the product, if available}
    """

    try:
        # Validate the search index
        if not keywords:
            raise ValueError("Keywords must not be empty.")
        if min_price:
            min_price = int(min_price)*100  # Convert to cents
        if max_price:
            max_price = int(max_price)*100  # Convert to cents
        if min_price and max_price and min_price > max_price:
            raise ValueError("Minimum price cannot be greater than maximum price.")

        client = AmazonAPISingleton()
        response = client.search_items(
            keywords=keywords,
            search_index=search_index,
            item_count=item_count,
            sort_by=sort_by,
            min_price=min_price,
            max_price=max_price,
            browse_node_id=browse_node_id,
            availability=availability
        )

        pretty_response: List[AmazonProductPrettyResponse] = []
        for item in response.items:
            # Safely extract price information
            _price = None
            if (item.offers
                and item.offers.listings
                and len(item.offers.listings) > 0 
                and item.offers.listings[0].price
                and item.offers.listings[0].price.amount
            ):
                _price = item.offers.listings[0].price.amount
            
            # Safely extract discount information
            _discount = 0
            if (item.offers
                and item.offers.listings
                and len(item.offers.listings) > 0
                and item.offers.listings[0].price.savings
                and item.offers.listings[0].price.savings.percentage
                and item.offers.listings[0].price.savings.percentage > 0
            ):
                _discount = item.offers.listings[0].price.savings.percentage
            
            # Safely extract old price
            _old_price = 0
            if (item.offers 
                and item.offers.listings 
                and len(item.offers.listings) > 0 
                and item.offers.listings[0].saving_basis 
                and item.offers.listings[0].saving_basis.amount
                and item.offers.listings[0].saving_basis.amount > 0
            ):
                _old_price = item.offers.listings[0].saving_basis.amount
            
            # Safely extract description
            _description = ""
            if (item.item_info 
                and item.item_info.features 
                and item.item_info.features.display_values
            ):
                _description = " ||| ".join(item.item_info.features.display_values)
            
            # Safely extract brand
            _brand = None
            if (item.item_info 
                and item.item_info.by_line_info 
                and item.item_info.by_line_info.brand 
                and item.item_info.by_line_info.brand.display_value
            ):
                _brand = item.item_info.by_line_info.brand.display_value

            _eans = []
            if (item.item_info 
                and item.item_info.external_ids 
                and item.item_info.external_ids.ea_ns 
                and item.item_info.external_ids.ea_ns.display_values
            ):
                _eans = item.item_info.external_ids.ea_ns.display_values

            # Create the dataclass instance
            pretty_item = AmazonProductPrettyResponse(
                title=item.item_info.title.display_value if item.item_info and item.item_info.title else "",
                asin=item.asin if item.asin else "",
                affiliate_link=item.detail_page_url if item.detail_page_url else "",
                price=_price,
                old_price=_old_price,
                image_url=item.images.primary.large.url if item.images and item.images.primary and item.images.primary.large else None,
                description=_description,
                features="",
                brand=_brand,
                discount=_discount,
                categories=extract_categories(item.browse_node_info).categories if item.browse_node_info else [],
                eans=_eans
            )
            if only_with_ean and len(_eans) == 0:
                print(f"Skipping item (ASIN: {pretty_item.asin}) due to no EANs.")
                continue
            pretty_response.append(pretty_item.to_dict())
        if not pretty_response:
            print("No items found for the given search criteria.")
            return []
        else:
            print(f"Found {len(pretty_response)} items matching the search criteria.")
            return pretty_response

    except Exception as e:
        # Handle exceptions and return an empty SearchResult
        print(f"Error during Amazon search: {e}")
        return []
    

def extract_categories(browse_nodes_info: ApiBrowseNodeInfo) -> PrettyCategoriesListModel:
    """
    Extracts categories from the ApiBrowseNodeInfo object and returns a PrettyCategoriesListModel.

    Args:
        browse_nodes_info (ApiBrowseNodeInfo): The ApiBrowseNodeInfo object containing category information.

    Returns:
        PrettyCategoriesListModel: A model containing the extracted categories.
    """
    if (browse_nodes_info
        and browse_nodes_info.browse_nodes
        and len(browse_nodes_info.browse_nodes) > 0
        and browse_nodes_info.browse_nodes[0]
    ):
        setted_names = set()
        categories = []
        current_node = browse_nodes_info.browse_nodes[0]
        actual_ancestor = current_node.ancestor

        while actual_ancestor:
            name = actual_ancestor.context_free_name
            if name not in setted_names:       # evita duplicados
                categories.append(PrettyCategoryModel(
                    name=name,
                    id=actual_ancestor.id
                ))
                setted_names.add(name)
            actual_ancestor = actual_ancestor.ancestor      # sube un nivel
    
    categories.reverse() # Reverses the order to have the root category first
    return PrettyCategoriesListModel(categories=categories)

if __name__ == "__main__":
    # Example usage of the tool
    result = tool_amazon_search_items(
        keywords="smart home",
    )
    print(result)
    
    # The detailed information is already printed by the function
    print(f"\nFunction returned {len(result)} products as AmazonProductPrettyResponse objects.")
    