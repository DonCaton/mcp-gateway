#!/usr/bin/env python3
"""
SDXL-Turbo Image Generator for Hermes Agent
Generates images from text prompts using local SDXL-Turbo API
"""

import os
import sys
import json
import base64
from datetime import datetime
from pathlib import Path

try:
    import httpx
except ImportError:
    print("❌ Error: httpx no está instalado. Instalando...")
    os.system("pip install httpx aiohttp")
    import httpx


class SDXLTurboGenerator:
    """Generador de imágenes con SDXL-Turbo"""
    
    def __init__(self):
        # Configuración
        self.api_url = os.environ.get("SDXL_TURBO_URL", "http://sdxl-turbo:7860")
        self.model_name = "sdxl-turbo"
        self.width = int(os.environ.get("SDXL_WIDTH", "512"))
        self.height = int(os.environ.get("SDXL_HEIGHT", "512"))
        self.steps = int(os.environ.get("SDXL_STEPS", "4"))
        
        # Directorio de salida
        self.output_dir = Path(os.environ.get("IMAGE_OUTPUT_DIR", os.path.expanduser("~/./cache/images")))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_image(self, prompt: str) -> str:
        """
        Genera una imagen desde un prompt usando SDXL-Turbo
        
        Args:
            prompt: Descripción de texto de la imagen a generar
            
        Returns:
            Ruta del archivo de imagen generado o mensaje de error
        """
        print(f"🎨 Generando imagen con prompt: '{prompt[:50]}...'")
        
        try:
            # Construir la petición
            payload = {
                "prompt": prompt,
                "steps": self.steps,
                "width": self.width,
                "height": self.height,
                "model": self.model_name
            }
            
            print(f"📡 Enviando petición a {self.api_url}/generate")
            
            # Hacer request a la API
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.api_url}/generate",
                    json=payload
                )
                
                if response.status_code != 200:
                    raise Exception(f"Error de API: {response.status_code} - {response.text}")
                
                data = response.json()
                
                # Extraer imagen base64
                if "image" not in data:
                    raise Exception(f"Respuesta inválida: {data}")
                
                b64_image = data["image"]
                
                # Guardar imagen en disco
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"img_{timestamp}.png"
                filepath = self.output_dir / filename
                
                # Decodificar base64 y guardar
                image_bytes = base64.b64decode(b64_image)
                filepath.write_bytes(image_bytes)
                
                print(f"✨ Imagen guardada en: {filepath}")
                
                # Retornar formato Markdown para Telegram
                return f"### 🖼️ Imagen Generada\n\n![Generada con SDXL-Turbo](file://{filepath.absolute()})\n\n*Guardada en:* `{filepath.absolute()}`"
                
        except httpx.ConnectError as e:
            error_msg = f"❌ Error de conexión: No se puede conectar a {self.api_url}/generate\n\n🔧 Verifica que el servicio SDXL-Turbo esté ejecutándose.\n   Ejecuta: `docker ps | grep sdxl`"
            print(error_msg)
            return error_msg
            
        except httpx.TimeoutException:
            error_msg = "❌ Error: Tiempo de espera excedido (>120s)\n\n🔧 El servicio está tarde. Verifica: `docker logs sdxl-turbo`"
            print(error_msg)
            return error_msg
            
        except Exception as e:
            error_msg = f"❌ Error al generar imagen: {str(e)}"
            print(error_msg)
            return error_msg


# Función principal para usar desde Hermes
async def generate_image(prompt: str, output_dir: str = None) -> str:
    """
    Función principal para generar imágenes
    
    Args:
        prompt: Descripción de la imagen
        output_dir: Directorio de salida opcional
        
    Returns:
        Markdown con la imagen o mensaje de error
    """
    generator = SDXLTurboGenerator()
    
    if output_dir:
        generator.output_dir = Path(output_dir)
    
    return await generator.generate_image(prompt)


# Si se ejecuta como script standalone
if __name__ == "__main__":
    import asyncio
    
    # Ejemplo de uso
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "a futuristic cyberpunk city with neon lights in 4K"
    
    result = asyncio.run(generate_image(prompt))
    print(result)