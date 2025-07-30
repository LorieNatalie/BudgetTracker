# BudgetTracker

A simple Python-based budget tracking application that allows you to manage income and expenses securely. It features user registration, login, transaction management, and persistent data storage using SQLite. Designed for educational purposes, it's perfect for tracking your finances in a straightforward way.
Features

    Register new users with secure password hashing
    Log in to access your personal budget data
    Add income or expense transactions with category and amount
    View all transactions in a table
    Edit or delete existing transactions
    View a summary with total income, total expenses, and current balance
    Data stored in an SQLite database for persistence
    Run in a virtual environment for dependency management

Setup Instructions
1. Clone or download the project folder
2. Create and activate a virtual environment

Open your terminal, navigate to the project directory, then run:

          

# Create virtual environment named bt_venv
python3 -m venv bt_venv

# Activate the virtual environment
source bt_venv/bin/activate

      

3. Install dependencies

Within the activated environment, install the required packages:

          

pip install bcrypt

      

(Note: tkinter is usually included with Python. If you encounter issues with the GUI, install it separately:)

          

sudo apt update
sudo apt install python3-tk

      

4. Run the Budget Tracker

          

python3 budget_tracker.py

      

5. When you're done, deactivate the environment:

          

deactivate

      

Usage

    Upon launching, a login window prompts you to log in or register.
    Register a new account or log in with your credentials.
    Once logged in, the main interface appears, allowing you to add, edit, or delete transactions.
    Use the buttons to view your budget summary or manage transactions.

    Note: The database (budget_data/budget.db) is created automatically if it doesn't exist and stores all your data securely.

Notes

    IDs for transactions are auto-incremented; they are not reused or reset upon deletion.
    Data persists across sessions.
    User passwords are hashed with bcrypt for security.
    The application is intended for educational use; feel free to modify and extend it.

License

This project is for educational purposes. Feel free to modify and use it as you see fit.
Contact

For questions or feedback, contact me at lorienatalienoelle@gmail.com