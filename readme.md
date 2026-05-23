# WEBUI with an MCP-Gateway that links to MCP server Playwright

# RUNNING OLLAMA Server

set OLLAMA_VULKAN=1
set OLLAMA_SCHED_SPREAD=1
set OLLAMA_DEBUG=1
c:\ollama serve
And in web ui set up context: 
set parameter num_ctx to 32768 in general advanced config 

# For MCP Gateway solution created with Claude

## Open WEB UI Standard standalone container installation (standalone, do not run if you use docker-compose.yml)
docker run -d ` -p 3000:8080 ` --add-host=host.docker.internal:host-gateway ` -v open-webui:/app/backend/data ` --name open-webui ` --restart always ` --network mcp-network ` ghcr.io/open-webui/open-webui:main

## Remove and rebuild everything
docker-compose down
docker-compose up -d --build
docker compose down -v   # borra volúmenes
docker rm ollama-webui   # elimina el container

# Ver si Ollama detecta la GPU
docker exec ollama-webui ollama run --help

# Ver nvidia-smi dentro del container
docker exec ollama-webui nvidia-smi

# Ver logs de Ollama buscando menciones a GPU/CUDA
docker logs ollama-webui 2>&1 | findstr -i "cuda\|gpu\|nvidia"

## Restart a specific container
docker-compose restart mcpo

## Rebuild a specific container
docker-compose up -d --build mcpo

## View real-time logs
docker-compose logs -f mcpo
docker logs mcpo-gateway -f

## Check resource usage
docker stats mcpo-gateway

# Test in powershell:
## AUTH BEARER
abracadabra

## Playwright
Invoke-RestMethod -Uri http://localhost:8000/playwright/openapi.json
http://host.docker.internal:8000/playwright
http://mcpo-gateway:8000/playwright

## Memory
Invoke-RestMethod -Uri http://localhost:8000/memory/openapi.json
http://host.docker.internal:8000/memory
http://mcpo-gateway:8000/memory

## Fetch
Invoke-RestMethod -Uri http://localhost:8000/fetch/openapi.json
http://host.docker.internal:8000/fetch
http://mcpo-gateway:8000/fetch

## Filesystem
Invoke-RestMethod -Uri http://localhost:8000/filesystem/openapi.json
http://host.docker.internal:8000/filesystem
http://mcpo-gateway:8000/filesystem

## GitHub
Invoke-RestMethod -Uri http://localhost:8000/github/openapi.json
http://host.docker.internal:8000/github
http://mcpo-gateway:8000/github

## Example: Navigate (adjust path based on what you see in docs)

# PROBANDO PLAYWRIGHT MCP Server Gateway por PowerShell

## 1. Create the Script File

Open Notepad or your preferred text editor.
Paste the code you provided into the editor.
Save the file with a .ps1 extension. For example: check_playwright.ps1.
Tip: Save it to a folder that is easy to access, such as C:\scripts\.

## 2. Create an "Easy" Alias (Optional but Recommended)
To run the script by simply typing a short command (like pwcheck) instead of the full path, create a batch wrapper:
Open a new Notepad file.
Paste the following line, replacing the path with your script's location:
batch
@powershell -ExecutionPolicy Bypass -File "C:\scripts\check_playwright.ps1"

Save this file as pwcheck.bat in a folder that is in your System PATH (like C:\Windows\).

## 3. RUN Script:
powershell -ExecutionPolicy Bypass -File "C:\scripts\check_playwright.ps1"

## QUICK STATUS Check
Write-Host "=== Playwright Tools Status ===" -ForegroundColor Cyan

$tools = @(
    "browser_navigate",
    "browser_snapshot", 
    "browser_take_screenshot",
    "browser_click",
    "browser_close"
)

foreach ($tool in $tools) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/playwright/$tool" `
            -Method Options `
            -ErrorAction Stop
        Write-Host "✓ $tool - Available" -ForegroundColor Green
    } catch {
        Write-Host "✗ $tool - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

## 1 Navigate to a Website
$body = @{
    url = "https://example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_navigate" ` -Method Post ` -Body $body ` -ContentType "application/json"
