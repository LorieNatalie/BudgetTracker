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
        if

