import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.core import load_data, save_data

class BudgetWindow:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        self.data = load_data()
        
        # Define color mapping with friendly names and hexcodes (for consistency with categories)
        self.color_mapping = {
            "Blue": "#4899d4",
            "Red": "#e74c3c",
            "Green": "#2ecc71",
            "Yellow": "#f1c40f",
            "Purple": "#9b59b6",
            "Orange": "#e67e22",
            "Gray": "#95a5a6"
        }
        
        # Configure styles to match dashboard
        self.configure_styles()
        
        # Header with title
        title_frame = ttk.Frame(self.frame, style='Header.TFrame')
        title_frame.pack(fill=tk.X)
        ttk.Label(title_frame, text="Budget Management", font=("Arial", 16, "bold"), 
                  foreground="white", background="#1e2a3a").pack(pady=10, padx=15, anchor=tk.W)
        
        # Main container
        main_container = ttk.Frame(self.frame, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Budget Table
        table_container = ttk.Frame(main_container, style='Panel.TFrame')
        table_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Table header
        header_frame = ttk.Frame(table_container, style='PanelHeader.TFrame')
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Budget Overview", style='PanelHeader.TLabel').pack(pady=8, padx=10, anchor=tk.W)
        
        # Table content
        content_frame = ttk.Frame(table_container, style='PanelContent.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable frame for the table
        self.canvas = tk.Canvas(content_frame, background="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        self.table_frame = ttk.Frame(self.canvas, style='PanelContent.TFrame')
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_frame, anchor=tk.NW)
        
        # Right panel - Set Budget Form
        form_container = ttk.Frame(main_container, style='Panel.TFrame', width=300)
        form_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        form_container.pack_propagate(False)  # Prevent shrinking
        
        # Form header
        header_frame = ttk.Frame(form_container, style='PanelHeader.TFrame')
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Set Budget", style='PanelHeader.TLabel').pack(pady=8, padx=10, anchor=tk.W)
        
        # Form content
        form_frame = ttk.Frame(form_container, style='PanelContent.TFrame', padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Select Category", style='Label.TLabel').pack(anchor=tk.W, pady=(5, 2))
        self.category_combobox = ttk.Combobox(form_frame, values=self.data.get("categories", []))
        self.category_combobox.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Enter Budget Amount (Rs)", style='Label.TLabel').pack(anchor=tk.W, pady=(5, 2))
        self.budget_entry = ttk.Entry(form_frame)
        self.budget_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Add Set Budget button
        ttk.Button(form_frame, text="Set Budget", command=self.set_budget, 
                  style='Blue.TButton').pack(fill=tk.X, pady=(15, 0))
        
        # Add a summary section at the bottom of the form
        summary_frame = ttk.Frame(form_frame, padding=(0, 20, 0, 0))
        summary_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Separator(summary_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Label(summary_frame, text="Total Budget:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.total_budget_label = ttk.Label(summary_frame, text="Rs0")
        self.total_budget_label.pack(anchor=tk.W)
        
        ttk.Label(summary_frame, text="Total Spent:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.total_spent_label = ttk.Label(summary_frame, text="Rs0")
        self.total_spent_label.pack(anchor=tk.W)
        
        ttk.Label(summary_frame, text="Total Remaining:", font=("Arial", 11, "bold")).pack(anchor=tk.W)
        self.total_remaining_label = ttk.Label(summary_frame, text="Rs0")
        self.total_remaining_label.pack(anchor=tk.W)
        
        # Add initial data for demo purposes if needed
        self.initialize_demo_data()
        
        # Populate the table with data
        self.update_budget_table()

    def on_canvas_configure(self, event):
        # Update the scrollable region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Update the canvas window width to match the canvas width
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())

    def initialize_demo_data(self):
        # Only initialize if the data doesn't exist yet
        if "budget" not in self.data or not self.data["budget"]:
            # Example budget data based on the screenshot
            demo_budgets = {
                "Housing": 1500,
                "Food": 600,
                "Transportation": 400,
                "Utilities": 300,
                "Entertainment": 200,
                "Shopping": 300,
                "Healthcare": 200,
                "Personal Care": 100
            }
            
            # Add these categories if they don't exist
            if "categories" not in self.data:
                self.data["categories"] = []
                
            for category in demo_budgets.keys():
                if category not in self.data["categories"]:
                    self.data["categories"].append(category)
            
            # Initialize budget dictionary
            if "budget" not in self.data:
                self.data["budget"] = {}
                
            # Add budget values
            for category, amount in demo_budgets.items():
                self.data["budget"][category] = amount
                
            # Save to file
            save_data(self.data)
            
            # Update the category combobox
            self.category_combobox['values'] = self.data.get("categories", [])

    def configure_styles(self):
        style = ttk.Style()
        
        # Main header style
        style.configure('Header.TFrame', background='#1e2a3a')
        
        # Panel styles
        style.configure('Panel.TFrame', background='white', relief='solid', borderwidth=1)
        style.configure('PanelHeader.TFrame', background='#4899d4')
        style.configure('PanelHeader.TLabel', font=('Arial', 12, 'bold'), 
                        background='#4899d4', foreground='white')
        style.configure('PanelContent.TFrame', background='white')
        
        # Table header style
        style.configure('TableHeader.TLabel', font=('Arial', 10, 'bold'), background='white')
        
        # Form elements
        style.configure('Label.TLabel', font=('Arial', 10), background='white')
        style.configure('Entry.TEntry', font=('Arial', 10))
        
        # Button styles
        style.configure('Blue.TButton', font=('Arial', 10, 'bold'))
        style.map('Blue.TButton',
                  background=[('!active', '#4899d4'), ('active', '#3a87c4')],
                  foreground=[('!active', 'white'), ('active', 'white')])
                  
        # Edit button style
        style.configure('Edit.TButton', font=('Arial', 9))

    def create_table_headers(self):
        # Create table header
        header_frame = ttk.Frame(self.table_frame, style='PanelContent.TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Create separator line above the headers
        ttk.Separator(self.table_frame, orient='horizontal').pack(fill=tk.X, padx=10)
        
        # Create header columns
        ttk.Label(header_frame, text="Category", style='TableHeader.TLabel', width=15, anchor='w').grid(row=0, column=0, padx=5)
        ttk.Label(header_frame, text="Budget", style='TableHeader.TLabel', width=10, anchor='e').grid(row=0, column=1, padx=5)
        ttk.Label(header_frame, text="Spent", style='TableHeader.TLabel', width=10, anchor='e').grid(row=0, column=2, padx=5)
        ttk.Label(header_frame, text="Remaining", style='TableHeader.TLabel', width=10, anchor='e').grid(row=0, column=3, padx=5)
        ttk.Label(header_frame, text="% of Total", style='TableHeader.TLabel', width=10, anchor='e').grid(row=0, column=4, padx=5)
        
        # Add a separator after the headers
        ttk.Separator(self.table_frame, orient='horizontal').pack(fill=tk.X, padx=10)

    def update_budget_table(self):
        # Clear existing table rows
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
        # Create table headers
        self.create_table_headers()
            
        # Check if budget data exists
        if "budget" not in self.data:
            self.data["budget"] = {}
            
        # Calculate totals and get transactions data
        transactions = self.data.get("transactions", [])
        
        # Get categories from both the categories list and the budget dictionary
        all_categories = set(self.data.get("categories", []))
        all_categories.update(self.data.get("budget", {}).keys())
        all_categories = sorted(list(all_categories))
        
        # Prepare a dictionary to track spending per category
        spent_by_category = {}
        for category in all_categories:
            spent_by_category[category] = 0
            
        # Sum up transactions by category
        for transaction in transactions:
            category = transaction.get("category", "")
            if category in spent_by_category:
                spent_by_category[category] += transaction.get("amount", 0)
        
        # Calculate total budget
        total_budget = sum(self.data["budget"].get(category, 0) for category in all_categories)
        
        # Add rows for each category
        row_index = 0
        total_spent = 0
        total_remaining = 0
        
        # Example spending data based on the screenshot
        demo_spending = {
            "Housing": 1200,
            "Food": 450,
            "Transportation": 350,
            "Utilities": 280,
            "Entertainment": 180,
            "Shopping": 420,
            "Healthcare": 50,
            "Personal Care": 85
        }
        
        # If we have no real transactions but have budget data, use the demo spending
        if not transactions and self.data.get("budget"):
            for category, amount in demo_spending.items():
                if category in all_categories:
                    spent_by_category[category] = amount
        
        for category in all_categories:
            budget_amount = self.data["budget"].get(category, 0)
            
            # Skip categories with no budget
            if budget_amount == 0:
                continue
                
            spent_amount = spent_by_category.get(category, 0)
            remaining = budget_amount - spent_amount
            
            # Update totals
            total_spent += spent_amount
            total_remaining += remaining
            
            # Create row frame
            row_frame = ttk.Frame(self.table_frame, style='PanelContent.TFrame')
            row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Determine color index (rotate through colors based on row index)
            color_index = row_index % len(self.color_mapping)
            color_name = list(self.color_mapping.keys())[color_index]
            color_hex = self.color_mapping[color_name]
            
            # Get icon based on category
            icon = self.get_icon_for_category(category)
            
            # Create a frame with the category color
            category_cell = ttk.Frame(row_frame)
            category_cell.grid(row=0, column=0, padx=5, sticky='w')
            
            # Color indicator
            color_indicator = tk.Frame(category_cell, width=5, height=20, background=color_hex)
            color_indicator.pack(side=tk.LEFT, padx=(0, 5))
            
            # Category label with icon
            ttk.Label(category_cell, text=f"{icon} {category}", width=14, anchor='w').pack(side=tk.LEFT)
            
            # Budget amount with edit button
            budget_cell = ttk.Frame(row_frame)
            budget_cell.grid(row=0, column=1, padx=5)
            
            ttk.Label(budget_cell, text=f"Rs{budget_amount:.2f}", width=8, anchor='e').pack(side=tk.LEFT)
            
            edit_btn = ttk.Button(budget_cell, text="✏️", width=3, 
                                 command=lambda cat=category: self.edit_budget(cat),
                                 style='Edit.TButton')
            edit_btn.pack(side=tk.LEFT)
            
            # Spent amount
            ttk.Label(row_frame, text=f"Rs{spent_amount:.2f}", width=10, anchor='e').grid(row=0, column=2, padx=5)
            
            # Remaining amount (with color indicator if negative)
            remaining_label = ttk.Label(row_frame, text=f"Rs{remaining:.2f}", width=10, anchor='e')
            if remaining < 0:
                remaining_label.configure(foreground="red")
            remaining_label.grid(row=0, column=3, padx=5)
            
            # Percentage of total budget
            percentage = (budget_amount / total_budget * 100) if total_budget > 0 else 0
            ttk.Label(row_frame, text=f"{percentage:.1f}%", width=10, anchor='e').grid(row=0, column=4, padx=5)
            
            # Add a separator after each row
            ttk.Separator(self.table_frame, orient='horizontal').pack(fill=tk.X, padx=10)
            
            row_index += 1
            
        # Add total row
        total_row = ttk.Frame(self.table_frame, style='PanelContent.TFrame')
        total_row.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(total_row, text="Total", font=("Arial", 11, "bold"), width=15, anchor='w').grid(row=0, column=0, padx=5)
        ttk.Label(total_row, text=f"Rs{total_budget:.2f}", font=("Arial", 11, "bold"), width=10, anchor='e').grid(row=0, column=1, padx=5)
        ttk.Label(total_row, text=f"Rs{total_spent:.2f}", font=("Arial", 11, "bold"), width=10, anchor='e').grid(row=0, column=2, padx=5)
        
        remaining_total = ttk.Label(total_row, text=f"Rs{total_remaining:.2f}", font=("Arial", 11, "bold"), width=10, anchor='e')
        if total_remaining < 0:
            remaining_total.configure(foreground="red")
        remaining_total.grid(row=0, column=3, padx=5)
        
        ttk.Label(total_row, text="100%", font=("Arial", 11, "bold"), width=10, anchor='e').grid(row=0, column=4, padx=5)
        
        # Update the summary labels
        self.total_budget_label.config(text=f"Rs{total_budget:.2f}")
        self.total_spent_label.config(text=f"Rs{total_spent:.2f}")
        self.total_remaining_label.config(text=f"Rs{total_remaining:.2f}")
        if total_remaining < 0:
            self.total_remaining_label.config(foreground="red")
        else:
            self.total_remaining_label.config(foreground="black")
        
        # Update the canvas scrollable region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_icon_for_category(self, category):
        # Map categories to icons (matching your example)
        icon_map = {
            "Housing": "🏠",
            "Food": "🍔",
            "Transportation": "🚗",
            "Utilities": "💡",
            "Entertainment": "🎬",
            "Shopping": "🛍️",
            "Healthcare": "🏥",
            "Personal Care": "👤"
        }
        return icon_map.get(category, "📊")  # Default icon

    def set_budget(self):
        category = self.category_combobox.get()
        budget_text = self.budget_entry.get().strip()
        
        if not category:
            messagebox.showerror("Error", "Please select a category")
            return
            
        if not budget_text:
            messagebox.showerror("Error", "Please enter a budget amount")
            return
            
        try:
            budget_amount = float(budget_text)
            if budget_amount < 0:
                messagebox.showerror("Error", "Budget amount cannot be negative")
                return
        except ValueError:
            messagebox.showerror("Error", "Budget amount must be a number")
            return
            
        # Initialize budget dict if it doesn't exist
        if "budget" not in self.data:
            self.data["budget"] = {}
            
        # Set budget for selected category
        self.data["budget"][category] = budget_amount
        save_data(self.data)
        
        # Update the table
        self.update_budget_table()
        
        # Clear inputs
        self.budget_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Budget for {category} has been set to Rs{budget_amount:.2f}")

    def edit_budget(self, category):
        current_budget = self.data.get("budget", {}).get(category, 0)
        new_budget = simpledialog.askfloat("Edit Budget", 
                                           f"Enter new budget amount for {category}:",
                                           initialvalue=current_budget,
                                           minvalue=0)
        
        if new_budget is not None:
            # Initialize budget dict if it doesn't exist
            if "budget" not in self.data:
                self.data["budget"] = {}
                
            # Update budget for category
            self.data["budget"][category] = new_budget
            save_data(self.data)
            
            # Update the table
            self.update_budget_table()