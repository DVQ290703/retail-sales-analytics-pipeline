$ErrorActionPreference = "Stop"

$connectUrl = "http://localhost:8083"
$maxAttempts = 30
$sleepSeconds = 5

for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    try {
        Invoke-RestMethod -Method Get -Uri "$connectUrl/connectors" | Out-Null
        Write-Output "Kafka Connect is ready."
        break
    }
    catch {
        if ($attempt -eq $maxAttempts) {
            throw "Kafka Connect did not become ready after $($maxAttempts * $sleepSeconds) seconds."
        }

        Write-Output "Waiting for Kafka Connect... attempt $attempt/$maxAttempts"
        Start-Sleep -Seconds $sleepSeconds
    }
}

$connectorConfig = Get-Content "debezium/register-postgres-connector.json" -Raw

Invoke-RestMethod `
    -Method Put `
    -Uri "$connectUrl/connectors/retail-postgres-connector/config" `
    -ContentType "application/json" `
    -Body (($connectorConfig | ConvertFrom-Json).config | ConvertTo-Json -Depth 10)

Write-Output "Registered Debezium connector: retail-postgres-connector"
