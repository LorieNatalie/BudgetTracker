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

#Creating the transactional table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT,
               type TEXT,       'income oe expense'
               category TEXT,
               amount REAL
               )
  ''')
conn.commit()

def add_transaction():
    while True:
        t_type = input("Enter transaction type('inome' or 'expense':)").strip().lower()
        if t_type in ['income', 'expense']:
            break
        else:
            print("Please enter 'Income' or 'Expense' ")
    category = input("Enter category").strip()  
    while True:
        try:
            amount = float(input("Enter amount: R"))  
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid amount.")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    INSERT INTO Transactions (date, type, category, amount)
    VALUE (?, ?, ?, ?)               
    ''',(date_str, t_type, category, amount))
    conn.commit()
    print(f"{t_type.capitalize()} of R{amount} in category '{category}' added.\n")
    
