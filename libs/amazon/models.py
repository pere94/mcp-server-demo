from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Any

class APIError(Exception):
    """Custom exception class for Amazon API errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class SearchIndex(Enum):
    """Amazon search categories enum for better type safety."""
    ALL = "All"
    ALEXA_SKILLS = "AlexaSkills"
    AMAZON_VIDEO = "AmazonVideo"
    APPLIANCES = "Appliances"
    APPS_GAMES = "AppsGames"
    AUTOMOTIVE = "Automotive"
    BABY = "Baby"
    BEAUTY = "Beauty"
    BOOKS = "Books"
    CLASSICAL = "Classical"
    CLOTHING_SHOES_JEWELRY = "ClothingAccessories"
    COLLECTIBLES_FINE_ART = "Collectibles"
    COMPUTERS = "Computers"
    DIGITAL_MUSIC = "DigitalMusic"
    ELECTRONICS = "Electronics"
    EVERYTHING_ELSE = "EverythingElse"
    FASHION = "Fashion"
    GARDEN_OUTDOOR = "GardenAndOutdoor"
    GIFT_CARDS = "GiftCards"
    GROCERY = "Grocery"
    HANDMADE = "Handmade"
    HEALTH_HOUSEHOLD = "HealthPersonalCare"
    HOME_KITCHEN = "HomeKitchen"
    INDUSTRIAL_SCIENTIFIC = "Industrial"
    KINDLE_STORE = "KindleStore"
    LUGGAGE = "Luggage"
    LUXURY_BEAUTY = "LuxuryBeauty"
    MAGAZINES = "Magazines"
    MOVIES_TV = "MoviesTV"
    MUSIC = "Music"
    MUSICAL_INSTRUMENTS = "MusicalInstruments"
    OFFICE_PRODUCTS = "OfficeProducts"
    PET_SUPPLIES = "PetSupplies"
    PHOTO = "Photo"
    SOFTWARE = "Software"
    SPORTS_OUTDOORS = "SportsOutdoors"
    TOOLS_HOME_IMPROVEMENT = "ToolsHomeImprovement"
    TOYS_GAMES = "ToysGames"
    VIDEO_GAMES = "VideoGames"

@dataclass
class PrettyCategoryModel:
    name: str
    id: str

@dataclass
class PrettyCategoriesListModel:
    categories: List[PrettyCategoryModel]

@dataclass
class AmazonProductPrettyResponse:
    """Dataclass to represent a pretty-printed Amazon product response."""
    title: str = ""
    asin: str = ""
    affiliate_link: str = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    features: Optional[str] = None
    brand: Optional[str] = None
    discount: Optional[float] = None
    categories: List[PrettyCategoryModel] = None
    eans: Optional[List[str]] = None
    
    def __post_init__(self):
        """Initialize categories as empty list if None."""
        if self.categories is None:
            self.categories = []
    
    def __str__(self):
        price_str = f"${self.price}" if self.price else "Price not available"
        brand_str = f" | Brand: {self.brand}" if self.brand else ""
        discount_str = f" | Discount: {self.discount}%" if self.discount else ""
        return f"Product: {self.title} | ASIN: {self.asin} | Price: {price_str}{brand_str}{discount_str}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convert the dataclass to a dictionary for better agent consumption."""
        return {
            'title': self.title,
            'asin': self.asin,
            'affiliate_link': self.affiliate_link,
            'price': self.price,
            'old_price': self.old_price,
            'image_url': self.image_url,
            'description': self.description,
            'features': self.features,
            'brand': self.brand,
            'discount': self.discount,
            'categories': [category.__dict__ for category in self.categories] if self.categories else [],
            'eans': self.eans if self.eans else []
        }
    
    def to_formatted_string(self):
        """Convert to a well-formatted string with all details for agent consumption."""
        lines = [
            f"Title: {self.title}",
            f"ASIN: {self.asin}",
            f"Price: ${self.price}" if self.price else "Price: Not available",
        ]
        
        if self.old_price:
            lines.append(f"Original Price: ${self.old_price}")
        if self.brand:
            lines.append(f"Brand: {self.brand}")
        if self.discount:
            lines.append(f"Discount: {self.discount}%")
        if self.image_url:
            lines.append(f"Image URL: {self.image_url}")
        if self.description:
            lines.append(f"Description: {self.description}")
        
        return " | ".join(lines)
    
