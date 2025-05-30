#!/usr/bin/env python3
"""
Servidor MCP Simple con FastMCP - Solo ladra como un perro
"""

import logging
import sys
import os
from mcp.server.fastmcp import FastMCP
from typing import List
from amazon_paapi.models import SortBy, Availability
from libs.amazon import AmazonAPISingleton
from libs.amazon.models import AmazonProductPrettyResponse, SearchIndex
from tools.amazon.tool_amazon_search_items import extract_categories

# Configuración de logging - CRÍTICO: enviar logs a stderr, NO stdout
# para evitar contaminar las respuestas JSON del MCP
logging.basicConfig(
    level=logging.ERROR,  # Solo errores críticos
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,  # IMPORTANTE: logs van a stderr, no stdout
    force=True  # Forzar reconfiguración de logging
)

# Configurar todos los loggers conocidos para que vayan a stderr
for logger_name in ['libs.amazon', 'httpx', 'amazon_paapi', 'agno', 'urllib3']:
    specific_logger = logging.getLogger(logger_name)
    specific_logger.handlers.clear()
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    specific_logger.addHandler(stderr_handler)
    specific_logger.setLevel(logging.ERROR)
    specific_logger.propagate = False

logger = logging.getLogger(__name__)

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logger.warning(f"✅ Variables de entorno cargadas desde {env_path}")
    else:
        logger.warning(f"⚠️ No se encontró archivo .env en {env_path}")
except ImportError:
    logger.warning("⚠️ python-dotenv no disponible, usando variables del sistema")

# Crear servidor FastMCP
mcp = FastMCP("dog-server")

@mcp.tool(
    name="tool_amazon_search_discovery",
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
            - (str) "All": Translate: Todos los departamentos
            - (str) "AmazonVideo": Translate: Prime Video
            - (str) "Apparel": Translate: Ropa y accesorios
            - (str) "Appliances": Translate: Grandes electrodomésticos
            - (str) "Automotive": Translate: Coche y moto
            - (str) "Baby": Translate: Bebé
            - (str) "Beauty": Translate: Belleza
            - (str) "Books": Translate: Libros
            - (str) "Computers": Translate: Informática
            - (str) "DigitalMusic": Translate: Música Digital
            - (str) "Electronics": Translate: Electrónica
            - (str) "EverythingElse": Translate: Otros Productos
            - (str) "Fashion": Translate: Moda
            - (str) "ForeignBooks": Translate: Libros en idiomas extranjeros
            - (str) "GardenAndOutdoor": Translate: Jardín
            - (str) "GiftCards": Translate: Cheques regalo
            - (str) "GroceryAndGourmetFood": Translate: Alimentación y bebidas
            - (str) "Handmade": Translate: Handmade
            - (str) "HealthPersonalCare": Translate: Salud y cuidado personal
            - (str) "HomeAndKitchen": Translate: Hogar y cocina
            - (str) "Industrial": Translate: Industria y ciencia
            - (str) "Jewelry": Translate: Joyería
            - (str) "KindleStore": Translate: Tienda Kindle
            - (str) "Lighting": Translate: Iluminación
            - (str) "Luggage": Translate: Equipaje
            - (str) "MobileApps": Translate: Appstore para Android
            - (str) "MoviesAndTV": Translate: Películas y TV
            - (str) "Music": Translate: Música: CDs y vinilos
            - (str) "MusicalInstruments": Translate: Instrumentos musicales
            - (str) "OfficeProducts": Translate: Oficina y papelería
            - (str) "PetSupplies": Translate: Productos para mascotas
            - (str) "Shoes": Translate: Zapatos y complementos
            - (str) "Software": Translate: Software
            - (str) "SportsAndOutdoors": Translate: Deportes y aire libre
            - (str) "ToolsAndHomeImprovement": Translate: Bricolaje y herramientas
            - (str) "ToysAndGames": Translate: Juguetes y juegos
            - (str) "Vehicles": Translate: Coche - renting
            - (str) "VideoGames": Translate: Videojuegos
            - (str) "Watches": Translate: Relojes
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
                logger.info(f"Skipping item (ASIN: {pretty_item.asin}) due to no EANs.")
                continue
            pretty_response.append(pretty_item.to_dict())
        if not pretty_response:
            logger.info("No items found for the given search criteria.")
            return []
        else:
            logger.info(f"Found {len(pretty_response)} items matching the search criteria.")
            return pretty_response

    except Exception as e:
        # Handle exceptions and return an empty SearchResult
        logger.error(f"Error during Amazon search: {e}")
        return []

if __name__ == "__main__":
    # Solo logs críticos van a stderr - no contaminar stdout del MCP
    logger.warning("🐕 Iniciando servidor MCP FastMCP")
    mcp.run()