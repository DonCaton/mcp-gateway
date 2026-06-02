# Cómo Usar SDXL-Turbo en Hermes Agent

## 🚀 Instalación Rápida

```bash
# 1. Ejecutar script de instalación
cd ~/./skills/creative/sdxl-turbo-generate
bash scripts/install.sh
```

Este script:
- ✓ Verifica Docker y GPU NVIDIA
- ✓ Descarga y inicia el servicio SDXL-Turbo
- ✓ Configura variables de ambiente
- ✓ Prueba la conexión con la API

## 📸 Generar Imágenes

### Opción 1: Desde el Chat de Hermes

Simplemente describe lo que quieres:

```
Genera una imagen de "un gato astronauta flotando en el espacio"
```

### Opción 2: Usando Terminal

```bash
# Formo directo
bash ~/./skills/creative/sdxl-turbo-generate/scripts/install.sh
python3 ~/./skills/creative/sdxl-turbo-generate/scripts/generate_image.py "tu prompt aquí"

# O usando python desde script
python3 ~/./skills/creative/sdxl-turbo-generate/scripts/generate_image.py "un paisaje cyberpunk futurista"
```

### Opción 3: Usando API desde Python

```python
import asyncio
from skills.creative.sdxl_turbo_generate.scripts.generate_image import generate_image

async def main():
    result = await generate_image("un castillo medieval al atardecer")
    print(result)

asyncio.run(main())
```

## ⚙️ Configuración

### Variables de Ambiente

```bash
# URL del servicio (puerto por defecto)
export SDXL_TURBO_URL="http://localhost:7860"

# Resolución de la imagen (por defecto 512x512)
export SDXL_WIDTH=512
export SDXL_HEIGHT=512

# Números de pasos de generación (más = mejor calidad, más lento)
export SDXL_STEPS=4

# Directorio de salida
export IMAGE_OUTPUT_DIR="$HOME/.hermes/cache/images"
```

### Agregar a .bashrc

```bash
echo 'export SDXL_TURBO_URL="http://localhost:7860"' >> ~/.bashrc
echo 'export SDXL_WIDTH=512' >> ~/.bashrc
echo 'export SDXL_HEIGHT=512' >> ~/.bashrc
echo 'export SDXL_STEPS=4' >> ~/.bashrc
source ~/.bashrc
```

## 🎨 Ejemplos de Prompts

### Paisajes
```
"un atardecer en Marte con nubes rosadas en 4K ultra detallado"
"un bosque encantado con hadas y luces de hadas nocturnas"
"una ciudad futurista cyberpunk con neón y lluvia"
```

### Retratos
```
"retrato de un guerrero cibernético con implantes brillantes"
"una mujer alienígena con ojos grandes en una nave espacial"
"un dragón ancestral volando sobre montañas nubosas"
```

### Abstracto
```
"arte abstracto geométrico con formas vibrantes y colores neón"
"explosión de partículas cósmicas en el espacio exterior"
"fractales matemáticos con paleta de colores vibrante"
```

### Estilo Artístico
```
"pintura al óleo de Van Gogh de un campo de girasoles en Marte"
"grabado en madera de un samurai japonés en estilo medieval"
"fotografía realista de un robot retro futurista por Blade Runner"
```

## 🔧 Troubleshooting

### Problema: "No se puede conectar a localhost:7860"

**Solución:** El servicio no está corriendo

```bash
# Verificar si Docker está corriendo
docker ps

# Verificar el servicio SDXL-Turbo
docker ps | grep sdxl

# Si no está, iniciar de nuevo
bash ~/./skills/creative/sdxl-turbo-generate/scripts/install.sh
```

### Problema: Imágenes borrosas o de baja calidad

**Solución:** Aumenta los steps o la resolución

```bash
export SDXL_STEPS=8
export SDXL_WIDTH=768
export SDXL_HEIGHT=768
```

### Problema: Error de GPU o "CUDA out of memory"

**Solución:** Verificar GPU disponible

```bash
# Verificar GPU
nvidia-smi

# Verificar uso de memoria del contenedor
docker stats sdxl-turbo

# Reducir resolución si es necesario
export SDXL_WIDTH=512
export SDXL_HEIGHT=512
```

### Problema: Lento (tarda mucho en generar)

**Verifica si está usando CPU en vez de GPU:**

```bash
# Verificar si container está usando GPU
docker inspect sdxl-turbo | grep -i nvidia

# Verificar logs del service
docker logs sdxl-turbo

# Ver recursos usados
docker stats sdxl-turbo
```

## 📁 Estructura del Skill

```
~/./skills/creative/sdxl-turbo-generate/
├── SKILL.md                 # Documentación del skill
├── scripts/
│   ├── generate_image.py    # Script principal de generación
│   └── install.sh           # Script de instalación
└── references/
    └── README.md           # Este archivo
```

## 🐳 Gestión del Servicio

### Iniciar Manualmente

```bash
docker run -d \
  --name sdxl-turbo \
  --gpus all \
  -p 7860:8188 \
  -v ~/./cache/sdxl-turbo:/output \
  ghcr.io/comfyanonymous/comfyui:latest
```

### Detener Servicio

```bash
docker stop sdxl-turbo
```

### Reiniciar Servicio

```bash
docker restart sdxl-turbo
```

### Eliminar Servicio

```bash
docker stop sdxl-turbo && docker rm sdxl-turbo
```

### Ver Logs del Servicio

```bash
docker logs -f sdxl-turbo
```

## 🎯 Parámetros Avanzados (Experimental)

### Modelos Personalizados

```bash
# Cambiar modelo (requiere cargar en el service)
export SDXL_MODEL="stable-diffusion-xl-base-1.0"
```

### Configurar Seed (para reproducibilidad)

```python
# En el script generate_image.py, agrega:
payload = {
    "prompt": prompt,
    "steps": self.steps,
    "width": self.width,
    "height": self.height,
    "seed": 12345  # Seed fijo para imágenes consistentes
}
```

### Configurar CFG Scale (creatividad vs fidelidad)

```python
payload = {
    "prompt": prompt,
    "steps": self.steps,
    "width": self.width,
    "height": self.height,
    "cfg_scale": 7.0  # Mayor = más fiel al prompt
}
```

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs:** `docker logs sdxl-turbo`
2. **Verifica GPU:** `nvidia-smi`
3. **Prueba la API:** `curl http://localhost:7860/generate`
4. **Lee la documentación:** Ver SKILL.md

## 🙏 Créditos

- **SDXL-Turbo:** https://github.com/Stability-AI/SDXL-Turbo
- **ComfyUI:** https://github.com/comfyanonymous/ComfyUI
- **Original Concept:** Open WebUI Community Tools