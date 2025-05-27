# � Dog MCP Server - FastMCP Edition

Servidor MCP simple y divertido construido con **FastMCP** que permite a Claude ladrar como un perro y hacer operaciones mágicas. ¡Perfecto para startups que buscan rapidez y simplicidad!

## � Características

- **🐶 Ladridos de perro** con diferentes intensidades
- **🪄 Operaciones mágicas** (suma 15 a cualquier número)
- **⚡ FastMCP** - Configuración simplificada
- **🐳 Docker Ready** - Containerizado y listo para producción
- **📝 Logging completo** para debugging

## 🏗️ Arquitectura

```
Claude Desktop ──stdio──► FastMCP Server ──Docker──► Production
```

- **FastMCP**: Framework simplificado para MCP
- **Herramientas**: Decoradores `@mcp.tool()` automáticos
- **Transporte**: stdio automático (sin configuración manual)

## ⚡ Instalación Rápida

### Desarrollo Local

```bash
# 1. Instalar dependencias
pip install mcp

# 2. Ejecutar servidor
python enterprise_mcp_server.py

# 3. Configurar Claude Desktop
# Copia el JSON de configuración a tu Claude Desktop
```

### Con Docker (Recomendado para producción)

```bash
# 1. Usar script automatizado (Recomendado)
chmod +x build_docker.sh
./build_docker.sh

# 2. O manualmente
docker build -t dog-mcp-server .
docker run --rm dog-mcp-server

# 3. Con docker-compose
docker-compose up -d
```

## 🎯 Herramientas Disponibles

### � `bark_like_dog`
Hace que el servidor ladre como un perro con diferentes intensidades.

**Parámetros:**
- `intensity` (string): "soft", "normal", "loud"

**Ejemplos:**
- `intensity: "soft"` → "woof woof 🐕"
- `intensity: "normal"` → "Woof! Woof! 🐶"
- `intensity: "loud"` → "WOOF WOOF WOOF! 🐕‍🦺 BARK BARK!"

### 🪄 `magic_tool`
Suma 15 a cualquier número de forma "mágica".

**Parámetros:**
- `number` (float): El número al que se le sumará 15

**Ejemplo:**
- `number: 25` → "Resultado mágico: 25 + 15 = 40 ✨"

## � Configuración Claude Desktop

Agrega esta configuración a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dog-server": {
      "command": "python",
      "args": ["/ruta/absoluta/a/enterprise_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/ruta/absoluta/a/tu/proyecto"
      }
    }
  }
}
```

## 📁 Estructura del Proyecto

```
mcp-server-demo/
├── enterprise_mcp_server.py    # 🐕 Servidor principal (FastMCP)
├── old-enterprise_mcp_server.py # 📜 Versión anterior (manual)
├── build_docker.sh             # 🐳 Script de construcción Docker
├── Dockerfile                   # 🐳 Configuración Docker
├── docker-compose.yml          # 🚀 Docker Compose
├── pyproject.toml              # 📦 Configuración del proyecto
├── uv.lock                     # 🔒 Lock de dependencias
├── claude_desktop_config.json  # ⚙️ Configuración Claude
└── README.md                   # 📖 Esta documentación
```

## 💻 Desarrollo

### Código FastMCP (Actual)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dog-server")

@mcp.tool()
async def bark_like_dog(intensity: str = "normal") -> str:
    """Ladra como un perro"""
    if intensity == "soft":
        return "woof woof 🐕"
    elif intensity == "loud":
        return "WOOF WOOF WOOF! 🐕‍🦺"
    else:
        return "Woof! Woof! 🐶"

if __name__ == "__main__":
    mcp.run()
```

### Ventajas de FastMCP

- ✅ **50% menos código** que configuración manual
- ✅ **Decoradores simples** `@mcp.tool()`
- ✅ **Manejo automático** de transporte y esquemas
- ✅ **Type hints automáticos** para validación
- ✅ **Perfecto para startups** - desarrollo rápido

## 🛠️ Scripts Disponibles

### � Build Docker (Automatizado)

```bash
# Script principal para Docker
chmod +x build_docker.sh
./build_docker.sh
```

**El script `build_docker.sh` hace:**
- ✅ Construye la imagen Docker automáticamente
- ✅ Tagea con versión y `latest`
- ✅ Ejecuta tests básicos de la imagen
- ✅ Muestra información de la imagen creada
- ✅ Opciones para push a registry

### 🚀 Deploy y Testing

```bash
# Crear script de despliegue personalizado
chmod +x deploy.sh && ./deploy.sh

# Test local directo
python enterprise_mcp_server.py
```

### 🐳 Docker Commands

```bash
# Usar script automatizado (Recomendado)
./build_docker.sh

# Desarrollo con compose
docker-compose up -d

# Producción directa
docker run --rm dog-mcp-server

# Ver logs
docker logs dog-mcp-server

# Rebuild completo
./build_docker.sh --clean
```

## 🆘 Troubleshooting

### Problemas Comunes

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'mcp'` | `pip install mcp` |
| Claude no conecta | Verificar ruta absoluta en config |
| Docker no inicia | `docker-compose logs` |
| Puerto ocupado | Cambiar puerto en docker-compose.yml |

### Debug Mode

```bash
# Logs detallados
export LOG_LEVEL=DEBUG
python enterprise_mcp_server.py

# O en Docker
docker run -e LOG_LEVEL=DEBUG dog-mcp-server
```

## 📚 Recursos

- **[MCP Documentation](https://docs.mcp.dev)** - Documentación oficial
- **[FastMCP Guide](https://docs.mcp.dev/quickstart/fastmcp)** - Guía FastMCP
- **[Claude Desktop Setup](https://docs.anthropic.com/claude/docs/mcp-setup)** - Configuración Claude

---

**🎉 ¡Servidor MCP listo para tu startup!** 

*Construido con ❤️ usando FastMCP - La forma más rápida de crear servidores MCP*