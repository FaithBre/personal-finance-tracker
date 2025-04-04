import tkinter as tk
from tkinter import ttk, messagebox

# Global list to store transactions
transactions = []
budget_limit = 15000  # Budget limit for alerts

def add_transaction():
    """Adds a new transaction to the list"""
    category = category_entry.get()
    amount = amount_entry.get()
    transaction_type = "Income" if income_var.get() else "Expense"

    # Validate input: Ensure category and amount are provided
    if not category or not amount:
        messagebox.showwarning("Input Error", "Please enter category and amount.")
        return

    # Validate input: Ensure amount is a number
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number.")
        return

    # Add transaction to the list
    transactions.append({"category": category, "amount": amount, "type": transaction_type})
    update_transaction_list()
    update_summary()
    check_budget_alert()

    # Clear input fields after adding transaction
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def delete_transaction():
    """Deletes the selected transaction from the list"""
    selected_index = transaction_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Selection Error", "Please select a transaction to delete.")
        return

    # Remove transaction based on selected index
    transactions.pop(selected_index[0])
    update_transaction_list()
    update_summary()
    check_budget_alert()

def filter_category():
    """Filters transactions based on entered category"""
    category = category_entry.get()
    if not category:
        messagebox.showwarning("Filter Error", "Enter a category to filter.")
        return

    # Show only matching transactions
    filtered_transactions = [t for t in transactions if t["category"].lower() == category.lower()]
    update_transaction_list(filtered_transactions)

def update_transaction_list(filtered_transactions=None):
    """Updates the transaction listbox with current transactions"""
    transaction_listbox.delete(0, tk.END)
    display_transactions = filtered_transactions if filtered_transactions else transactions

    for transaction in display_transactions:
        transaction_listbox.insert(
            tk.END, f"{transaction['category']} - {transaction['type']}: Kshs{transaction['amount']}"
        )

def update_summary():
    """Calculates and updates total income, expenses, and balance"""
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = total_income - total_expenses

    # Update UI labels with calculated values
    income_label.config(text=f"Total Income: Kshs{total_income}")
    expense_label.config(text=f"Total Expenses: Kshs{total_expenses}")
    balance_label.config(text=f"Balance: Kshs{balance}")

def check_budget_alert():
    """Checks if expenses exceed the budget limit and shows a warning"""
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    if total_expenses > budget_limit:
        messagebox.showwarning("Budget Alert", f"Warning: Expenses exceeded the budget limit of Kshs{budget_limit}!")
        
# GUI Setup
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("500x450")
root.configure(bg="#999")  # Set background color

# Title Label
title_label = tk.Label(root, text="Personal Finance Tracker", font=("TrebuchetMS", 14, "bold"), bg="royalblue")
title_label.pack(fill="x")

# Input Section Frame
input_frame = tk.Frame(root, bg="#999")
input_frame.pack(pady=10)

# Category Input
tk.Label(input_frame, text="Category:", bg="#999", fg="white").grid(row=0, column=0)
category_entry = tk.Entry(input_frame)
category_entry.grid(row=0, column=1, padx=5)

# Amount Input
tk.Label(input_frame, text="Amount:", bg="#999", fg="white").grid(row=1, column=0)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=1, column=1, padx=5)

# Transaction Type (Income/Expense)
income_var = tk.BooleanVar(value=True)
tk.Radiobutton(input_frame, text="Income", variable=income_var, value=True, bg="#333", fg="white").grid(row=2, column=0)
tk.Radiobutton(input_frame, text="Expense", variable=income_var, value=False, bg="#333", fg="white").grid(row=2, column=1)

# Buttons for Actions
btn_frame = tk.Frame(root, bg="#666")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Transaction", command=add_transaction).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete Selected", command=delete_transaction).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Filter Category", command=filter_category).grid(row=0, column=2, padx=5)

# Listbox to Display Transactions
transaction_listbox = tk.Listbox(root, height=10, width=50)
transaction_listbox.pack(pady=10)

# Summary Section
summary_frame = tk.Frame(root, bg="#666")
summary_frame.pack(fill="x", pady=5)

# Labels for Summary
income_label = tk.Label(summary_frame, text="Total Income: Kshs 0", bg="darkgreen", fg="white")
income_label.pack(fill="x")

expense_label = tk.Label(summary_frame, text="Total Expenses: Kshs 0", bg="darkred", fg="white")
expense_label.pack(fill="x")

balance_label = tk.Label(summary_frame, text="Balance: Kshs 0", bg="navyblue", fg="white")
balance_label.pack(fill="x")

# Run the application
root.mainloop()