## 2 Take a Snapshot (Get Page Content)
$body = @{} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_snapshot" ` -Method Post ` -Body $body ` -ContentType "application/json"
## 3 Take a Screenshot
$body = @{
    type = "png"
    filename = "test-screenshot.png"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_take_screenshot" ` -Method Post ` -Body $body ` -ContentType "application/json"
## 4. First Navigate then CLIC an element
### Navigate
$navBody = @{
    url = "https://example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_navigate" `
    -Method Post `
    -Body $navBody `
    -ContentType "application/json"

### Get snapshot to find elements
$snapBody = @{} | ConvertTo-Json

$snapshot = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_snapshot" `
    -Method Post `
    -Body $snapBody `
    -ContentType "application/json"

### Display snapshot to see available elements
$snapshot
## 5. Full Workflow Test
Write-Host "=== Playwright Full Workflow Test ===" -ForegroundColor Cyan

### Step 1: Navigate
Write-Host "`n[1/4] Navigating to example.com..." -ForegroundColor Yellow
try {
    $nav = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_navigate" `
        -Method Post `
        -Body (@{url="https://example.com"} | ConvertTo-Json) `
        -ContentType "application/json"
    Write-Host "✓ Navigation successful" -ForegroundColor Green
    $nav | ConvertTo-Json
} catch {
    Write-Host "✗ Navigation failed: $_" -ForegroundColor Red
    exit
}

Start-Sleep -Seconds 2

### Step 2: Get snapshot
Write-Host "`n[2/4] Getting page snapshot..." -ForegroundColor Yellow
try {
    $snapshot = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_snapshot" `
        -Method Post `
        -Body (@{} | ConvertTo-Json) `
        -ContentType "application/json"
    Write-Host "✓ Snapshot retrieved" -ForegroundColor Green
    Write-Host "Content preview:" -ForegroundColor White
    $snapshot.content[0] | ConvertTo-Json | Select-Object -First 500
} catch {
    Write-Host "✗ Snapshot failed: $_" -ForegroundColor Red
}

### Step 3: Take screenshot
Write-Host "`n[3/4] Taking screenshot..." -ForegroundColor Yellow
try {
    $screenshot = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_take_screenshot" `
        -Method Post `
        -Body (@{type="png"; filename="test.png"} | ConvertTo-Json) `
        -ContentType "application/json"
    Write-Host "✓ Screenshot taken" -ForegroundColor Green
    $screenshot | ConvertTo-Json
} catch {
    Write-Host "✗ Screenshot failed: $_" -ForegroundColor Red
}

### Step 4: Close browser
Write-Host "`n[4/4] Closing browser..." -ForegroundColor Yellow
try {
    $close = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_close" `
        -Method Post `
        -Body (@{} | ConvertTo-Json) `
        -ContentType "application/json"
    Write-Host "✓ Browser closed" -ForegroundColor Green
} catch {
    Write-Host "✗ Close failed: $_" -ForegroundColor Red
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan
## 6. Navigate to a complex site
### Navigate to Wikipedia
$body = @{
    url = "https://www.wikipedia.org"
} | ConvertTo-Json

Write-Host "Navigating to Wikipedia..." -ForegroundColor Yellow
$result = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_navigate" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$result | ConvertTo-Json

### Get the page content
Write-Host "`nGetting page snapshot..." -ForegroundColor Yellow
$snapshot = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_snapshot" `
    -Method Post `
    -Body (@{} | ConvertTo-Json) `
    -ContentType "application/json"

### Display first 1000 characters
Write-Host "`nPage Content (first 1000 chars):" -ForegroundColor Cyan
($snapshot | ConvertTo-Json -Depth 5).Substring(0, [Math]::Min(1000, ($snapshot | ConvertTo-Json -Depth 5).Length))
## 7 FORM Interaction
### Navigate to a site with forms
$nav = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_navigate" `
    -Method Post `
    -Body (@{url="https://www.google.com"} | ConvertTo-Json) `
    -ContentType "application/json"

Start-Sleep -Seconds 2

### Get snapshot to find form elements
$snapshot = Invoke-RestMethod -Uri "http://localhost:8000/playwright/browser_snapshot" `
    -Method Post `
    -Body (@{} | ConvertTo-Json) `
    -ContentType "application/json"

Write-Host "Page elements:" -ForegroundColor Cyan
$snapshot | ConvertTo-Json -Depth 3