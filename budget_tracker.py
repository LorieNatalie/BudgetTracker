import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import os
from datetime import datetime
import bcrypt

#Create a folder for the database if it doesn't exists
folder_name = 'budget_data'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

#path to the database
db_path = os.path.join(folder_name,'budget.db')

#Connect to the database
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Create Users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
)
''')
conn.commit()

# Create Transactions table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    type TEXT,
    category TEXT,
    amount REAL
)
''')
conn.commit()

# --- Authentication Functions ---
def register_user(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO Users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    

def verify_user(username, password):
    cursor.execute('SELECT password_hash FROM Users WHERE username=?', (username,))
    row = cursor.fetchone()
    if row:
        stored_hash = row['password_hash']
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False


# --- Initialize main window but keep it hidden until login ---
root = tk.Tk()
root.title("CODE TEMPTRESS Budget Tracker")
root.withdraw()  # Hide main window initially

current_user = None  # To track logged-in user


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

# --- GUI functions ---
def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    if current_user:
        for row in get_transactions():
            tree.insert('', tk.END, values=list(row))

def show_login():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.grab_set()  # Make modal

    tk.Label(login_win, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_win, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = tk.Entry(login_win, show='*')
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if verify_user(username, password):
            global current_user
            current_user = username
            login_win.destroy()
            # Show main window now
            root.deiconify()
            refresh_tree()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_register():
        reg_win = tk.Toplevel()
        reg_win.title("Register")
        reg_win.grab_set()

        tk.Label(reg_win, text="New Username:").grid(row=0, column=0, padx=5, pady=5)
        new_user_entry = tk.Entry(reg_win)
        new_user_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(reg_win, text="New Password:").grid(row=1, column=0, padx=5, pady=5)
        new_pass_entry = tk.Entry(reg_win, show='*')
        new_pass_entry.grid(row=1, column=1, padx=5, pady=5)

        def attempt_register():
            new_username = new_user_entry.get()
            new_password = new_pass_entry.get()
            if register_user(new_username, new_password):
                messagebox.showinfo("Success", "Registration successful! Please login.")
                reg_win.destroy()
            else:
                messagebox.showerror("Error", "Username already exists.")

        tk.Button(reg_win, text="Register", command=attempt_register).grid(row=2, column=0, columnspan=2, pady=5)

    tk.Button(login_win, text="Login", command=attempt_login).grid(row=2, column=0, pady=5)
    tk.Button(login_win, text="Register", command=show_register).grid(row=2, column=1, pady=5)

# --- Main window setup ---
# Create frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

# Treeview for transactions
tree = ttk.Treeview(root, columns=('ID', 'Date', 'Type', 'Category', 'Amount'), show='headings')
for col in ('ID', 'Date', 'Type', 'Category', 'Amount'):
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

# Button callbacks
def prompt_add_transaction():
    if not current_user:
        messagebox.showerror("Unauthorized", "Please login first.")
        return
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
    if not current_user:
        messagebox.showerror("Unauthorized", "Please login first.")
        return
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No transaction selected.")
        return
    t_id = tree.item(selected[0])['values'][0]
    delete_transaction(t_id)
    refresh_tree()

def edit_selected():
    if not current_user:
        messagebox.showerror("Unauthorized", "Please login first.")
        return
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No transaction selected.")
        return
    item = list(tree.item(selected[0])['values'])
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
    if not current_user:
        messagebox.showerror("Unauthorized", "Please login first.")
        return
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

# --- Show login window first ---
root.after(100, show_login)

# Run mainloop only after login success
root.mainloop()

# Close database connection on exit
conn.close()