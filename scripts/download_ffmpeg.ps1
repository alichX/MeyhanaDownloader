[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetDir
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$binDir = Join-Path $TargetDir "ffmpeg\bin"
$zipPath = Join-Path $env:TEMP "meyhana-ffmpeg.zip"
$extractDir = Join-Path $env:TEMP "meyhana-ffmpeg"

New-Item -ItemType Directory -Force -Path $binDir | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue $zipPath
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $extractDir

Write-Host "Downloading FFmpeg..."
Invoke-WebRequest `
    -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" `
    -OutFile $zipPath

Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force
$sourceBin = Get-ChildItem -Path $extractDir -Directory -Recurse |
    Where-Object { $_.Name -eq "bin" } |
    Select-Object -First 1

if ($null -eq $sourceBin) {
    throw "Downloaded FFmpeg archive does not contain a bin directory."
}

Copy-Item -Force (Join-Path $sourceBin.FullName "ffmpeg.exe") $binDir
Copy-Item -Force (Join-Path $sourceBin.FullName "ffprobe.exe") $binDir

Remove-Item -Force -ErrorAction SilentlyContinue $zipPath
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $extractDir

Write-Host "FFmpeg installed."
