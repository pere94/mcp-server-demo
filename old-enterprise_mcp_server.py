#!/usr/bin/env python3
"""
Servidor MCP Simple - Solo ladra como un perro
"""

import asyncio
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear servidor
server = Server("dog-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista las herramientas disponibles"""
    return [
        Tool(
            name="bark_like_dog",
            description="Ladra como un perro",
            inputSchema={
                "type": "object",
                "properties": {
                    "intensity": {
                        "type": "string",
                        "description": "Intensidad del ladrido: soft, normal, loud",
                        "enum": ["soft", "normal", "loud"],
                        "default": "normal"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="magic_tool",
            description="Suma 15 a un número dado",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {
                        "type": "number",
                        "description": "El número al que se le sumará 15"
                    }
                },
                "required": ["number"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Ejecuta una herramienta"""
    if name == "bark_like_dog":
        intensity = arguments.get("intensity", "normal")
        
        if intensity == "soft":
            bark = "woof woof 🐕"
        elif intensity == "loud":
            bark = "WOOF WOOF WOOF! 🐕‍🦺 BARK BARK!"
        else:  # normal
            bark = "Woof! Woof! 🐶"
        
        # Devolver como lista de TextContent
        return [TextContent(type="text", text=bark)]
        
    elif name == "magic_tool":
        try:
            number = arguments.get("number")
            if number is None:
                return [TextContent(type="text", text="Error: Se requiere el parámetro 'number'")]
            
            result = number + 15
            message = f"Resultado mágico: {number} + 15 = {result} ✨"
            
            return [TextContent(type="text", text=message)]
            
        except (TypeError, ValueError) as e:
            return [TextContent(type="text", text=f"Error: El parámetro debe ser un número válido. {str(e)}")]
    else:
        return [TextContent(type="text", text=f"Herramienta desconocida: {name}")]

async def main():
    """Función principal"""
    logger.info("🐕 Iniciando servidor MCP que ladra como un perro")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
