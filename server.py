#!/usr/bin/env python3
"""
Servidor MCP Simple con FastMCP - Solo ladra como un perro
"""

import logging
import sys
import os
from mcp.server.fastmcp import FastMCP
from agno.agent import RunResponse
from agents.amazon.agent_amazon import agent_amazon

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

@mcp.tool()
async def tool_magic(number: float) -> str:
    """
    Suma 15 a un número dado
    
    Args:
        number: El número al que se le sumará 15
    """
    try:
        result = number + 15
        message = f"Resultado mágico: {number} + 15 = {result} ✨"
        # Comentado para evitar contaminar stdout con logs de debug
        # logger.info(f"🪄 Operación mágica: {message}")
        return message
        
    except (TypeError, ValueError) as e:
        error_msg = f"Error: El parámetro debe ser un número válido. {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool(
    name="tool_amazon_search_discovery",
    description="Performs a search on Amazon using the Amazon search agent. Does not modify the user query.",
)
async def tool_amazon_search_discovery(user_query: str) -> str:
    """
    Realiza una búsqueda en Amazon (search_items) utilizando el agente de búsqueda de Amazon.
    
    Args:
        user_query: La consulta de búsqueda del usuario completa sin modificar
    """
    try:
        if not user_query:
            raise ValueError("La consulta de búsqueda no puede estar vacía.")
        
        # Busqueda con agente - IMPORTANTE: NO usar await porque run() no es async
        response: RunResponse = agent_amazon.run(user_query)
        content = response.content

        if not content:
            raise ValueError("No se encontraron resultados.")

        # Comentado para evitar contaminar stdout - logs van a stderr
        # logger.info(f"🔎 Resultados de búsqueda en Amazon: {content}")
        return content

    except Exception as e:
        error_msg = f"Error al buscar en Amazon: {str(e)}"
        logger.error(error_msg)
        return error_msg


if __name__ == "__main__":
    # Solo logs críticos van a stderr - no contaminar stdout del MCP
    logger.warning("🐕 Iniciando servidor MCP FastMCP")
    mcp.run()