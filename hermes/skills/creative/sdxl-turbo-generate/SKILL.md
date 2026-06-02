---
title: SDXL-Turbo Image Generator
name: sdxl-turbo-generate
author: Hermes Agent
version: 1.0.0
description: Generate images instantly using SDXL-Turbo AI model
---

# SDXL-Turbo Image Generator

Genera imágenes a partir de descripciones de texto usando el modelo **SDXL-Turbo**, conocido por su velocidad (solo 1-2 segundos por imagen).

## Prerrequisitos

### Servicio SDXL-Turbo Local

El modelo debe estar ejecutándose como un servicio local en:
- **URL:** `http://localhost:7860` o `http://<hostname>:7860`
- **Endpoint:** `/generate` (accepts POST with JSON)

### Configuración del Servicio

Puedes ejecutar SDXL-Turbo con:

```bash
# Opción 1: Usar ComfyUI con SDXL-Turbo
docker run -p 7860:7860 \
  -v /opt/data/cache/images:/app/output \
  --gpus all \
  comfyui-sdxl-turbo

# Opción 2: Usar InvokeAI
docker run -p 7860:7860 \
  -v ./models:/invoke-ai/models \
  --gpus all \
  invokeai/sdxl-turbo
```

### Verificar el Servicio

```bash
curl -X POST http://localhost:7860/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test", "steps": 4, "width": 512, "height": 512}'
```

## Uso en Hermes

### Desde Chat (Automático)

Cuando describes lo que quieres generar, el skill se activa automáticamente:

```
Genera una imagen de "un gato astronauta en Marte"
```

### Parámetros de Configuración

Edita el script principal para ajustar:

| Parámetro | Valor por defecto | Descripción |
|------|---|----|
| `API_URL` | `http://localhost:7860` | Dirección del servicio |
| `WIDTH` | `512` | Ancho de la imagen |
| `HEIGHT` | `512` | Alto de la imagen |
| `STEPS` | `4` | Números de pasos (más rápido con menos pasos) |
| `OUTPUT_DIR` | `~/./cache/images` | Carpeta de salida |

### Ejemplos de Prompts

```
"un paisaje futurista con neón y coches voladores"
"retrato de un guerrero cyberpunk con implantes cibernéticos"
"un bosque encantado con hadas y mariposas luminosas en 4K"
"un robot retro holding a flower, vaporwave aesthetic"
"abstract art with geometric shapes and vibrant colors"
```

## Flujo de Ejecución

1. **Recibe prompt** del usuario
2. **Valida** el prompt (no vacío, longitud adecuada)
3. **Envía** a la API de SDXL-Turbo
4. **Guarda** la imagen en disco
5. **Muestra** la imagen con formato Markdown

## Troubleshooting

### Error: Connection refused

El servicio SDXL-Turbo no está ejecutándose:
```bash
# Verificar si el puerto está en uso
netstat -tuln | grep 7860
lsof -i :7860
```

### Error: Timeout (>120s)

El modelo está procesando lentamente o el servidor está caído:
- Reiniciar el servicio
- Verificar uso de GPU: `nvidia-smi`

### Error: Imagen corrupta

Base64 inválido o archivo incompleto:
- Verificar logs del servicio: `docker logs sdxl-turbo`
- Asegurar espacio en disco: `df -h`

### La imagen es borrosa

SDXL-Turbo es un modelo de difusión de 1 paso, usa más steps:
```python
"steps": 8  # en lugar de 4
```

## Integración Avanzada

### Usar desde Scripts Python

```python
import subprocess
import json

prompt = "input de tu prompt aquí"
result = subprocess.run([
    "hermes", "skill", "run", "sdxl-turbo-generate",
    "--prompt", prompt
], capture_output=True, text=True)

print(result.stdout)
```

### Usar desde Terminal

```bash
hermes run --skill sdxl-turbo-generate --prompt "tu descripción"
```

## Creditos

Este skill está basado en:
- [Open WebUI - SDXL-Turbo Tool](https://github.com/open-webui)
- [SDXL-Turbo by Stability AI](https://github.com/Stability-AI/SDXL-Turbo)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)