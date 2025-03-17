[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
winget source update


$osArch = (Get-WmiObject -Class Win32_OperatingSystem).OSArchitecture

Write-Host "OS Arch $osArch"

# Install Python if necessary
$pythonVersion = "3.12.5"
if ($osArch -match "ARM") {
    $installerName = "python-$pythonVersion-arm64.exe"
} elseif ($osArch -match "64") {
    $installerName = "python-$pythonVersion-amd64.exe"
} else {
    $installerName = "python-$pythonVersion.exe"
}
$downloadUrl = "https://www.python.org/ftp/python/$pythonVersion/$installerName"
$installerPath = Join-Path $env:TEMP $installerName
$installedPython = try { & python --version 2>&1 } catch { "" }

if ($installedPython -notmatch $pythonVersion) {
    Write-Host "Installing Python $pythonVersion..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath
    Write-Host "Downloaded Python installer to $installerPath."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Write-Host "Python $pythonVersion installation complete."
} else {
    Write-Host "Python $pythonVersion is already installed."
}

# Setup EdgeDriver
$edgeVersion = (Get-ItemProperty -Path HKCU:\Software\Microsoft\Edge\BLBeacon -Name version).version
$driverFile = if ($osArch -match "ARM") { "edgedriver_arm64.zip" } elseif ($osArch -match "64") { "edgedriver_win64.zip" } else { "edgedriver_win32.zip" }
$driverUrl = "https://msedgedriver.azureedge.net/$edgeVersion/$driverFile"
$outputFile = Join-Path (Get-Location) $driverFile


Write-Host "Edge Version $edgeVersion"

Write-Host "Downloading EdgeDriver..."
Invoke-WebRequest -Uri $driverUrl -OutFile $outputFile
Write-Host "Downloaded EdgeDriver from $driverUrl to $outputFile."

$extractPath = Join-Path (Get-Location) "msedgedriver"
if (!(Test-Path $extractPath)) { New-Item -ItemType Directory -Path $extractPath | Out-Null }
Expand-Archive -Path $outputFile -DestinationPath $extractPath -Force
Remove-Item $outputFile -Force

Write-Host "EdgeDriver setup complete."
