#!/bin/bash

python_path="python"
venv_name=".venv"  

# Get the directory where the script is located
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
program_path="$script_dir/main.py" 

# Check if virtual environment exists
if [ ! -d "$venv_name" ]; then
    echo "Virtual environment not found. Creating..."
    $python_path -m venv "$venv_name"
fi

# Activate virtual environment
source "$venv_name/bin/activate"

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    python -m pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Skipping dependency installation."
fi

# Execute the Python program
$python_path $program_path
