#!/bin/bash

MCP_NAME="${MCP_NAME:-mcp_amazon_affiliate}"

echo "🧪 Probando servidor MCP empresarial en Docker..."

# Verificar que Docker está disponible
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Construir la imagen si no existe
echo "🔨 Construyendo imagen Docker..."
docker build -t mcp/${MCP_NAME} .

if [ $? -eq 0 ]; then
    echo "✅ Imagen construida exitosamente"
else
    echo "❌ Error construyendo la imagen"
    exit 1
fi

# Probar el contenedor (debe responder a stdin/stdout)
echo "🧪 Probando comunicación MCP..."
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | docker run -i --rm mcp/${MCP_NAME} mcp-server

echo ""
echo "📋 Configuración para Claude Desktop:"
echo "-------------------------------------"
cat ./DOC/claude_desktop_config.json

echo ""
echo "🎉 ¡Listo! Copia el contenido de claude_desktop_config.json a tu configuración de Claude Desktop"
