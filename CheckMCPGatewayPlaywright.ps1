Write-Host "=== Connection Verification ===" -ForegroundColor Cyan

# 1. Check both containers are running
Write-Host "`n[1/4] Checking containers..." -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-String -Pattern "mcpo-gateway|open-webui"

# 2. Check network
Write-Host "`n[2/4] Checking network..." -ForegroundColor Yellow
docker network inspect mcp-network --format '{{range .Containers}}{{.Name}} {{end}}'

# 3. Test Open WebUI → MCP Gateway
Write-Host "`n[3/4] Testing Open WebUI → MCP Gateway..." -ForegroundColor Yellow
$test1 = docker exec open-webui curl -s -o /dev/null -w "%{http_code}" http://mcpo-gateway:8000/playwright/openapi.json
if ($test1 -eq "200") {
    Write-Host "✓ Open WebUI can reach MCP Gateway" -ForegroundColor Green
} else {
    Write-Host "✗ Failed (HTTP $test1)" -ForegroundColor Red
}

# 4. Test Open WebUI → Ollama (on Windows)
Write-Host "`n[4/4] Testing Open WebUI → Ollama..." -ForegroundColor Yellow
$test2 = docker exec open-webui curl -s -o /dev/null -w "%{http_code}" http://host.docker.internal:11434/api/tags
if ($test2 -eq "200") {
    Write-Host "✓ Open WebUI can reach Ollama on Windows" -ForegroundColor Green
} else {
    Write-Host "✗ Failed (HTTP $test2)" -ForegroundColor Red
}

Write-Host "`n=== Configuration ===" -ForegroundColor Cyan
Write-Host "In Open WebUI, configure tools with:" -ForegroundColor White
Write-Host "  URL: http://mcpo-gateway:8000/playwright" -ForegroundColor Yellow
Write-Host "  API Key: abracadabra" -ForegroundColor Yellow