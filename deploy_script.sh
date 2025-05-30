#!/bin/bash


# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

set -e  # Salir si hay errores

# Limpiar imágenes anteriores
clean_old_images() {
    echo -e "${BLUE}🧹 Limpiando imágenes anteriores...${NC}"
    
    # Eliminar imagen local si existe
    if docker images | grep -q "$IMAGE_LOCAL"; then
        echo -e "${YELLOW}🗑️  Eliminando imagen local anterior: ${IMAGE_LOCAL}${NC}"
        docker rmi "$IMAGE_LOCAL" 2>/dev/null || true
    fi
    
    # Eliminar imágenes huérfanas y cache
    echo -e "${YELLOW}🗑️  Limpiando cache de Docker...${NC}"
    docker system prune -f >/dev/null 2>&1 || true
    
    echo -e "${GREEN}✅ Limpieza completada${NC}"
}

# Reconstruir imagen local siempre
# Esto garantiza que la imagen siempre tenga las últimas actualizaciones del código
check_local_image() {
    echo -e "${BLUE}🔨 Reconstruyendo imagen '${IMAGE_LOCAL}' desde cero...${NC}"
    echo -e "${YELLOW}⚡ Usando --no-cache para garantizar actualizaciones${NC}"
    
    if docker build --no-cache -t "$IMAGE_LOCAL" .; then
        echo -e "${GREEN}✅ Imagen reconstruida exitosamente con últimos cambios${NC}"
    else
        echo -e "${RED}❌ Error reconstruyendo la imagen${NC}"
        exit 1
    fi
}

echo -e "${BLUE}🚀 Script de Deploy MCP Server a GitHub Container Registry${NC}"
echo "================================================================"

# Variables - Se pueden configurar con variables de entorno
GITHUB_USERNAME="${GITHUB_USERNAME:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
REPO_NAME="${REPO_NAME:-mcp_amazon_affiliate}"
MCP_NAME="${MCP_NAME:-mcp_amazon_affiliate}"
IMAGE_LOCAL="${IMAGE_LOCAL:-mcp/${MCP_NAME}}"

echo -e "${BLUE}🔧 Configuración detectada:${NC}"
echo -e "   REPO_NAME: ${REPO_NAME}"
echo -e "   IMAGE_LOCAL: ${IMAGE_LOCAL}"
if [ -n "$GITHUB_USERNAME" ]; then
    echo -e "   GITHUB_USERNAME: ${GITHUB_USERNAME}"
fi
echo

# Función para solicitar datos si están vacíos
get_user_input() {
    if [ -z "$GITHUB_USERNAME" ]; then
        echo -e "${YELLOW}📝 Ingresa tu username de GitHub:${NC}"
        read -p "> " GITHUB_USERNAME
    else
        echo -e "${GREEN}✅ Username GitHub: ${GITHUB_USERNAME}${NC}"
    fi
    
    if [ -z "$GITHUB_TOKEN" ]; then
        echo -e "${YELLOW}🔑 Ingresa tu Personal Access Token:${NC}"
        read -s -p "> " GITHUB_TOKEN
        echo
    else
        echo -e "${GREEN}✅ Token GitHub configurado${NC}"
    fi
}

# Verificar Docker
check_docker() {
    echo -e "${BLUE}🔍 Verificando Docker...${NC}"
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no encontrado. Instálalo primero.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker encontrado${NC}"
}

# Verificar imagen local
# Esto se hace para asegurarnos de que la imagen local existe antes de intentar subirla
# Si no existe la creamos
check_local_image() {
    echo -e "${BLUE}🔍 Verificando imagen local '${IMAGE_LOCAL}'...${NC}"
    if ! docker images | grep -q "$IMAGE_LOCAL"; then
        echo -e "${YELLOW}⚠️ Imagen local '$IMAGE_LOCAL' no encontrada.${NC}"
        echo -e "${BLUE}� Construyendo imagen automáticamente...${NC}"
        
        if docker build --no-cache -t "$IMAGE_LOCAL" .; then
            echo -e "${GREEN}✅ Imagen construida exitosamente${NC}"
        else
            echo -e "${RED}❌ Error construyendo la imagen${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Imagen local encontrada${NC}"
    fi
}

