$pythonPath = "python" # Adjust if your Python path is different
$venvName = ".venv"

# Get the directory where the script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$programPath = Join-Path $scriptDir "main.py"

# Check if virtual environment exists
if (!(Test-Path $venvName -PathType Container)) {
    Write-Output "Virtual environment not found. Creating..."
    & $pythonPath -m venv $venvName
}

# Activate virtual environment
& (Join-Path $venvName "Scripts\Activate.ps1")

# Check if requirements.txt exists
if (Test-Path "requirements.txt" -PathType Leaf) {
    Write-Output "Installing dependencies from requirements.txt..."
    python -m pip install -r requirements.txt
} else {
    Write-Output "Warning: requirements.txt not found. Skipping dependency installation."
}

# Execute the Python program
& $pythonPath $programPath 
