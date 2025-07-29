#!/bin/bash

# Create virtual environment named bt_venv
python3 -m venv bt_venv

# Activate the virtual environment
source bt_venv/bin/activate

# (Optional) Install dependencies here if needed, e.g.,
# pip install some_package

# Run your Python script
python3 budget_tracker.py

# Deactivate after running
deactivate

#Deleting database
rm budget_data/budget.db

#Automate Setup
Make it executable:
        
        chmod +x build.sh

Run it:

    ./build.sh