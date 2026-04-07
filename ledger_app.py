import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Initial accounts
accounts = {
    "FOUZ": 0,
    "MOM": 0,
    "FIDA": 0
}

transactions = {
    "FOUZ": [],
    "MOM": [],
    "FIDA": []
}

# Dictionaries to hold pages and nav buttons
account_pages = {}
nav_buttons = {}

def get_bank_balance():
    return sum(accounts.values())

def show_frame(frame):
    frame.tkraise()
    update_all()

def update_all():
    # Update all account pages
    for name, (frame, balance_label, listbox) in account_pages.items():
        balance_label.config(text=f"Balance: ₹{accounts[name]}")
        listbox.delete(0, tk.END)
        for t in transactions[name]:
            listbox.insert(tk.END, t)
    bank_balance.config(text=f"Bank Balance: ₹{get_bank_balance()}")

def create_person_page(person):
    frame = tk.Frame(container)

    title = tk.Label(frame, text=f"{person} Account", font=("Arial", 20, "bold"))
    title.pack(pady=5)

    balance_label = tk.Label(frame, font=("Arial", 16))
    balance_label.pack(pady=5)

    amount_entry = tk.Entry(frame, font=("Arial", 16), width=25)
    amount_entry.pack(pady=5)
    amount_entry.insert(0, "Amount")

    reason_entry = tk.Entry(frame, font=("Arial", 16), width=40)
    reason_entry.pack(pady=5)
    reason_entry.insert(0, "Reason ")

    listbox = tk.Listbox(frame, width=70, height=10, font=("Arial", 14))
    listbox.pack(pady=10)

    # Deposit
    def do_deposit():
        if amount_entry.get().isdigit():
            amount = int(amount_entry.get())
            reason = reason_entry.get()
            accounts[person] += amount
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            transactions[person].append(f"+{amount} | {reason} | {now}")
            update_all()
            amount_entry.delete(0, tk.END)
            reason_entry.delete(0, tk.END)

    # Withdraw (allow negative balance)
    def do_withdraw():
        if amount_entry.get().isdigit():
            amount = int(amount_entry.get())
            reason = reason_entry.get()
            accounts[person] -= amount  # negative allowed
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            transactions[person].append(f"-{amount} | {reason} | {now}")
            update_all()
            amount_entry.delete(0, tk.END)
            reason_entry.delete(0, tk.END)

    # Delete transaction
    def delete_transaction():
        selected = listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a transaction to delete")
            return
        index = selected[0]
        entry = transactions[person][index]
        if entry.startswith("+"):
            amount = int(entry.split("|")[0][1:].strip())
            accounts[person] -= amount
        elif entry.startswith("-"):
            amount = int(entry.split("|")[0][1:].strip())
            accounts[person] += amount
        transactions[person].pop(index)
        update_all()

    tk.Button(frame, text="Deposit", font=("Arial", 14), command=do_deposit).pack(pady=3)
    tk.Button(frame, text="Withdraw", font=("Arial", 14), command=do_withdraw).pack(pady=3)
    tk.Button(frame, text="Delete Selected Transaction", font=("Arial", 12),
              command=delete_transaction, fg="red").pack(pady=6)

    return frame, balance_label, listbox

# Main App
app = tk.Tk()
app.title("FOUZ Family Ledger Software")
app.geometry("750x850")

container = tk.Frame(app)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Create initial accounts
for name in accounts:
    page, balance_label, listbox = create_person_page(name)
    account_pages[name] = (page, balance_label, listbox)
    page.grid(row=0, column=0, sticky="nsew")

# Bank page
bank_page = tk.Frame(container)
bank_title = tk.Label(bank_page, text="Bank Account", font=("Arial", 22, "bold"))
bank_title.pack(pady=20)

bank_balance = tk.Label(bank_page, font=("Arial", 20))
bank_balance.pack(pady=10)

# --- Add / Delete account section ---
account_frame = tk.Frame(bank_page)
account_frame.pack(pady=20)

# Add Account
tk.Label(account_frame, text="New Account Name:", font=("Arial", 14)).grid(row=0, column=0, padx=5)
new_account_entry = tk.Entry(account_frame, font=("Arial", 14))
new_account_entry.grid(row=0, column=1, padx=5)

tk.Label(account_frame, text="Initial Balance:", font=("Arial", 14)).grid(row=1, column=0, padx=5)
new_balance_entry = tk.Entry(account_frame, font=("Arial", 14))
new_balance_entry.grid(row=1, column=1, padx=5)

def add_new_account():
    name = new_account_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Account name cannot be empty")
        return
    if name in accounts:
        messagebox.showerror("Error", "Account already exists")
        return
    try:
        balance = int(new_balance_entry.get()) if new_balance_entry.get() else 0
    except:
        messagebox.showerror("Error", "Initial balance must be a number")
        return

    accounts[name] = balance
    transactions[name] = []
    page, balance_label, listbox = create_person_page(name)
    account_pages[name] = (page, balance_label, listbox)
    page.grid(row=0, column=0, sticky="nsew")

    # Add nav button
    btn = tk.Button(nav, text=name, font=("Arial", 14), command=lambda n=name: show_frame(account_pages[n][0]))
    btn.pack(side="left", expand=True)
    nav_buttons[name] = btn

    new_account_entry.delete(0, tk.END)
    new_balance_entry.delete(0, tk.END)
    messagebox.showinfo("Success", f"Account '{name}' added successfully!")
    update_all()

tk.Button(account_frame, text="Add Account", font=("Arial", 14), command=add_new_account, fg="green").grid(row=2, column=0, columnspan=2, pady=10)

# Delete Account
tk.Label(account_frame, text="Delete Account Name:", font=("Arial", 14)).grid(row=3, column=0, padx=5)
delete_account_entry = tk.Entry(account_frame, font=("Arial", 14))
delete_account_entry.grid(row=3, column=1, padx=5)

def delete_account():
    name = delete_account_entry.get().strip()
    if name not in accounts:
        messagebox.showerror("Error", "Account does not exist")
        return
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete account '{name}'? This will remove all transactions and balance."):
        del accounts[name]
        del transactions[name]
        account_pages[name][0].destroy()
        del account_pages[name]
        nav_buttons[name].destroy()
        del nav_buttons[name]
        delete_account_entry.delete(0, tk.END)
        messagebox.showinfo("Deleted", f"Account '{name}' has been deleted.")
        update_all()

tk.Button(account_frame, text="Delete Account", font=("Arial", 14), command=delete_account, fg="red").grid(row=4, column=0, columnspan=2, pady=10)

# Place bank page
bank_page.grid(row=0, column=0, sticky="nsew")

# Navigation
nav = tk.Frame(app)
nav.pack(side="bottom", fill="x")

# Buttons for initial accounts and bank
for name in accounts:
    btn = tk.Button(nav, text=name, font=("Arial", 14), command=lambda n=name: show_frame(account_pages[n][0]))
    btn.pack(side="left", expand=True)
    nav_buttons[name] = btn
tk.Button(nav, text="BANK", font=("Arial", 14), command=lambda: show_frame(bank_page)).pack(side="left", expand=True)

# Start with FOUZ page
show_frame(account_pages["FOUZ"][0])
app.mainloop()
