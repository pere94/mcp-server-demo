# Dockerfile optimizado para Claude Desktop MCP
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos esenciales
COPY enterprise_mcp_server.py pyproject.toml ./

# Instalar dependencias MCP
RUN pip install --no-cache-dir mcp pydantic click

# Crear directorios para datos
RUN mkdir -p /app/data /app/tools

# Variables de entorno para MCP
ENV PYTHONUNBUFFERED=1
ENV MCP_DOCKER_MODE=true

# Comando por defecto - ejecutar el servidor MCP usando stdio para Claude Desktop
CMD ["python", "-u", "enterprise_mcp_server.py"]
