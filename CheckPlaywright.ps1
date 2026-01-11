Write-Host "=== Playwright Tools Status ===" -ForegroundColor Cyan

# Define the tools to check
$tools = @(
    "browser_navigate",
    "browser_snapshot", 
    "browser_take_screenshot",
    "browser_click",
    "browser_close"
)

# Headers required for the API
$headers = @{
    "accept" = "application/json"
    "Content-Type" = "application/json"
}

foreach ($tool in $tools) {
    # Prepare a dummy/test payload for each tool to satisfy the API requirements
    $body = @{ url = "https://example.com" } | ConvertTo-Json

    try {
        # Using POST as required by the API
        $response = Invoke-WebRequest -Uri "http://localhost:8000/playwright/$tool" `
            -Method Post `
            -Headers $headers `
            -Body $body `
            -ErrorAction Stop

        Write-Host "[OK] $tool - Available (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        # Check if it's a 400-level error that still proves the endpoint exists
        if ($_.Exception.Message -like "*422*" -or $_.Exception.Message -like "*400*") {
            Write-Host "[OK] $tool - Reachable (But requires specific parameters)" -ForegroundColor Yellow
        } else {
            Write-Host "[FAIL] $tool - Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}