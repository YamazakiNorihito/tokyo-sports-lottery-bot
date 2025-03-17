$driverPath = Join-Path $PSScriptRoot 'msedgedriver\msedgedriver.exe'

Set-Location $PSScriptRoot

# Define the virtual environment path
$venvPath = Join-Path $PSScriptRoot 'venv'

# If the virtual environment doesn't exist, create it and install dependencies
if (!(Test-Path $venvPath)) {
    python -m venv venv
    & "$venvPath\Scripts\pip.exe" install -r requirements.txt
}

# Execute the Python script using the virtual environment's python interpreter
& "$venvPath\Scripts\python.exe" src/main.py --driver_path $driverPath