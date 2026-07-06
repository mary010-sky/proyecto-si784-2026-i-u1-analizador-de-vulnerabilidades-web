import asyncio
import os
import sys

# Asegurar que encuentre el modulo server.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuramos la variable de entorno para la prueba ANTES de importar el server
os.environ["WVS_API_KEY"] = "test-key"

from server import scan_vulnerabilities

async def probar_escaneo(url):
    print(f"Iniciando escaneo de prueba hacia {url} ...")
    try:
        # Llamamos directamente a la función de la skill
        resultado = await scan_vulnerabilities(url, depth=1)
        
        print("\n================ RESULTADO DEL ESCANEO ================")
        print(resultado)
        print("=======================================================")
    except Exception as e:
        print(f"\nError durante la prueba: {e}")

# Ejecutamos la prueba asíncrona
if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("Ingresa la URL a escanear (ej. http://testphp.vulnweb.com): ")
        if not target_url.strip():
            print("URL inválida.")
            sys.exit(1)
            
    asyncio.run(probar_escaneo(target_url))
