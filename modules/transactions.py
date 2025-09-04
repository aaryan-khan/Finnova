# transaction.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.core import load_data, save_data
from modules.utils import get_current_timestamp

def calculate_total_savings(data):
    """
    Calculate total savings based on income and expenses.
    """
    total_income = sum(income["amount"] for income in data["income"])
    total_expenses = sum(expense["amount"] for expense in data["expenses"])
    savings = total_income - total_expenses
    return savings

class TransactionWindow:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        # self.data = load_data() # Removed

        # Configure the frame to center its contents
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create a frame for the buttons at the top
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Transaction Type Selection
        ttk.Label(self.button_frame, text="Transaction Type:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Bigger buttons for Expense and Income
        self.transaction_type = tk.StringVar(value="expense")
        ttk.Button(self.button_frame, text="Expense", command=self.show_expense_form, width=15).grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        ttk.Button(self.button_frame, text="Income", command=self.show_income_form, width=15).grid(row=0, column=2, padx=5, pady=10, sticky="ew")

        # Center-align the button frame
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        # Create a frame for the form below the buttons
        self.transaction_form_frame = ttk.Frame(self.frame)
        self.transaction_form_frame.grid(row=1, column=0, padx=(10, 20), pady=10, sticky="nsew")  # Add right padding (20)

        # Center-align the form frame
        self.transaction_form_frame.grid_columnconfigure(0, weight=1)
        self.transaction_form_frame.grid_columnconfigure(3, weight=1)

        # Show the expense form by default
        self.show_expense_form()

    def show_expense_form(self):
        self.clear_form()
        ttk.Label(self.transaction_form_frame, text="Amount:").grid(row=0, column=1, padx=(10, 20), pady=5, sticky="w")  # Add right padding (20)
        self.amount_entry = ttk.Entry(self.transaction_form_frame)
        self.amount_entry.grid(row=0, column=2, padx=(10, 20), pady=5, sticky="ew")  # Add right padding (20)

        ttk.Label(self.transaction_form_frame, text="Category:").grid(row=1, column=1, padx=(10, 20), pady=5, sticky="w")  # Add right padding (20)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            self.transaction_form_frame,
            textvariable=self.category_var,  # Link the Combobox to category_var
            values=load_data()["categories"] # Modified to load data
        )
        self.category_combobox.grid(row=1, column=2, padx=(10, 20), pady=5, sticky="ew")  # Add right padding (20)

        ttk.Label(self.transaction_form_frame, text="Description:").grid(row=2, column=1, padx=(10, 20), pady=5, sticky="w")  # Add right padding (20)
        self.description_entry = ttk.Entry(self.transaction_form_frame)
        self.description_entry.grid(row=2, column=2, padx=(10, 20), pady=5, sticky="ew")  # Add right padding (20)

        ttk.Button(self.transaction_form_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=1, columnspan=2, padx=(10, 20), pady=10, sticky="ew")  # Add right padding (20)

    def show_income_form(self):
        self.clear_form()
        ttk.Label(self.transaction_form_frame, text="Amount:").grid(row=0, column=1, padx=(10, 20), pady=5, sticky="w")  # Add right padding (20)
        self.amount_entry = ttk.Entry(self.transaction_form_frame)
        self.amount_entry.grid(row=0, column=2, padx=(10, 20), pady=5, sticky="ew")  # Add right padding (20)

        ttk.Label(self.transaction_form_frame, text="Description:").grid(row=1, column=1, padx=(10, 20), pady=5, sticky="w")  # Add right padding (20)
        self.description_entry = ttk.Entry(self.transaction_form_frame)
        self.description_entry.grid(row=1, column=2, padx=(10, 20), pady=5, sticky="ew")  # Add right padding (20)

        ttk.Button(self.transaction_form_frame, text="Add Income", command=self.add_income).grid(row=2, column=1, columnspan=2, padx=(10, 20), pady=10, sticky="ew")  # Add right padding (20)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()  # Get the selected category from the Combobox
            description = self.description_entry.get()

            if category not in load_data()["categories"]: # modified to load data
                messagebox.showerror("Error", "Invalid category!")
                return

            if category in load_data()["budget"] and amount > load_data()["budget"][category]: # modified to load data
                messagebox.showwarning("Budget Alert", "This expense exceeds the set budget!")

            data = load_data() # Reload data
            data["expenses"].append({
                "timestamp": get_current_timestamp(),
                "amount": amount,
                "category": category,
                "description": description
            })
            save_data(data)

            messagebox.showinfo("Success", "Expense added successfully!")

            # Refresh the report window
            if hasattr(self, "report_window"):
                self.report_window.update_report()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount! Please enter a valid number.")

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()

            # Add income to the database
            data = load_data() # Reload data
            data["income"].append({
                "timestamp": get_current_timestamp(),
                "amount": amount,
                "description": description
            })
            save_data(data)

            messagebox.showinfo("Success", "Income added successfully!")

            # Refresh the report window
            if hasattr(self, "report_window"):
                self.report_window.update_report()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount! Please enter a valid number.")

    def clear_form(self):
        for widget in self.transaction_form_frame.winfo_children():
            widget.destroy()