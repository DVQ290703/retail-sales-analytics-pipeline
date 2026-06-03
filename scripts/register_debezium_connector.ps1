$ErrorActionPreference = "Stop"

$connectorConfig = Get-Content "debezium/register-postgres-connector.json" -Raw

Invoke-RestMethod `
    -Method Put `
    -Uri "http://localhost:8083/connectors/retail-postgres-connector/config" `
    -ContentType "application/json" `
    -Body (($connectorConfig | ConvertFrom-Json).config | ConvertTo-Json -Depth 10)

Write-Output "Registered Debezium connector: retail-postgres-connector"
