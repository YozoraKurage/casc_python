<#
.SYNOPSIS
    Batch-export every .casc under a folder to FBX, into the same directory with
    the same base name. Cascadeur command-line launcher.

.DESCRIPTION
    Uses Cascadeur's command line:  --run-script <module-name>
    to make a running Cascadeur instance perform the batch export.

    Cascadeur facts this relies on:
      * --run-script takes a MODULE NAME (not an absolute path).
        This tool's module is: commands.batch_export_fbx._startup
      * The module must be on Cascadeur's Python path
        (placing it under commands/ puts it on the path automatically).
      * Cascadeur must be ALREADY RUNNING. If not, --run-script arguments may be
        misinterpreted as scene names (so use -StartIfNotRunning to start+wait).

    Passing the settings (folder + options):
      When --run-script is dispatched to an already-running instance, environment
      variables set by THIS launcher process do NOT reach that instance. Therefore
      settings are passed via a JSON file (~/.casc_batch_export_fbx.json) which the
      startup module reads (and then deletes).

    NOTE: This script is intentionally ASCII-only so Windows PowerShell 5.1 parses
          it correctly regardless of system locale/codepage.

.EXAMPLE
    # With Cascadeur already running:
    .\Export-CascToFbx.ps1 -Folder "D:\projects"

.EXAMPLE
    # Auto-start Cascadeur, export, then quit (headless-style batch):
    .\Export-CascToFbx.ps1 -Folder "D:\projects" -StartIfNotRunning -Quit -Ascii -UpAxis Y
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Folder,

    [string]$Cascadeur = "C:\Program Files\Cascadeur\cascadeur.exe",

    # Module name passed to --run-script (normally no need to change)
    [string]$Module = "commands.batch_export_fbx._startup",

    [ValidateSet("all", "model", "joints", "scene")]
    [string]$Mode = "all",

    [switch]$NoRecursive,
    [switch]$SkipExisting,
    [switch]$RigMode,
    [switch]$Ascii,

    [ValidateSet("X", "Y", "Z")]
    [string]$UpAxis = "",

    [switch]$Quit,

    # Start Cascadeur if it is not running, then wait before sending --run-script
    [switch]$StartIfNotRunning,
    [int]$StartupWait = 25,

    # Config file path (must match Python side default_config_path())
    [string]$ConfigPath = (Join-Path $env:USERPROFILE ".casc_batch_export_fbx.json")
)

$ErrorActionPreference = "Stop"

# --- validate input -------------------------------------------------------
if (-not (Test-Path -LiteralPath $Folder)) {
    throw "Folder not found: $Folder"
}
$Folder = (Resolve-Path -LiteralPath $Folder).Path

# --- write settings JSON (read by the startup module) ---------------------
$upAxisValue = $null
if (-not [string]::IsNullOrWhiteSpace($UpAxis)) { $upAxisValue = $UpAxis }

$config = [ordered]@{
    folder         = $Folder
    recursive      = (-not $NoRecursive.IsPresent)
    export_mode    = $Mode
    skip_existing  = $SkipExisting.IsPresent
    enter_rig_mode = $RigMode.IsPresent
    ascii          = $Ascii.IsPresent
    up_axis        = $upAxisValue
    quit_after     = $Quit.IsPresent
}
$json = $config | ConvertTo-Json
# Write UTF-8 without BOM (Python reads it with utf-8-sig, so either is fine)
[System.IO.File]::WriteAllText($ConfigPath, $json, (New-Object System.Text.UTF8Encoding($false)))

Write-Host "[Export-CascToFbx] wrote settings: $ConfigPath"
Write-Host $json
Write-Host "[Export-CascToFbx] target folder: $Folder"

if (-not (Test-Path -LiteralPath $Cascadeur)) {
    Write-Warning "Cascadeur executable not found: $Cascadeur (use -Cascadeur to set the correct path)"
}

# --- check running state --------------------------------------------------
$procName = [System.IO.Path]::GetFileNameWithoutExtension($Cascadeur)
$running = @(Get-Process -Name $procName -ErrorAction SilentlyContinue)

if ($running.Count -eq 0) {
    if ($StartIfNotRunning) {
        if (Test-Path -LiteralPath $Cascadeur) {
            Write-Host "[Export-CascToFbx] starting Cascadeur, waiting $StartupWait s ..."
            Start-Process -FilePath $Cascadeur
            Start-Sleep -Seconds $StartupWait
        }
        else {
            throw "Cannot start Cascadeur (executable not found): $Cascadeur"
        }
    }
    else {
        Write-Warning "Cascadeur is not running."
        Write-Host "  Start Cascadeur first and re-run, or pass -StartIfNotRunning." -ForegroundColor Yellow
        Write-Host "  (Sending --run-script while not running may be misread as a scene name.)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  Alternatively, run this in Cascadeur's Python console:" -ForegroundColor Yellow
        Write-Host "      from commands.batch_export_fbx import cli; cli.run_auto()" -ForegroundColor Cyan
        return
    }
}

# --- send --run-script ----------------------------------------------------
if ($Quit -and -not $StartIfNotRunning) {
    Write-Warning "-Quit will close Cascadeur after export, including your current working session."
}

Write-Host "[Export-CascToFbx] running: `"$Cascadeur`" --run-script $Module"
Start-Process -FilePath $Cascadeur -ArgumentList @("--run-script", $Module)

Write-Host ""
Write-Host "Sent. The export runs inside the Cascadeur process." -ForegroundColor Green
Write-Host "Check progress/results in Cascadeur's Python console / logs." -ForegroundColor Green
