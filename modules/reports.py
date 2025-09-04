import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # For date range selection
import csv
from fpdf import FPDF  # For PDF export
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from database.core import load_data
from modules.utils import calculate_totals


class ReportWindow:
    def __init__(self, notebook):
        # Main frame
        self.frame = ttk.Frame(notebook)
        self.data = load_data()

        # Setup styles for consistent look
        self.setup_styles()

        # Configure grid layout
        self.frame.columnconfigure(0, weight=1)  # Left column (Financial Summary + Chart)
        self.frame.columnconfigure(1, weight=2)  # Right column (Recent Transactions + Buttons)
        self.frame.rowconfigure(0, weight=1)  # Financial Summary
        self.frame.rowconfigure(1, weight=1)  # Expense Breakdown Chart
        self.frame.rowconfigure(2, weight=1)  # Recent Transactions + Buttons

        # Create main panels
        self.create_financial_summary_panel()
        self.create_expense_breakdown_panel()
        self.create_transaction_history_panel()

        # Initial data load
        self.update_report()

    def get_recent_transactions(self, limit=5):
        """
        Retrieve the most recent transactions.

        Args:
            limit (int): Number of transactions to retrieve. Default is 5.

        Returns:
            list: A list of dictionaries containing transaction details.
        """
        all_transactions = []

        # Process income transactions
        for income in self.data["income"]:
            all_transactions.append({
                "date": income["timestamp"].split()[0],  # Extract date part
                "category": "-",  # No category for income
                "amount": income["amount"],
                "type": "Income"
            })

        # Process expense transactions
        for expense in self.data["expenses"]:
            all_transactions.append({
                "date": expense["timestamp"].split()[0],  # Extract date part
                "category": expense["category"],
                "amount": expense["amount"],
                "type": "Expense"
            })

        # Sort by date (most recent first)
        all_transactions.sort(key=lambda x: x["date"], reverse=True)

        # Return the most recent transactions
        return all_transactions[:limit]

    def setup_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()

        # Panel style
        style.configure("Panel.TFrame", background="#ffffff", relief="solid", borderwidth=1)

        # Panel header style
        style.configure("PanelTitle.TLabel",
                       background="#3498db",
                       foreground="white",
                       font=("Helvetica", 12, "bold"),
                       padding=5)

        # Data labels
        style.configure("DataHeading.TLabel",
                       font=("Helvetica", 11, "bold"))

        # Item labels
        style.configure("DataItem.TLabel",
                       font=("Helvetica", 10))

        # Positive and negative values
        style.configure("Positive.TLabel",
                       foreground="#27ae60",
                       font=("Helvetica", 11, "bold"))

        style.configure("Negative.TLabel",
                       foreground="#e74c3c",
                       font=("Helvetica", 11, "bold"))

        # Button style
        style.configure("Action.TButton",
                       font=("Helvetica", 10))

    def create_panel(self, row, column, rowspan=1, columnspan=1, title=""):
        """Helper method to create a consistent panel with title bar"""
        # Create outer frame
        panel = ttk.Frame(self.frame, style="Panel.TFrame")
        panel.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan,
                   padx=10, pady=10, sticky="nsew")

        # Title bar that spans the width
        title_bar = ttk.Label(panel, text=title, style="PanelTitle.TLabel")
        title_bar.pack(fill=tk.X)

        # Content frame
        content = ttk.Frame(panel)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        return panel, content

    def create_financial_summary_panel(self):
        """Create the financial summary panel"""
        panel, content = self.create_panel(0, 0, title="Financial Summary")

        # Create fields for summary data
        ttk.Label(content, text="Total Income:", style="DataHeading.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.income_label = ttk.Label(content, style="DataItem.TLabel")
        self.income_label.grid(row=0, column=1, sticky=tk.E, pady=5)

        ttk.Label(content, text="Total Expenses:", style="DataHeading.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.expenses_label = ttk.Label(content, style="DataItem.TLabel")
        self.expenses_label.grid(row=1, column=1, sticky=tk.E, pady=5)

        ttk.Separator(content, orient=tk.HORIZONTAL).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Label(content, text="Net Balance:", style="DataHeading.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.balance_label = ttk.Label(content)
        self.balance_label.grid(row=3, column=1, sticky=tk.E, pady=5)

        # Add refresh button
        refresh_btn = ttk.Button(content, text="Refresh Report",
                                 style="Action.TButton", command=self.update_report)
        refresh_btn.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=10)

    def create_transaction_history_panel(self):
        """Create the transaction history panel"""
        panel, content = self.create_panel(0, 1, rowspan=2, title="Recent Transactions")

        # Create Treeview for transactions
        columns = ("date", "category", "amount", "type")
        self.transaction_tree = ttk.Treeview(content, columns=columns, show="headings", height=15)

        # Configure columns
        self.transaction_tree.heading("date", text="Date")
        self.transaction_tree.heading("category", text="Category")
        self.transaction_tree.heading("amount", text="Amount")
        self.transaction_tree.heading("type", text="Type")

        self.transaction_tree.column("date", width=100)
        self.transaction_tree.column("category", width=150)
        self.transaction_tree.column("amount", width=100, anchor=tk.E)
        self.transaction_tree.column("type", width=100)

        # Style for different transaction types
        self.transaction_tree.tag_configure('income', background='#e6ffe6')
        self.transaction_tree.tag_configure('expense', background='#fff0f0')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(content, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscroll=scrollbar.set)

        # Layout
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add date range filter and buttons below the Treeview
        self.create_date_range_filter(content)

    def create_date_range_filter(self, parent):
        """Create date range filter for transactions"""
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text="From:").pack(side=tk.LEFT, padx=5)
        self.start_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.start_date.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.end_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.end_date.pack(side=tk.LEFT, padx=5)

        # Buttons stacked vertically
        button_frame = ttk.Frame(filter_frame)
        button_frame.pack(side=tk.LEFT, padx=5)

        filter_btn = ttk.Button(button_frame, text="Filter", command=self.filter_transactions)
        filter_btn.pack(pady=5)

        export_csv_btn = ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        export_csv_btn.pack(pady=5)

        export_pdf_btn = ttk.Button(button_frame, text="Export to PDF", command=self.export_to_pdf)
        export_pdf_btn.pack(pady=5)

    def filter_transactions(self):
        """Filter transactions based on date range"""
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()

        filtered_transactions = []
        for transaction in self.data["income"] + self.data["expenses"]:
            transaction_date = datetime.datetime.strptime(transaction["timestamp"].split()[0], "%Y-%m-%d").date()
            if start_date <= transaction_date <= end_date:
                filtered_transactions.append({
                    "date": transaction["timestamp"].split()[0],  # Extract date part
                    "category": transaction.get("category", "-"),
                    "amount": transaction["amount"],
                    "type": "Income" if "income" in transaction else "Expense"
                })

        self.update_transaction_list(filtered_transactions)

    def export_to_csv(self):
        """Export transactions to CSV"""
        filename = "transactions_export.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Type"])
            for transaction in self.transaction_tree.get_children():
                values = self.transaction_tree.item(transaction, 'values')
                writer.writerow(values)
        messagebox.showinfo("Export Successful", f"Transactions exported to {filename}")

    def export_to_pdf(self):
        """Export transactions to PDF"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Transaction Report", ln=True, align='C')
        pdf.ln(10)

        for transaction in self.transaction_tree.get_children():
            values = self.transaction_tree.item(transaction, 'values')
            pdf.cell(200, 10, txt=f"{values[0]} | {values[1]} | {values[2]} | {values[3]}", ln=True)

        pdf.output("transactions_export.pdf")
        messagebox.showinfo("Export Successful", "Transactions exported to transactions_export.pdf")

    def create_expense_breakdown_panel(self):
        """Create the expense breakdown chart panel"""
        panel, content = self.create_panel(1, 0, title="Expense Breakdown")

        # Create a frame for the matplotlib figure
        self.chart_frame = ttk.Frame(content)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

    def update_report(self):
        """Update all panels with the latest data"""
        # Reload data
        self.data = load_data()

        # Calculate totals
        totals = calculate_totals(self.data)

        # Update financial summary
        self.income_label.config(text=f"Rs{totals['income']:,.2f}")
        self.expenses_label.config(text=f"Rs{totals['expenses']:,.2f}")

        # Format balance with appropriate style based on value
        if totals['balance'] >= 0:
            self.balance_label.config(
                text=f"Rs{totals['balance']:,.2f}",
                style="Positive.TLabel")
        else:
            self.balance_label.config(
                text=f"Rs{totals['balance']:,.2f}",
                style="Negative.TLabel")

        # Update transaction history
        self.update_transaction_list()

        # Update expense breakdown chart
        self.update_expense_chart()

    def update_transaction_list(self, transactions=None):
        """Update the transaction tree with the latest transactions"""
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

        # Use provided transactions or load all transactions
        if transactions is None:
            transactions = self.get_recent_transactions(limit=20)

        # Add to treeview
        for transaction in transactions:
            tag = 'income' if transaction["type"] == "Income" else 'expense'
            amount_text = f"Rs{transaction['amount']:,.2f}"

            self.transaction_tree.insert(
                "", "end",
                values=(
                    transaction["date"],
                    transaction["category"],
                    amount_text,
                    transaction["type"]
                ),
                tags=(tag,)
            )

    def update_expense_chart(self):
        """Update the expense breakdown chart"""
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Get expense breakdown data
        categories, expenses = self.get_expense_breakdown()

        if not categories:  # No expense data
            ttk.Label(self.chart_frame, text="No expense data available",
                      style="DataItem.TLabel").pack(pady=20)
            return

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

        # Generate colors
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
        if len(categories) > len(colors):
            # If more categories than colors, cycle through the colors
            colors = colors * (len(categories) // len(colors) + 1)

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            expenses,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(categories)]
        )

        # Customize pie chart appearance
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color('white')

        ax.set_title("Expense Breakdown")
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Create legend
        ax.legend(
            wedges,
            categories,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        # Create canvas and add to frame
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_expense_breakdown(self):
        """
        Retrieves the expense breakdown by category.

        Returns:
            tuple: A tuple containing lists of categories and corresponding expenses.
        """
        categories = []
        expenses = []
        for expense in self.data["expenses"]:
            category = expense['category']
            amount = expense['amount']
            if category in categories:
                expenses[categories.index(category)] += amount
            else:
                categories.append(category)
                expenses.append(amount)
        return categories, expenses