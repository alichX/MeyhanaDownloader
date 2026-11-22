$ErrorActionPreference = "Stop"

$repoRoot = $PSScriptRoot
Set-Location $repoRoot

& py -3 -m PyInstaller --clean --noconfirm main.spec
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed."
}

$iscc = Get-ChildItem "C:\Program Files","C:\Program Files (x86)" -Filter "ISCC.exe" -Recurse -ErrorAction SilentlyContinue |
    Select-Object -First 1 -ExpandProperty FullName

if (-not $iscc) {
    $registryKeys = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )
    $inno = Get-ItemProperty $registryKeys -ErrorAction SilentlyContinue |
        Where-Object { $_.DisplayName -like "*Inno Setup*" } |
        Select-Object -First 1
    $innoPath = if ($inno.'Inno Setup: App Path') {
        $inno.'Inno Setup: App Path'
    } elseif ($inno.InstallLocation) {
        $inno.InstallLocation
    }
    if ($innoPath) {
        $candidate = Join-Path $innoPath "ISCC.exe"
        if (Test-Path $candidate) {
            $iscc = $candidate
        }
    }
}

if (-not $iscc) {
    throw "Inno Setup Compiler (ISCC.exe) is not installed."
}

New-Item -ItemType Directory -Force -Path (Join-Path $repoRoot "installer") | Out-Null
& $iscc (Join-Path $repoRoot "MeyhanaDownloader.iss")
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup build failed."
}
