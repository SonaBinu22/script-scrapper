<#
.SYNOPSIS
    Creates a synchronized database and filesystem backup for Script Scrapper.
.DESCRIPTION
    Dumps PostgreSQL 16 database using pg_dump custom format and archives storage files.
    Calculates SHA256 integrity checksums for all backup artifacts.
.PARAMETER BackupDir
    Target directory for storing backups. Defaults to 'D:\script-scrapper\backups'.
.PARAMETER DatabaseName
    Target database name. Defaults to 'script_scrapper'.
.PARAMETER StorageDir
    Path to storage directory. Defaults to 'D:\script-scrapper\storage'.
.PARAMETER PgBinDir
    Path to PostgreSQL bin directory. Defaults to 'D:\tools\pgsql\bin'.
#>
[CmdletBinding()]
param (
    [string]$BackupDir = "D:\script-scrapper\backups",
    [string]$DatabaseName = "script_scrapper",
    [string]$StorageDir = "D:\script-scrapper\storage",
    [string]$PgBinDir = "D:\tools\pgsql\bin",
    [string]$DbHost = "127.0.0.1",
    [int]$Port = 5432,
    [string]$Username = "postgres"
)

$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$targetBackupDir = Join-Path $BackupDir "backup_$timestamp"
$dbDumpFile = Join-Path $targetBackupDir "database.dump"
$storageBackupDir = Join-Path $targetBackupDir "storage"
$checksumFile = Join-Path $targetBackupDir "checksums.sha256"
$metaFile = Join-Path $targetBackupDir "backup_meta.json"

Write-Host "=== Script Scrapper Backup Operation ===" -ForegroundColor Cyan
Write-Host "Timestamp: $timestamp"
Write-Host "Destination: $targetBackupDir"

# Ensure directories exist
New-Item -ItemType Directory -Path $targetBackupDir -Force | Out-Null
New-Item -ItemType Directory -Path $storageBackupDir -Force | Out-Null
if (-not (Test-Path $StorageDir)) {
    New-Item -ItemType Directory -Path $StorageDir -Force | Out-Null
}

# Locate pg_dump
$pgDumpExe = Join-Path $PgBinDir "pg_dump.exe"
if (-not (Test-Path $pgDumpExe)) {
    $pgDumpExe = (Get-Command "pg_dump" -ErrorAction SilentlyContinue).Source
}

if (-not $pgDumpExe -or -not (Test-Path $pgDumpExe)) {
    Write-Error "pg_dump.exe not found at $PgBinDir or in system PATH."
    exit 1
}

try {
    # 1. Execute pg_dump
    Write-Host "Executing PostgreSQL database dump..." -ForegroundColor Cyan
    $pgDumpArgs = @(
        "-h", $DbHost,
        "-p", $Port,
        "-U", $Username,
        "-F", "c",
        "-b",
        "-v",
        "-f", $dbDumpFile,
        $DatabaseName
    )
    
    $proc = Start-Process -FilePath $pgDumpExe -ArgumentList $pgDumpArgs -Wait -NoNewWindow -PassThru
    if ($proc.ExitCode -ne 0) {
        throw "pg_dump failed with exit code $($proc.ExitCode)"
    }
    Write-Host "Database dump completed: $dbDumpFile ($((Get-Item $dbDumpFile).Length) bytes)" -ForegroundColor Green

    # 2. Synchronize Storage Files
    Write-Host "Synchronizing storage files from $StorageDir..." -ForegroundColor Cyan
    $storageFiles = Get-ChildItem -Path $StorageDir -Recurse -File -ErrorAction SilentlyContinue
    $fileCount = 0
    if ($storageFiles) {
        $fileCount = $storageFiles.Count
        Copy-Item -Path "$StorageDir\*" -Destination $storageBackupDir -Recurse -Force
    }
    Write-Host "Storage files copied: $fileCount items" -ForegroundColor Green

    # 3. Generate SHA256 Checksums
    Write-Host "Calculating SHA256 checksums..." -ForegroundColor Cyan
    $allBackupFiles = Get-ChildItem -Path $targetBackupDir -Recurse -File | Where-Object { $_.FullName -ne $checksumFile -and $_.FullName -ne $metaFile }
    $checksumLines = @()
    foreach ($file in $allBackupFiles) {
        $hash = (Get-FileHash -Path $file.FullName -Algorithm SHA256).Hash.ToLower()
        $relativeName = $file.FullName.Substring($targetBackupDir.Length + 1)
        $checksumLines += "$hash  $relativeName"
    }
    $checksumLines | Out-File -FilePath $checksumFile -Encoding utf8
    Write-Host "Checksum file written: $checksumFile" -ForegroundColor Green

    # 4. Generate Metadata Manifest
    $meta = [PSCustomObject]@{
        timestamp = $timestamp
        database = $DatabaseName
        dump_file = "database.dump"
        dump_size_bytes = (Get-Item $dbDumpFile).Length
        storage_file_count = $fileCount
        status = "COMPLETED"
    }
    $meta | ConvertTo-Json -Depth 4 | Out-File -FilePath $metaFile -Encoding utf8
    Write-Host "Backup metadata written: $metaFile" -ForegroundColor Green

    Write-Host "=== Backup Operation Succeeded ===" -ForegroundColor Green
    return $targetBackupDir
}
catch {
    Write-Error "Backup failed: $_"
    exit 1
}
