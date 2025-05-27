# 🚀 Servidor MCP Empresarial

Servidor MCP centralizado que funciona vía Docker + SSH. **Todos los empleados conectan sus Claude Desktop al mismo servidor** sin instalar nada.

## 🔑 Información de Conexión del Servidor

**🖥️ SSH del Servidor:**
- **Host:** localhost  
- **Puerto:** 2222
- **Usuario:** mcpuser
- **Contraseña:** mcppass
- **Comando completo:** `ssh mcpuser@localhost -p 2222`

---

## ⚡ Para Empleados

**Solo necesitas hacer esto UNA vez:**

1. Lee `SETUP_GUIDE.md`
2. Copia la configuración JSON 
3. Pégala en Claude Desktop
4. ¡Listo!

## 🏗️ Arquitectura

```
Claude Desktop (Empleado) ──SSH──► Docker Container (Servidor Empresa)
Claude Desktop (Empleado) ──SSH──► Docker Container (Servidor Empresa)  
Claude Desktop (Empleado) ──SSH──► Docker Container (Servidor Empresa)
```

- **Empleados**: Solo configuran Claude Desktop
- **Servidor**: Todo centralizado en Docker
- **Sin instalaciones**: Nada que instalar localmente

## 🛠️ Para Administradores

```bash
# Desplegar servidor (solo una vez)
./deploy.sh

# Verificar que funciona
./verify_deployment.sh
```

## 🎯 Herramientas Disponibles

- **👥 Usuarios**: Crear, consultar, actualizar, eliminar
- **📊 Proyectos**: Gestión completa de proyectos
- **📁 Archivos**: Operaciones de archivos
- **🏢 Empresariales**: Reportes, notificaciones, backups, auditorías

## 📁 Archivos Importantes

- **`SETUP_GUIDE.md`** - Instrucciones para empleados
- **`claude_desktop_config_final.json`** - Configuración para copiar
- **`deploy.sh`** - Despliega el servidor
- **`verify_deployment.sh`** - Verifica que funciona

## 🆘 Problemas?

- **Container no funciona?** → `./verify_deployment.sh`
- **Claude no conecta?** → Revisar `SETUP_GUIDE.md`

---
**Todo configurado y listo para usar** ✅