$input_json = [Console]::In.ReadToEnd()

$message = "Claude Code needs your attention"
try {
    $payload = $input_json | ConvertFrom-Json
    if ($payload.message) {
        $message = $payload.message
    }
} catch {}

Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show($message, "Claude Code") | Out-Null
