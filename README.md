# BudgetTracker

A simple Python-based budget tracking application that allows you to add income and expense transactions, view all transactions, and see a summary of your finances. Data is stored in an SQLite database for persistence.

## Features

- Add income or expense transactions with category and amount
- View all transactions in a table
- See a summary with total income, total expenses, and current balance
- Use a virtual environment for dependency management


## Setup Instructions

### 1. Clone or download the project folder

### 2. Create and activate a virtual environment

Open your terminal, navigate to the project directory, then run:

```bash
# Create virtual environment named bt_venv
python3 -m venv bt_venv

# Activate the virtual environment
source bt_venv/bin/activate
```

### 3. Run the Budget Tracker

With the virtual environment activated, run:

```bash
python3 budget_tracker.py
```

### 4. Deactivate the virtual environment when done

```bash
deactivate
```


## Usage

Follow the on-screen menu to add transactions, view all transactions, see your budget summary, or exit the application.


## Notes

- The data is stored in `budget.db`.


## License

This project is for educational purposes. Feel free to modify and use it as you like.


## Contact

For questions or feedback, contact me at lorienatalienoelle@gmail.com
