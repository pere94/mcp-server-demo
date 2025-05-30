"""
Ejemplo de uso de la biblioteca mejorada de Amazon PA-API.
Demuestra las nuevas funcionalidades y mejoras implementadas.
"""

import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from libs.amazon import AmazonAPISingleton


def example_search_items():
    """Ejemplo básico de uso del API de Amazon."""
    print("🚀 Ejemplo básico de uso de la biblioteca Amazon PA-API mejorada")
    print("=" * 70)
    
    try:
        # Crear instancia (singleton)
        amazon_client = AmazonAPISingleton.get_instance()
        print("✅ Cliente Amazon PA-API inicializado correctamente")
        
        # Ejemplo 1: Búsqueda básica
        print("\n📱 Ejemplo 1: Búsqueda de productos inteligentes...")
        response = amazon_client.search_items(
            keywords="smart home devices",
        )
        
        print("🔍 Resultados de búsqueda: \n", response[0])
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {str(e)}")
        print("\n💡 Asegúrate de:")
        print("   1. Tener configuradas las variables de entorno de Amazon")
        print("   2. Verificar las credenciales en el archivo .env")
        print("   3. Comprobar la conectividad a internet")

def example_get_items():
    """Ejemplo de obtención de detalles de productos."""
    print("\n📦 Ejemplo 2: Obtención de detalles de productos...")
    
    try:
        amazon_client = AmazonAPISingleton.get_instance()
        item_asins = ["B0CNPQWZB4"]  # IDs de ejemplo
        response = amazon_client.get_items(item_asins=item_asins)
        
        print("🔍 Detalles de productos: \n", response)
        
    except Exception as e:
        print(f"❌ Error al obtener detalles de productos: {str(e)}")

if __name__ == "__main__":
    # Ejecutar el ejemplo básico
    # example_search_items()
    example_get_items()