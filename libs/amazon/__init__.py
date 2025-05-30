"""
Amazon Product Advertising API Library
Enhanced implementation with type safety and better error handling.
"""

from .lib_amazon import (
    # Main classes
    AmazonPAAPI,
    AmazonAPISingleton,  # Backward compatibility
    
    # Data classes
    SearchResult,
    
    # Enums
    SearchIndex,
)

__all__ = [
    # Main classes
    'AmazonPAAPI',
    'AmazonAPISingleton',
    
    # Data classes
    'AmazonAPIResponse',
    'SearchResult', 
    'ItemsResult',
    'AmazonProduct',
    'ProductItemInfo',
    'ProductImages',
    'ProductImage',
    'ProductOffer',
    'ProductPrice',
    'APIError',
    
    # Enums
    'SearchIndex',
]

# Version info
__version__ = '2.0.0'
__author__ = 'Pinterest AI Team'
__description__ = 'Enhanced Amazon Product Advertising API library'