# Login a GHCR
login_ghcr() {
    echo -e "${BLUE}🔐 Haciendo login a GitHub Container Registry...${NC}"
    echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Login exitoso${NC}"
    else
        echo -e "${RED}❌ Error en login. Verifica username y token${NC}"
        exit 1
    fi
}

# Etiquetar imagen
tag_image() {
    FULL_IMAGE_NAME="ghcr.io/${GITHUB_USERNAME}/${REPO_NAME}:latest"
    echo -e "${BLUE}🏷️  Etiquetando imagen como '${FULL_IMAGE_NAME}'...${NC}"
    
    docker tag "$IMAGE_LOCAL" "$FULL_IMAGE_NAME"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Imagen etiquetada${NC}"
    else
        echo -e "${RED}❌ Error etiquetando imagen${NC}"
        exit 1
    fi
}

# Subir imagen
push_image() {
    echo -e "${BLUE}📤 Subiendo imagen a GHCR...${NC}"
    docker push "$FULL_IMAGE_NAME"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Imagen subida exitosamente${NC}"
    else
        echo -e "${RED}❌ Error subiendo imagen${NC}"
        exit 1
    fi
}

# Generar configuración para empleados
generate_employee_config() {
    echo -e "${BLUE}📄 Generando configuración para empleados...${NC}"
    
    # JSON de configuración para empleados
    cat > ./DOC/claude_desktop_config.json << EOF
{
  "mcpServers": {
    "enterprise-server": {
      "command": "bash",
      "args": [
        "-c",
        "docker images | grep -q ${FULL_IMAGE_NAME} || docker pull ${FULL_IMAGE_NAME} >/dev/null 2>&1; docker run -i --rm --init -e DOCKER_CONTAINER=true ${FULL_IMAGE_NAME}"
      ]
    }
  }
}
EOF

    echo -e "${GREEN}✅ Archivo generado: claude_desktop_config.json${NC}"
}

# Mostrar información final
show_final_info() {
    echo
    echo -e "${GREEN}🎉 ¡Deploy completado exitosamente!${NC}"
    echo "================================================================"
    echo -e "${BLUE}📦 Imagen Docker:${NC} ${FULL_IMAGE_NAME}"
    echo -e "${BLUE}🌐 Para hacer pública:${NC} Ve a GitHub → Packages → ${REPO_NAME} → Settings → Change visibility → Public"
    echo
    echo -e "${YELLOW}📋 Archivo para empleados:${NC}"
    echo -e "${GREEN}claude_desktop_config.json${NC}"
    echo
    echo -e "${YELLOW}📝 Contenido del JSON:${NC}"
    cat ./DOC/claude_desktop_config.json
    echo
    echo -e "${YELLOW}📍 Los empleados deben copiarlo a:${NC}"
    echo "~/.config/claude-desktop/claude_desktop_config.json"
}

# Mostrar ayuda sobre variables de entorno
show_env_help() {
    echo -e "${YELLOW}💡 Variables de entorno disponibles:${NC}"
    echo "   GITHUB_USERNAME - Tu username de GitHub"
    echo "   GITHUB_TOKEN    - Tu Personal Access Token"
    echo "   REPO_NAME       - Nombre del repositorio (default: mcp_amazon_affiliate)"
    echo "   IMAGE_LOCAL     - Nombre de la imagen local (default: mcp/mcp_amazon_affiliate)"
    echo
    echo -e "${YELLOW}📝 Ejemplo de uso:${NC}"
    echo "   export GITHUB_USERNAME='mi-usuario'"
    echo "   export GITHUB_TOKEN='ghp_xxxxxxxxxxxx'"
    echo "   ./deploy-to-ghcr.sh"
    echo
}

# Verificar argumentos de ayuda
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_env_help
    exit 0
fi

# Ejecutar todo
main() {
    get_user_input
    check_docker
    clean_old_images
    check_local_image
    login_ghcr
    tag_image
    push_image
    generate_employee_config
    show_final_info
}

# Ejecutar script principal
main