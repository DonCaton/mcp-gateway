FROM ghcr.io/open-webui/mcpo:main

# Install Node.js and system dependencies
RUN apt-get update && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs xvfb && \
    rm -rf /var/lib/apt/lists/*

# Install uv for Python MCP servers
RUN pip install uv

# Install Playwright and ALL browsers (including chrome)
RUN npx -y @playwright/mcp@latest --help && \
    npx playwright install chrome chromium firefox webkit --with-deps

WORKDIR /app

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Xvfb..."\n\
rm -f /tmp/.X99-lock\n\
Xvfb :99 -screen 0 1920x1080x24 &\n\
sleep 3\n\
echo "Starting MCPO..."\n\
export DISPLAY=:99\n\
exec mcpo --config /app/config/config.json\n\
' > /app/start.sh && chmod +x /app/start.sh

# Override ENTRYPOINT and use our startup script
ENTRYPOINT []
CMD ["/app/start.sh"]