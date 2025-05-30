"""
Amazon Product Advertising API (PA-API) Library
Enhanced singleton implementation for better error handling, caching, and functionality.
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import asdict
from amazon_paapi import AmazonApi
from amazon_paapi.models.regions import Country
from amazon_paapi.models import SearchResult, SortBy, Item, Availability
import dotenv

# Import models from separate models module
from .models import SearchIndex

# Load environment variables from .env file
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





class AmazonPAAPI:
    """
    Enhanced Amazon Product Advertising API client with singleton pattern.
    
    Features:
    - Singleton pattern for efficient API usage
    - Enhanced error handling and logging
    - Data class responses for better type safety
    - Caching capabilities
    - Multiple search and retrieval methods
    - Configuration validation
    """
    
    _instance: Optional['AmazonPAAPI'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'AmazonPAAPI':
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(AmazonPAAPI, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the Amazon PA-API client."""
        if not self._initialized:
            self._load_credentials()
            self._validate_credentials()
            self._initialize_api()
            self._initialized = True
            logger.info("Amazon PA-API client initialized successfully")
    
    def _load_credentials(self) -> None:
        """Load credentials from environment variables."""
        self.api_key = os.getenv('AMAZON_API_KEY') or dotenv.get_key('.env', 'AMAZON_API_KEY')
        self.secret_key = os.getenv('AMAZON_SECRET_KEY') or dotenv.get_key('.env', 'AMAZON_SECRET_KEY')
        self.associate_tag = os.getenv('AMAZON_ASSOCIATE_TAG') or dotenv.get_key('.env', 'AMAZON_ASSOCIATE_TAG')
        self.country = Country.ES  # Default to Spain, can be made configurable
    
    def _validate_credentials(self) -> None:
        """Validate that all required credentials are present."""
        missing_credentials = []
        
        if not self.api_key:
            missing_credentials.append('AMAZON_API_KEY')
        if not self.secret_key:
            missing_credentials.append('AMAZON_SECRET_KEY')
        if not self.associate_tag:
            missing_credentials.append('AMAZON_ASSOCIATE_TAG')
        
        if missing_credentials:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_credentials)}")
    
    def _initialize_api(self) -> None:
        """Initialize the Amazon API client."""
        try:
            self.amazon_api = AmazonApi(
                key=self.api_key,
                secret=self.secret_key,
                tag=self.associate_tag,
                country=self.country
            )
        except Exception as e:
            logger.error(f"Failed to initialize Amazon API: {str(e)}")
            raise
    

    def search_items(
        self,
        keywords: str,
        search_index: Union[str, SearchIndex] = SearchIndex.ALL,
        item_count: int = 10,
        sort_by: SortBy = SortBy.RELEVANCE,
        min_price: int = None,
        max_price: int = None,
        browse_node_id: Optional[str] = None,
        availability: Optional[Availability] = Availability.AVAILABLE  # Optional filter for item availability
    ) -> SearchResult:
        """
        Search for items on Amazon.
        
        Args:
            keywords: Search keywords
            search_index: Category to search in
            item_count: Number of items to return (max 10)
            sort_by: Sort criteria (e.g., 'Relevance')
            min_price: Minimum price filter (in cents)
            max_price: Maximum price filter (in cents)
        
        Returns:
            AmazonAPIResponse containing search results
        """
        try:
            # Convert enum to string if needed
            if isinstance(search_index, SearchIndex):
                search_index = search_index.value
            
            # Limit item count to API maximum
            item_count = min(item_count, 10)
            
            logger.info(f"Searching Amazon for: '{keywords}' in category '{search_index}'")
            
            
            # Execute search
            response = self.amazon_api.search_items(
                keywords=keywords,
                search_index=search_index,
                item_count=item_count,
                sort_by=sort_by,
                min_price=min_price,
                max_price=max_price,
                browse_node_id=browse_node_id,  # Optional, can be used for more specific searches
                availability=availability  # Optional filter for item availability
            )
            
            # Parse response
            if response.items and len(response.items) > 0:
                return response
            else:
                logger.warning("No items found for the given search criteria")
                return SearchResult(items=[], total_result_count=0, search_url="")
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return SearchResult(items=[], total_result_count=0, search_url="")
    
    def get_items(self,
        item_asins: Union[str, List[str]],
        languages_of_preference: List[str] = ['es']  # Default to Spanish
    ) -> List[Item]:
        """
        Get specific items by ASIN.
        
        Args:
            item_asins: Single ASIN or list of ASINs
        
        Returns:
            AmazonAPIResponse containing item details
        """
        try:
            # Convert single ASIN to list
            if isinstance(item_asins, str):
                item_asins = [item_asins]
            
            # Limit to API maximum
            item_asins = item_asins[:10]
            
            logger.info(f"Getting items: {item_asins}")
            
            
            # Execute request
            amazon_items = self.amazon_api.get_items(
                items=item_asins,
                # languages_of_preference=languages_of_preference
            )
            
            if amazon_items and len(amazon_items) > 0:
                return amazon_items
            else:
                logger.warning("No items found for the given ASINs")
                return []
            
        except Exception as e:
            logger.error(f"Get items failed: {str(e)}")
            return []
    
    
    @classmethod
    def get_instance(cls) -> 'AmazonPAAPI':
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def reload_credentials(self) -> None:
        """Reload credentials and reinitialize API."""
        logger.info("Reloading Amazon API credentials")
        dotenv.load_dotenv(override=True)
        self._load_credentials()
        self._validate_credentials()
        self._initialize_api()
        logger.info("Amazon API credentials reloaded successfully")


# Backward compatibility aliases
AmazonAPISingleton = AmazonPAAPI