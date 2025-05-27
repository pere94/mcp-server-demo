#!/usr/bin/env python3
"""
Servidor MCP Simple con FastMCP - Solo ladra como un perro
"""

import logging
from mcp.server.fastmcp import FastMCP

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear servidor FastMCP
mcp = FastMCP("dog-server")

@mcp.tool()
async def bark_like_dog(intensity: str = "normal") -> str:
    """
    Ladra como un perro
    
    Args:
        intensity: Intensidad del ladrido (soft, normal, loud)
    """
    logger.info(f"🐕 Ladrando con intensidad: {intensity}")
    
    if intensity == "soft":
        return "woof woof 🐕"
    elif intensity == "loud":
        return "WOOF WOOF WOOF! 🐕‍🦺 BARK BARK!"
    else:  # normal
        return "Woof! Woof! 🐶"

@mcp.tool()
async def magic_tool(number: float) -> str:
    """
    Suma 15 a un número dado
    
    Args:
        number: El número al que se le sumará 15
    """
    try:
        result = number + 15
        message = f"Resultado mágico: {number} + 15 = {result} ✨"
        logger.info(f"🪄 Operación mágica: {message}")
        return message
        
    except (TypeError, ValueError) as e:
        error_msg = f"Error: El parámetro debe ser un número válido. {str(e)}"
        logger.error(error_msg)
        return error_msg

if __name__ == "__main__":
    logger.info("🐕 Iniciando servidor MCP FastMCP que ladra como un perro")
    mcp.run()