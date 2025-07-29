import sqlite3
import os
from datetime import datetime

#Create a folder for the database if it doesn't exists
folder_name = 'budget_data'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

#path to the database
db_path = os.path.join(folder_name,'budget.db')

#Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing table and recreate with correct schema
cursor.execute('DROP TABLE IF EXISTS Transactions')
cursor.execute('''
CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    category TEXT,
    amount REAL
)
''')
conn.commit()

#Creating the transactional table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT,
               type TEXT,       'income or expense'
               category TEXT,
               amount REAL
               )
  ''')
conn.commit()

def add_transaction():
    while True:
        t_type = input("Enter transaction type('income' or 'expense'): ").strip().lower()
        if t_type in ['income', 'expense']:
            break
        else:
            print("Please enter 'Income' or 'Expense': ")
    category = input("Enter category: ").strip()  
    while True:
        try:
            amount = float(input("Enter amount: R"))  
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid amount.")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO Transactions (date, type, category, amount) VALUES (?, ?, ?, ?)', (date_str, t_type, category, amount))
    conn.commit()
    print(f"{t_type.capitalize()} of R{amount} in category '{category}' added.\n")


def view_transactions():
    cursor.execute('SELECT * FROM  Transactions ORDER BY date DESC')
    rows = cursor.fetchall()
    if not rows:
        print("\nNo transactions found.\n")
        return
    print("\nAll Transactions:")
    print(f"{'Date':20} | {'Type':8} | {'Category':15} | {'Amount':10}")
    print("-" * 65)
    for row in rows:
        print(f"{row[1]:20} | {row[2]:8} | {row[3]:15} | ${row[4]:10.2f}")
    print()

def show_summary():
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE type='income'")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE type='expense'")
    total_expense = cursor.fetchone()[0] or 0
    balance = total_income - total_expense
    print("\n--- Budget Summary ---")
    print(f"Total Income: R{total_income:.2f}")
    print(f"Total Expenses: R{total_expense:.2f}")
    print(f"Current Balance: R{balance:.2f}\n")

def main():
    print("Welcome to 'CODE TEMPTRESS' Budget Tracker!")
    while True:
        print("Please choose an option:")
        print("1. Add a transaction")
        print("2. View all transactions")
        print("3. Show budget summary")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            show_summary()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")
    # Close database connection
    conn.close()

if __name__ == '__main__':
    main()

