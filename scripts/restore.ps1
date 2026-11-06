<#
.SYNOPSIS
    Restores a Script Scrapper database and storage backup.
.DESCRIPTION
    Validates SHA256 checksums, recreates the target database if required,
    restores database tables via pg_restore, and restores storage files.
.PARAMETER BackupDir
    Mandatory path to the backup directory (e.g. 'D:\script-scrapper\backups\backup_20261106_120000').
.PARAMETER TargetDatabase
    Name of the target database to restore into. Defaults to 'script_scrapper'.
.PARAMETER TargetStorageDir
    Path to destination storage directory. Defaults to 'D:\script-scrapper\storage'.
.PARAMETER PgBinDir
    Path to PostgreSQL bin directory. Defaults to 'D:\tools\pgsql\bin'.
.PARAMETER CreateDbIfNotExists
    Switch to automatically create the database if missing.
#>
[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$BackupDir,
    [string]$TargetDatabase = "script_scrapper",
    [string]$TargetStorageDir = "D:\script-scrapper\storage",
    [string]$PgBinDir = "D:\tools\pgsql\bin",
    [string]$DbHost = "127.0.0.1",
    [int]$Port = 5432,
    [string]$Username = "postgres",
    [switch]$CreateDbIfNotExists = $true
)

$ErrorActionPreference = "Stop"

Write-Host "=== Script Scrapper Restore Operation ===" -ForegroundColor Cyan
Write-Host "Source Backup: $BackupDir"
Write-Host "Target Database: $TargetDatabase"
Write-Host "Target Storage: $TargetStorageDir"

if (-not (Test-Path $BackupDir)) {
    Write-Error "Backup directory does not exist: $BackupDir"
    exit 1
}

$dbDumpFile = Join-Path $BackupDir "database.dump"
$storageBackupDir = Join-Path $BackupDir "storage"
$checksumFile = Join-Path $BackupDir "checksums.sha256"

if (-not (Test-Path $dbDumpFile)) {
    Write-Error "Database dump file missing: $dbDumpFile"
    exit 1
}

# 1. Verify Checksums
if (Test-Path $checksumFile) {
    Write-Host "Verifying SHA256 integrity checksums..." -ForegroundColor Cyan
    $checksumLines = Get-Content -Path $checksumFile
    foreach ($line in $checksumLines) {
        if (-not $line.Trim()) { continue }
        $parts = $line -split "\s+", 2
        $expectedHash = $parts[0].Trim().ToLower()
        $relPath = $parts[1].Trim()
        $fullPath = Join-Path $BackupDir $relPath

        if (-not (Test-Path $fullPath)) {
            throw "Integrity verification failed: Missing file $relPath"
        }
        $actualHash = (Get-FileHash -Path $fullPath -Algorithm SHA256).Hash.ToLower()
        if ($expectedHash -ne $actualHash) {
            throw "Integrity verification failed for ${relPath}: Expected $expectedHash, got $actualHash"
        }
    }
    Write-Host "Integrity verification PASSED." -ForegroundColor Green
} else {
    Write-Warning "Checksum file not found. Proceeding without checksum verification."
}

# Locate pg_restore and createdb
$pgRestoreExe = Join-Path $PgBinDir "pg_restore.exe"
$createdbExe = Join-Path $PgBinDir "createdb.exe"
$psqlExe = Join-Path $PgBinDir "psql.exe"

if (-not (Test-Path $pgRestoreExe)) {
    $pgRestoreExe = (Get-Command "pg_restore" -ErrorAction SilentlyContinue).Source
}
if (-not $pgRestoreExe -or -not (Test-Path $pgRestoreExe)) {
    Write-Error "pg_restore.exe not found at $PgBinDir or in system PATH."
    exit 1
}

try {
    # 2. Check if Target Database Exists
    Write-Host "Checking target database existence: $TargetDatabase..." -ForegroundColor Cyan
    $dbCheckOutput = & $psqlExe -h $DbHost -p $Port -U $Username -lqt | Select-String "\b$TargetDatabase\b"
    if (-not $dbCheckOutput) {
        if ($CreateDbIfNotExists) {
            Write-Host "Database '$TargetDatabase' does not exist. Creating..." -ForegroundColor Cyan
            & $createdbExe -h $DbHost -p $Port -U $Username $TargetDatabase
            Write-Host "Database created successfully." -ForegroundColor Green
        } else {
            throw "Target database '$TargetDatabase' does not exist and CreateDbIfNotExists was not set."
        }
    }

    # 3. Execute pg_restore
    Write-Host "Executing PostgreSQL database restore into $TargetDatabase..." -ForegroundColor Cyan
    $pgRestoreArgs = @(
        "-h", $DbHost,
        "-p", $Port,
        "-U", $Username,
        "-d", $TargetDatabase,
        "--clean",
        "--if-exists",
        "-v",
        $dbDumpFile
    )

    $proc = Start-Process -FilePath $pgRestoreExe -ArgumentList $pgRestoreArgs -Wait -NoNewWindow -PassThru
    # pg_restore returns 0 on success, or 1 if warnings (e.g., --clean on non-existent objects). Exit codes > 1 indicate failure.
    if ($proc.ExitCode -gt 1) {
        throw "pg_restore failed with exit code $($proc.ExitCode)"
    }
    Write-Host "Database restored successfully." -ForegroundColor Green

    # 4. Restore Storage Files
    if (Test-Path $storageBackupDir) {
        Write-Host "Restoring storage files to $TargetStorageDir..." -ForegroundColor Cyan
        New-Item -ItemType Directory -Path $TargetStorageDir -Force | Out-Null
        Copy-Item -Path "$storageBackupDir\*" -Destination $TargetStorageDir -Recurse -Force
        Write-Host "Storage files restored." -ForegroundColor Green
    }

    # 5. Verification Query
    Write-Host "Verifying table relations in $TargetDatabase..." -ForegroundColor Cyan
    $tables = & $psqlExe -h $DbHost -p $Port -U $Username -d $TargetDatabase -c "\dt"
    $tables | Out-Host

    Write-Host "=== Restore Operation Succeeded ===" -ForegroundColor Green
}
catch {
    Write-Error "Restore operation failed: $_"
    exit 1
}
