import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "data.json"

# ---------------- DATA STORAGE ---------------- #

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

def load_data():
    global accounts
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            accounts = json.load(file)
    else:
        accounts = {
            "FOUZ": [],
            "MOM": [],
            "FIDA": []
        }

# ---------------- LOGIC ---------------- #

def get_account_balance(name):
    return sum(t["amount"] for t in accounts[name])

def get_bank_balance():
    return sum(get_account_balance(acc) for acc in accounts)

def add_transaction(account, amount, note):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaction = {
        "amount": amount,
        "note": note,
        "time": time_now
    }

    accounts[account].append(transaction)
    save_data()
    refresh()

def delete_transaction(account, index):
    del accounts[account][index]
    save_data()
    refresh()

def add_account():
    name = simpledialog.askstring("New Account", "Enter account name:")
    if name and name not in accounts:
        accounts[name] = []
        save_data()
        refresh()

def delete_account(account):
    if messagebox.askyesno("Confirm Delete", f"Delete account {account}?"):
        del accounts[account]
        save_data()
        refresh()

# ---------------- GUI ---------------- #

def refresh():
    for widget in main_frame.winfo_children():
        widget.destroy()
    create_ui()

def create_ui():
    row = 0

    bank_balance = get_bank_balance()
    tk.Label(main_frame, text=f"BANK BALANCE : ₹ {bank_balance}", font=("Arial", 18, "bold")).grid(row=row, column=0, columnspan=4, pady=10)
    row += 1

    for acc in accounts:
        balance = get_account_balance(acc)

        tk.Label(main_frame, text=f"{acc} Balance: ₹ {balance}", font=("Arial", 14, "bold")).grid(row=row, column=0, sticky="w")
        tk.Button(main_frame, text="Delete Account", command=lambda a=acc: delete_account(a)).grid(row=row, column=3)
        row += 1

        listbox = tk.Listbox(main_frame, width=80, height=5)
        listbox.grid(row=row, column=0, columnspan=4)

        for i, t in enumerate(accounts[acc]):
            sign = "+" if t["amount"] >= 0 else ""
            listbox.insert(tk.END, f"{i+1}. {sign}{t['amount']} | {t['note']} | {t['time']}")

        row += 1

        amount_entry = tk.Entry(main_frame)
        amount_entry.grid(row=row, column=0)

        note_entry = tk.Entry(main_frame, width=40)
        note_entry.grid(row=row, column=1)

        tk.Button(main_frame, text="Deposit",
                  command=lambda a=acc, e=amount_entry, n=note_entry:
                  add_transaction(a, float(e.get()), n.get())).grid(row=row, column=2)

        tk.Button(main_frame, text="Withdraw",
                  command=lambda a=acc, e=amount_entry, n=note_entry:
                  add_transaction(a, -float(e.get()), n.get())).grid(row=row, column=3)

        row += 1

        tk.Button(main_frame, text="Delete Selected Transaction",
                  command=lambda a=acc, lb=listbox:
                  delete_transaction(a, lb.curselection()[0]) if lb.curselection() else None).grid(row=row, column=0, pady=5)

        row += 2

    tk.Button(main_frame, text="Add New Account", font=("Arial", 12, "bold"), command=add_account).grid(row=row, column=0, pady=20)

# ---------------- START APP ---------------- #

load_data()

root = tk.Tk()
root.title("Ledger Accounting Software")
root.geometry("900x700")

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

create_ui()

root.mainloop()
