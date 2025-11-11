$jsonInput = [Console]::In.ReadToEnd()
$data = $jsonInput | ConvertFrom-Json

$time = Get-Date -Format 'hh:mmtt'
$branch = git branch --show-current 2>$null
if (-not $branch) { $branch = 'main' }
$cost = if ($data.cost.total_cost_usd -and $data.cost.total_cost_usd -gt 0) {
    '$' + ('{0:F4}' -f $data.cost.total_cost_usd)
} else {
    '$0.0000'
}

Write-Output "$time | Sonnet 4.5 | $env:USERNAME [GitBranch: $branch] | Cost: $cost"
