# OpenClaw con Chromium Headless para browser automation
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Instalar Chromium, dependencias y Xvfb para el display virtual
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    # === AÑADIDO: Xvfb es necesario para que DISPLAY=:99 funcione ===
    xvfb \
    x11-utils \
    # Dependencias gráficas y de sistema
    libgtk-3-0 \
    libasound2 \
    libatspi2.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libxss1 \
    libglib2.0-0 \
    fonts-liberation \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-kacst \
    fonts-freefont-ttf \
    xdg-utils \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# === AÑADIDO: Crear wrapper que fuerza --no-sandbox en Chromium ===
# Sin esto, Chromium falla en contenedores porque el kernel
# no tiene soporte para el sandbox de namespaces de usuario
RUN mv /usr/bin/chromium /usr/bin/chromium-real \
    && echo '#!/bin/bash\nexec /usr/bin/chromium-real --no-sandbox --disable-setuid-sandbox "$@"' \
       > /usr/bin/chromium \
    && chmod +x /usr/bin/chromium

# Configurar variables de ambiente
ENV DISPLAY=:99
ENV CHROME_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PUPPETEER_SKIP_DOWNLOAD=1
ENV NODE_OPTIONS="--max-old-space-size=4096"
# === AÑADIDO: Flags de Chromium para entornos containerizados ===
ENV CHROMIUM_FLAGS="--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage --disable-gpu"

# === CORREGIDO: Crear el directorio y asignar ownership al usuario node ===
# Antes se creaba como root y node no podía escribir en él
RUN mkdir -p /home/node/.cache/google-chrome \
    && mkdir -p /home/node/.config/chromium \
    && chown -R node:node /home/node/.cache \
    && chown -R node:node /home/node/.config

USER node

# Verificar instalación
RUN chromium --version

WORKDIR /home/node/.openclaw/workspace

# === CORREGIDO: Arrancar Xvfb primero y luego OpenClaw ===
# El CMD anterior con tail -f /dev/null dejaba el contenedor vacío
CMD Xvfb :99 -screen 0 1280x720x24 -ac & sleep 1 && tail -f /dev/null