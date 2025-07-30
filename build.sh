#!/bin/bash


# Create virtual environment named bt_venv
python3 -m venv bt_venv

# Activate the virtual environment
source bt_venv/bin/activate

# (Optional) Install dependencies here
# Make sure to include bcrypt and any other packages your script needs
pip install bcrypt

# Install tkinter if not already installed (for Debian/Ubuntu)
# sudo apt update
# sudo apt install python3-tk

# Run your Python script
python3 budget_tracker.py

# Deactivate the virtual environment
deactivate

# (Optional) Delete the database after running
# Be cautious with this! Uncomment if you want to delete it every time
# rm -rf budget_data/budget.db

# Make script executable
# chmod +x build.sh

      

Notes:

    pip install bcrypt is included so your script has the bcrypt library.
    python3-tk installation is commented out because it typically requires sudo privileges; run that manually if needed.
    Database deletion is optional; uncomment the rm line if you want the database wiped each run.
    Remember to give execution permission:

          

chmod +x build.sh

      

Usage:

          

./build.sh
