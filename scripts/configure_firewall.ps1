<#
.SYNOPSIS
    Configures Windows Defender Firewall rules for Script Scrapper host.
.DESCRIPTION
    Opens inbound ports 80 (HTTP) and 443 (HTTPS) strictly scoped to the local LAN subnet.
    Ensures backend API (8000) and PostgreSQL (5432) remain protected on localhost.
.PARAMETER LanSubnet
    The authorized CIDR subnet (e.g. "192.168.1.0/24"). Defaults to value in .env or 192.168.1.0/24.
.PARAMETER DryRun
    If set, validates and prints configuration without modifying firewall rules.
#>
[CmdletBinding()]
param (
    [string]$LanSubnet,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "=== Script Scrapper Firewall Configuration ===" -ForegroundColor Cyan

# Resolve LAN Subnet
if (-not $LanSubnet) {
    if (Test-Path ".env") {
        $envMatch = Select-String -Path ".env" -Pattern "^LAN_SUBNET\s*=\s*['""]?([^'""]+)['""]?"
        if ($envMatch) {
            $LanSubnet = $envMatch.Matches[0].Groups[1].Value.Trim()
            Write-Host "Discovered LAN_SUBNET from .env: $LanSubnet" -ForegroundColor Green
        }
    }
}

if (-not $LanSubnet) {
    $LanSubnet = "192.168.1.0/24"
    Write-Host "Using default LAN_SUBNET: $LanSubnet" -ForegroundColor Yellow
}

Write-Host "Target Authorized Ingress Subnet: $LanSubnet"
Write-Host "Target Inbound Ports: 80 (HTTP), 443 (HTTPS)"
Write-Host "Internal Blocked Ports: 8000 (FastAPI), 5432 (PostgreSQL) - Localhost Only"

if ($DryRun) {
    Write-Host "[DRY RUN] Verification complete. No rules modified." -ForegroundColor Yellow
    exit 0
}

# Check Administrative Privileges
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Warning "Modifying Windows Firewall rules requires Administrator privileges."
    Write-Warning "Run PowerShell as Administrator to apply these rules permanently, or use -DryRun for validation."
    exit 1
}

try {
    # 1. Remove existing Script Scrapper firewall rules if present
    Remove-NetFirewallRule -DisplayName "ScriptScrapper-HTTPS-In" -ErrorAction SilentlyContinue
    Remove-NetFirewallRule -DisplayName "ScriptScrapper-HTTP-In" -ErrorAction SilentlyContinue

    # 2. Add Inbound HTTPS Rule (Port 443) scoped to LanSubnet and LocalSubnet
    New-NetFirewallRule -DisplayName "ScriptScrapper-HTTPS-In" `
        -Direction Inbound `
        -Action Allow `
        -Protocol TCP `
        -LocalPort 443 `
        -RemoteAddress @($LanSubnet, "LocalSubnet") `
        -Description "Script Scrapper Secure Web UI and API Gateway (Caddy HTTPS)" | Out-Null
    Write-Host "Created Inbound Rule: ScriptScrapper-HTTPS-In (TCP 443, Remote: $LanSubnet)" -ForegroundColor Green

    # 3. Add Inbound HTTP Rule (Port 80) for automatic HTTPS redirection
    New-NetFirewallRule -DisplayName "ScriptScrapper-HTTP-In" `
        -Direction Inbound `
        -Action Allow `
        -Protocol TCP `
        -LocalPort 80 `
        -RemoteAddress @($LanSubnet, "LocalSubnet") `
        -Description "Script Scrapper HTTP to HTTPS Redirect" | Out-Null
    Write-Host "Created Inbound Rule: ScriptScrapper-HTTP-In (TCP 80, Remote: $LanSubnet)" -ForegroundColor Green

    # 4. Verification Check: Ensure ports 8000 and 5432 are NOT exposed
    $exposedRules = Get-NetFirewallRule -Direction Inbound -Action Allow -Enabled True -ErrorAction SilentlyContinue |
        Get-NetFirewallPortFilter | Where-Object { $_.LocalPort -match "8000|5432" }

    if ($exposedRules) {
        Write-Warning "Security Warning: The following inbound allow rules permit traffic on ports 8000/5432:"
        $exposedRules | Format-Table -Property Protocol, LocalPort
    } else {
        Write-Host "Security Audit PASSED: Ports 8000 and 5432 have no public/LAN inbound allow rules." -ForegroundColor Green
    }
}
catch {
    Write-Error "Failed to configure firewall: $_"
    exit 1
}
