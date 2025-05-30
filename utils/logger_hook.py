import logging
import sys
from typing import Any, Callable, Dict

# Configure logger to send to stderr only
logger = logging.getLogger(__name__)
logger.handlers.clear()
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(stderr_handler)
logger.setLevel(logging.INFO)
logger.propagate = False

def logger_hook(function_name: str, function_call: Callable, arguments: Dict[str, Any]):
    """Pre-hook function that runs before the tool execution"""
    # Use stderr logging instead of print to avoid contaminating stdout
    logger.info(f"About to call {function_name} with arguments: {arguments}")
    result = function_call(**arguments)
    logger.info(f"Function call completed with result: {result}")
    return result