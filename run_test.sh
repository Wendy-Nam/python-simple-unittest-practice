#!/bin/bash

# Automated test script for the Student Information Management Program
# This script checks for required packages and runs the test suite

echo "🧪 Starting automated tests for Student Information Management Program"
echo "=============================="

# Check if requirements.txt exists and install packages from it
if [ -f requirements.txt ]; then
  echo "🔍 Found requirements.txt, attempting to install required packages..."
  pip3 install -r requirements.txt
  if [ $? -ne 0 ]; then
    echo "❌ Failed to install packages from requirements.txt! Please check your pip environment."
    exit 1
  fi
else
  # Fallback: manually check and install required packages if requirements.txt doesn't exist
  REQUIRED_PKGS=("tabulate" "rich" "pandas" "openpyxl")
  for pkg in "${REQUIRED_PKGS[@]}"; do
    # Try to import the package to check if it's installed
    python3 -c "import $pkg" 2>/dev/null
    if [ $? -ne 0 ]; then
      echo "🔧 Package $pkg not found, installing automatically..."
      pip3 install $pkg
      if [ $? -ne 0 ]; then
        echo "❌ Failed to install $pkg! Please check your pip environment."
        exit 1
      fi
    fi
  done
fi

# Run the test suite
echo "🚀 Running test suite..."
python3 test_student_program.py

# Check test results and display appropriate message
if [ $? -eq 0 ]; then
  echo "✅ All tests passed successfully!"
else
  echo "❌ Tests failed! Please review your code."
fi
echo "=============================="