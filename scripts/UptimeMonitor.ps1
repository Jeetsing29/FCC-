<#
.SYNOPSIS
    AWS EC2 Website Live Uptime & Latency Monitor
    Course: Fundamentals of Cloud Computing (Second-Year B.Tech)
.DESCRIPTION
    Polls the EC2 website, checks HTTP status 200, calculates response time,
    and reports live uptime status.
#>

param(
    [string]$Url = "http://13.204.82.29/",
    [int]$IntervalSec = 3,
    [int]$MaxChecks = 5
)

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  AWS EC2 LIVE WEBSITE UPTIME & LATENCY MONITOR (PowerShell)            " -ForegroundColor Cyan
Write-Host "  Course: Fundamentals of Cloud Computing (Second-Year B.Tech)         " -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "Target URL      : $Url"
Write-Host "Interval        : $IntervalSec seconds"
Write-Host "Checks to run   : $(if ($MaxChecks -eq 0) { 'Infinite (Ctrl+C to stop)' } else { $MaxChecks })"
Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan

$count = 0
$success = 0
$failed = 0
$latencies = @()

try {
    while ($true) {
        $count++
        $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        
        try {
            $response = Invoke-WebRequest -Uri $Url -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
            $sw.Stop()
            $latency = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
            $statusCode = $response.StatusCode
            
            if ($statusCode -eq 200) {
                $success++
                $latencies += $latency
                Write-Host "[$timestamp] Status: $statusCode OK  | Latency: $latency ms | [UP]" -ForegroundColor Green
            } else {
                $failed++
                Write-Host "[$timestamp] Status: $statusCode  | Latency: $latency ms | [WARN]" -ForegroundColor Yellow
            }
        }
        catch {
            $sw.Stop()
            $failed++
            $latency = [math]::Round($sw.Elapsed.TotalMilliseconds, 2)
            Write-Host "[$timestamp] Status: DOWN/FAIL | Latency: $latency ms | Error: $($_.Exception.Message)" -ForegroundColor Red
        }

        if ($MaxChecks -gt 0 -and $count -ge $MaxChecks) {
            break
        }
        Start-Sleep -Seconds $IntervalSec
    }
}
catch {
    Write-Host "`nMonitoring halted by user." -ForegroundColor Yellow
}

$uptime = if ($count -gt 0) { [math]::Round(($success / $count) * 100, 2) } else { 0 }
$avgLatency = if ($latencies.Count -gt 0) { [math]::Round(($latencies | Measure-Object -Average).Average, 2) } else { 0 }

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "SUMMARY: Checks: $count | Up: $success | Down: $failed | Uptime: $uptime% | Avg Latency: $avgLatency ms" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
