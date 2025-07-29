import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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

# --------- Database functions ---------
def get_transactions():
    cursor.execute('SELECT * FROM Transactions ORDER BY date DESC')
    return cursor.fetchall()

def add_transaction(t_type, category, amount):
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO Transactions (date, type, category, amount) VALUES (?, ?, ?, ?)',
                   (date_str, t_type, category, amount))
    conn.commit()

def delete_transaction(t_id):
    cursor.execute('DELETE FROM Transactions WHERE id=?', (t_id,))
    conn.commit()

def update_transaction(t_id, t_type, category, amount):
    cursor.execute('UPDATE Transactions SET type=?, category=?, amount=? WHERE id=?',
                   (t_type, category, amount, t_id))
    conn.commit()

def get_summary():
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE type='income'")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM Transactions WHERE type='expense'")
    total_expense = cursor.fetchone()[0] or 0
    balance = total_income - total_expense
    return total_income, total_expense, balance

# --------- GUI setup ---------
root = tk.Tk()
root.title("CODE TEMPTRESS Budget Tracker")

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

# Treeview for transactions
tree = ttk.Treeview(root, columns=('ID', 'Date', 'Type', 'Category', 'Amount'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Date', text='Date')
tree.heading('Type', text='Type')
tree.heading('Category', text='Category')
tree.heading('Amount', text='Amount')
tree.pack(fill=tk.BOTH, expand=True)

def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    for row in get_transactions():
        tree.insert('', tk.END, values=row)

# --------- Button callbacks -----------
def prompt_add_transaction():
    t_type = simpledialog.askstring("Transaction Type", "Enter type ('income' or 'expense'):")
    if t_type is None:
        return
    t_type = t_type.strip().lower()
    if t_type not in ['income', 'expense']:
        messagebox.showerror("Error", "Invalid type! Must be 'income' or 'expense'.")
        return
    category = simpledialog.askstring("Category", "Enter category:")
    if category is None:
        return
    try:
        amount_str = simpledialog.askstring("Amount", "Enter amount in R:")
        if amount_str is None:
            return
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Invalid amount!")
        return
    add_transaction(t_type, category, amount)
    refresh_tree()

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No transaction selected.")
        return
    t_id = tree.item(selected[0])['values'][0]
    delete_transaction(t_id)
    refresh_tree()

def edit_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No transaction selected.")
        return
    item = tree.item(selected[0])['values']
    t_id, date, t_type, category, amount = item
    # Get new data via dialogs
    new_type = simpledialog.askstring("Type", "Enter new type ('income' or 'expense'):", initialvalue=t_type)
    if new_type is None:
        return
    new_type = new_type.strip().lower()
    if new_type not in ['income', 'expense']:
        messagebox.showerror("Error", "Invalid type!")
        return
    new_category = simpledialog.askstring("Category", "Enter new category:", initialvalue=category)
    if new_category is None:
        return
    try:
        new_amount_str = simpledialog.askstring("Amount", "Enter new amount:", initialvalue=str(amount))
        if new_amount_str is None:
            return
        new_amount = float(new_amount_str)
        if new_amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Invalid amount!")
        return
    update_transaction(t_id, new_type, new_category, new_amount)
    refresh_tree()

def show_summary():
    total_income, total_expense, balance = get_summary()
    messagebox.showinfo(
        "Budget Summary",
        f"Total Income: R{total_income:.2f}\n"
        f"Total Expenses: R{total_expense:.2f}\n"
        f"Current Balance: R{balance:.2f}"
    )

# Buttons
tk.Button(button_frame, text="Add Transaction", command=prompt_add_transaction).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Edit Selected", command=edit_selected).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="Show Budget Summary", command=show_summary).pack(side=tk.LEFT, padx=5, pady=5)

# Initialize display
refresh_tree()

# Run the GUI
root.mainloop()

# Close database connection
conn.close()