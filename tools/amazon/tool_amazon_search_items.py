import os
import sys
import json
import logging

# Configure logging to stderr at module level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from amazon_paapi.models.item_result import ApiBrowseNodeInfo
from libs.amazon.models import (
    PrettyCategoriesListModel,
    PrettyCategoryModel
)
# from agno.tools import tool
# from utils.logger_hook import logger_hook
  

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

# if __name__ == "__main__":
#     # Example usage of the tool
#     result = tool_amazon_search_items(
#         keywords="smart home",
#     )
#     logger.info(result)
    
#     # The detailed information is already printed by the function
#     logger.info(f"\nFunction returned {len(result)} products as AmazonProductPrettyResponse objects.")
