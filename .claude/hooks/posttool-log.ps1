$input_json = [Console]::In.ReadToEnd()

$toolName = "unknown"
try {
    $payload = $input_json | ConvertFrom-Json
    if ($payload.tool_name) {
        $toolName = $payload.tool_name
    }
} catch {}

$logPath = Join-Path $PSScriptRoot "posttool.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logPath -Value "$timestamp - Tool used: $toolName"
