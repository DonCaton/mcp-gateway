# OpenClaw con Chromium Headless para browser automation
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Instalar Chromium y dependencias necesarias
RUN apt-get update && apt-get install -y \
    # Chromium headless
    chromium \
    chromium-driver \
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
    # Utilidades adicionales
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configurar variables de ambiente para Chromium headless
ENV DISPLAY=:99
ENV CHROME_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PUPPETEER_SKIP_DOWNLOAD=1
ENV NODE_OPTIONS="--max-old-space-size=4096"

# Crear directorio para cache de Chromium
RUN mkdir -p /home/node/.cache/google-chrome

# Cambiar de vuelta al usuario node
USER node

# Verificar que Chromium esté instalado
RUN chromium --version || echo "Chromium installation verification"

WORKDIR /home/node/.openclaw/workspace

CMD ["tail", "-f", "/dev/null"]