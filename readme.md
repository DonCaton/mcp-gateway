# Remove and rebuild everything
docker-compose down
docker-compose up -d --build

# Restart a specific container
docker-compose restart mcpo

# Rebuild a specific container
docker-compose up -d --build mcpo

# View real-time logs
docker-compose logs -f mcpo

# Check resource usage
docker stats mcpo-gateway

# Test in powershell:

# Playwright
Invoke-RestMethod -Uri http://localhost:8000/playwright/openapi.json

# Memory
Invoke-RestMethod -Uri http://localhost:8000/memory/openapi.json

# Fetch
Invoke-RestMethod -Uri http://localhost:8000/fetch/openapi.json

# Filesystem
Invoke-RestMethod -Uri http://localhost:8000/filesystem/openapi.json

# GitHub
Invoke-RestMethod -Uri http://localhost:8000/github/openapi.json

# Example: Navigate (adjust path based on what you see in docs)

