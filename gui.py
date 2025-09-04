import tkinter as tk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.transactions import TransactionWindow
from modules.reports import ReportWindow
from modules.budget import BudgetWindow
from modules.categories import CategoriesWindow
from modules.goals.manager import GoalsWindow, get_goals
from assets.styles import set_theme

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finnova - Personal Finance Manager")
        self.root.geometry("1200x800")

        set_theme(self.root)

        # Main Frame Layout
        self.main_frame = tk.Frame(root, bg="#E8F0FF")  # Slightly lighter blue background
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with gradient effect
        self.header_frame = tk.Frame(self.main_frame, bg="#1C2E40")  # Darker blue for more depth
        self.header_frame.pack(fill=tk.X)

        self.header_label = tk.Label(self.header_frame,
                                     text="Finnova - Personal Finance Manager",
                                     font=("Helvetica Neue", 22, "bold"),  # Increased font size
                                     bg="#1C2E40",
                                     fg="white",
                                     pady=18)  # Increased padding
        self.header_label.pack(side=tk.LEFT, padx=25)  # Increased padding

        # Separator Frame (using grid) with gradient effect
        self.separator_frame = tk.Frame(self.main_frame,
                                         bg="#D0E0F0",  # Lighter blue for contrast
                                         height=36)  # Increased height
        self.separator_frame.pack(fill=tk.X)

        self.separator_frame.grid_columnconfigure(1, weight=1)

        self.welcome_label = tk.Label(self.separator_frame,
                                        text="Welcome to Finnova",
                                        font=("Helvetica Neue", 13, "bold"),  # Increased font size
                                        bg="#D0E0F0",
                                        fg="#1A2530")  # Darker text for better contrast
        self.welcome_label.grid(row=0, column=0, padx=25, pady=0, ipady=3, sticky=tk.W)

        self.date_label = tk.Label(self.separator_frame,
                                    text="",
                                    font=("Helvetica Neue", 13, "bold"),
                                    bg="#D0E0F0",
                                    fg="#1A2530")
        self.date_label.grid(row=0, column=1, pady=0, ipady=3)
        self.date_label.config(justify=tk.CENTER, height=1)

        self.time_label = tk.Label(self.separator_frame,
                                    text="",
                                    font=("Helvetica Neue", 13, "bold"),
                                    bg="#D0E0F0",
                                    fg="#1A2530")
        self.time_label.grid(row=0, column=2, padx=25, pady=0, ipady=3, sticky=tk.E)

        self.update_time()

        # Content Frame (Sidebar + Main Content)
        self.content_frame = tk.Frame(self.main_frame, bg="#E8F0FF")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar (Increased width)
        self.sidebar = tk.Frame(self.content_frame, bg="#2C3E50", width=300)  # Increased width
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)  # Prevent sidebar from shrinking

        self.create_sidebar_buttons()

        # Main Content Area
        self.main_content = tk.Frame(self.content_frame, bg="#E8F0FF")
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Dashboard Frame
        self.dashboard_frame = tk.Frame(self.main_content, bg="#E8F0FF")
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Added padding

        # Tab Frames
        self.transaction_tab = TransactionWindow(self.main_content)
        self.report_tab = ReportWindow(self.main_content)
        self.budget_tab = BudgetWindow(self.main_content)
        self.categories_tab = CategoriesWindow(self.main_content)
        self.goals_tab = GoalsWindow(self.main_content)

        self.transaction_tab.report_window = self.report_tab

        self.show_dashboard()

    def update_time(self):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        formatted_time = now.strftime("%H:%M:%S")
        self.date_label.config(text=formatted_date)
        self.time_label.config(text=formatted_time)
        self.date_label.after(1000, self.update_time)

    def create_sidebar_buttons(self):
        # Add logo or app name at the top of sidebar
        logo_label = tk.Label(
            self.sidebar,
            text="FINNOVA",
            font=("Helvetica Neue", 18, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1",
            pady=20
        )
        logo_label.pack(fill="x")

        # Add separator
        separator = ttk.Separator(self.sidebar, orient="horizontal")
        separator.pack(fill="x", padx=15, pady=5)

        menu_items = [
            ("🏠 Overview", self.show_dashboard),
            ("💰 Transactions", lambda: self.show_tab(self.transaction_tab.frame)),
            ("📊 Reports", lambda: self.show_tab(self.report_tab.frame)),
            ("📅 Budget", lambda: self.show_tab(self.budget_tab.frame)),
            ("📂 Categories", lambda: self.show_tab(self.categories_tab.frame)),
            ("🎯 Goals", lambda: self.show_tab(self.goals_tab.frame)),
        ]

        # Create a frame for buttons
        button_frame = tk.Frame(self.sidebar, bg="#2C3E50")
        button_frame.pack(fill="x", pady=10)

        for text, command in menu_items:
            button = tk.Button(
                button_frame,
                text=text,
                font=("Helvetica Neue", 14, "bold"),  # Made bold
                bg="#34495E",  # Slightly lighter for button
                fg="white",
                bd=0,
                relief="flat",
                activebackground="#1A2939",  # Darker for active state
                activeforeground="#ECF0F1",  # Light color for active text
                command=command,
                pady=14,  # Increased padding
                padx=25,  # Increased padding
                anchor="w",
                cursor="hand2",  # Hand cursor on hover
            )
            button.pack(fill="x", pady=6, padx=15)  # Increased spacing between buttons

        # Add version info at bottom
        version_label = tk.Label(
            self.sidebar,
            text="Version 1.0",
            font=("Helvetica Neue", 10),
            bg="#2C3E50",
            fg="#95A5A6",
            pady=10
        )
        version_label.pack(side="bottom", fill="x")

    def show_tab(self, tab_frame):
        self.dashboard_frame.pack_forget()
        self.transaction_tab.frame.pack_forget()
        self.report_tab.frame.pack_forget()
        self.budget_tab.frame.pack_forget()
        self.categories_tab.frame.pack_forget()
        self.goals_tab.frame.pack_forget()
        tab_frame.pack(fill=tk.BOTH, expand=True)

    def show_dashboard(self):
        # Clear main content area
        for widget in self.main_content.winfo_children():
            widget.pack_forget()

        # Re-add dashboard frame
        self.dashboard_frame = tk.Frame(self.main_content, bg="#E8F0FF")
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Increased padding

        # Create Containers with LabelFrames - custom styling
        recent_transactions_container = tk.Frame(self.dashboard_frame, bg="white", bd=1, relief="solid")
        expense_breakdown_container = tk.Frame(self.dashboard_frame, bg="white", bd=1, relief="solid")
        goal_trackers_container = tk.Frame(self.dashboard_frame, bg="white", bd=1, relief="solid")

        # Add shadow effect and rounded corners through borders
        for container in [recent_transactions_container, expense_breakdown_container, goal_trackers_container]:
            container.configure(highlightbackground="#CCCCCC", highlightthickness=1)

        # Container headers
        recent_header = tk.Label(recent_transactions_container, text="Recent Transactions",
                                font=("Helvetica Neue", 14, "bold"), bg="#3498DB", fg="white",
                                anchor="w", padx=15, pady=8)
        recent_header.pack(fill="x")

        expense_header = tk.Label(expense_breakdown_container, text="Category Breakdown Chart",
                                font=("Helvetica Neue", 14, "bold"), bg="#3498DB", fg="white",
                                anchor="w", padx=15, pady=8)
        expense_header.pack(fill="x")

        goal_header = tk.Label(goal_trackers_container, text="Recent Goal",
                            font=("Helvetica Neue", 14, "bold"), bg="#3498DB", fg="white",
                            anchor="w", padx=15, pady=8)
        goal_header.pack(fill="x")

        # Container content frames
        recent_content = tk.Frame(recent_transactions_container, bg="white", padx=15, pady=15)
        recent_content.pack(fill="both", expand=True)

        expense_content = tk.Frame(expense_breakdown_container, bg="white", padx=15, pady=15)
        expense_content.pack(fill="both", expand=True)

        goal_content = tk.Frame(goal_trackers_container, bg="white", padx=15, pady=15)
        goal_content.pack(fill="both", expand=True)

        # Grid Layout for Containers with more space for charts
        recent_transactions_container.grid(row=0, column=0, rowspan=1, sticky="nsew", padx=10, pady=10)
        expense_breakdown_container.grid(row=0, column=1, rowspan=1, sticky="nsew", padx=10, pady=10)
        goal_trackers_container.grid(row=0, column=2, rowspan=1, sticky="nsew", padx=10, pady=10)

        # Configure row and column weights - middle column gets more weight for the chart
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_columnconfigure(1, weight=2)  # Give chart more space
        self.dashboard_frame.grid_columnconfigure(2, weight=1)
        self.dashboard_frame.grid_rowconfigure(0, weight=1)

        # Assign the containers to the frames
        self.recent_transactions_frame = recent_content
        self.expense_breakdown_frame = expense_content
        self.goal_trackers_frame = goal_content

        # Update Content in the Containers
        self.update_recent_transactions()
        self.update_expense_breakdown()
        self.update_goal_trackers()

    def update_recent_transactions(self):
        for widget in self.recent_transactions_frame.winfo_children():
            widget.destroy()

        # Add a scrollable frame for transactions
        transaction_canvas = tk.Canvas(self.recent_transactions_frame, bg="white", highlightthickness=0)
        transaction_canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.recent_transactions_frame, orient="vertical", command=transaction_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        transaction_canvas.configure(yscrollcommand=scrollbar.set)
        
        transactions_frame = tk.Frame(transaction_canvas, bg="white")
        transaction_canvas.create_window((0, 0), window=transactions_frame, anchor="nw")
        
        def on_frame_configure(event):
            transaction_canvas.configure(scrollregion=transaction_canvas.bbox("all"))
            
        transactions_frame.bind("<Configure>", on_frame_configure)

        transactions = self.report_tab.get_recent_transactions(5)  # Increased number of transactions
        
        if transactions:
            for i, transaction in enumerate(transactions):
                # Create frame for each transaction with alternating background
                bg_color = "#F9F9F9" if i % 2 == 0 else "white"
                transaction_item = tk.Frame(transactions_frame, bg=bg_color, padx=5, pady=8)
                transaction_item.pack(fill="x")
                
                # Date in bold
                date_label = tk.Label(
                    transaction_item,
                    text=transaction['date'],
                    font=("Helvetica Neue", 10, "bold"),
                    bg=bg_color,
                    fg="#2C3E50"
                )
                date_label.pack(side="left", padx=(0, 10))
                
                # Category with custom colors based on type
                category_colors = {
                    "Food": "#27AE60",       # Green
                    "Transport": "#3498DB",  # Blue
                    "Entertainment": "#F39C12"  # Orange
                }
                category_color = category_colors.get(transaction['category'], "#7F8C8D")  # Default gray
                
                category_label = tk.Label(
                    transaction_item,
                    text=transaction['category'],
                    font=("Helvetica Neue", 10),
                    bg=bg_color,
                    fg=category_color
                )
                category_label.pack(side="left", padx=(0, 10))
                
                # Amount right-aligned and bold
                amount_label = tk.Label(
                    transaction_item,
                    text=f"Rs{transaction['amount']}",
                    font=("Helvetica Neue", 10, "bold"),
                    bg=bg_color,
                    fg="#E74C3C" if float(transaction['amount']) > 0 else "#27AE60"  # Red for expenses, green for income
                )
                amount_label.pack(side="right")
        else:
            no_transactions_label = tk.Label(
                transactions_frame, 
                text="No recent transactions.",
                font=("Helvetica Neue", 12),
                bg="white",
                fg="#7F8C8D",
                pady=20
            )
            no_transactions_label.pack(fill="x")

    def update_expense_breakdown(self):
        for widget in self.expense_breakdown_frame.winfo_children():
            widget.destroy()

        categories, expenses = self.report_tab.get_expense_breakdown()
        self.create_expense_chart(categories, expenses)

    def create_expense_chart(self, categories, expenses):
        # Clear previous widgets
        for widget in self.expense_breakdown_frame.winfo_children():
            widget.destroy()
            
        # Check if we have data
        if not expenses or sum(expenses) == 0:
            label = tk.Label(
                self.expense_breakdown_frame, 
                text="No expense data available",
                font=("Helvetica Neue", 14),
                fg="#7F8C8D",
                bg="white"
            )
            label.pack(padx=10, pady=40)
            return
            
        # Custom colors for categories
        colors = ['#3498DB', '#E74C3C', '#27AE60', '#F39C12', '#9B59B6', '#1ABC9C']
        
        # Create the figure with original size
        fig = Figure(figsize=(7, 6), dpi=100)
        ax = fig.add_subplot(111)
            
        # Create the pie chart with improved styling
        wedges, texts, autotexts = ax.pie(
            expenses, 
            labels=None,  # We'll add labels separately
            autopct="%1.1f%%", 
            startangle=90, 
            shadow=True,
            explode=[0.05] * len(categories),  # Slightly explode all pieces
            colors=colors[:len(categories)],
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        # Customize text properties
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_weight('bold')
            autotext.set_color('white')
        
        # Add a title with original styling
        ax.set_title("Expense Breakdown", fontsize=16, pad=20, fontweight='bold')
        
        # Equal aspect ratio ensures the pie chart is circular
        ax.axis("equal")
        
        # Add a legend with adjusted font size and spacing
        ax.legend(
            wedges, 
            categories,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(0.28, -1, 0.4, 1),  # Adjusted bbox_to_anchor
            fontsize=10,  # Slightly increased fontsize
            labelspacing=0.4, 
            borderpad=0.2, 
            handlelength=1,
              # Added ncol for columns
            handletextpad=0.6,  # Increased handletextpad
            columnspacing=1.2  # Increased columnspacing
            )
        
        # Adjust layout
        fig.tight_layout()
        
        # Create canvas with original styling
        canvas = FigureCanvasTkAgg(fig, master=self.expense_breakdown_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_goal_trackers(self):
        for widget in self.goal_trackers_frame.winfo_children():
            widget.destroy()

        goals = get_goals()
        if goals:
            latest_goal = goals[-1]
            self.display_latest_goal(latest_goal)
        else:
            empty_label = tk.Label(
                self.goal_trackers_frame,
                text="No goals set.",
                font=("Helvetica Neue", 14),
                fg="#7F8C8D",
                bg="white",
                pady=30
            )
            empty_label.pack(fill="both", expand=True)

    def display_latest_goal(self, goal):
        # Create container for goal details
        goal_details = tk.Frame(self.goal_trackers_frame, bg="white")
        goal_details.pack(fill="both", expand=True, padx=10, pady=10)  # Add padding to goal_details

        # Goal name with larger font
        name_label = tk.Label(
            goal_details,
            text=goal['name'],
            font=("Helvetica Neue", 16, "bold"),
            bg="white",
            fg="#2C3E50",
            anchor="w"
        )
        name_label.pack(fill="x", pady=(5, 15))

        # Details with icons and better formatting
        details_frame = tk.Frame(goal_details, bg="white")
        details_frame.pack(fill="x", pady=5)

        # Configure grid columns for even distribution
        details_frame.grid_columnconfigure(0, weight=1)
        details_frame.grid_columnconfigure(1, weight=1)

        # Target amount
        target_label = tk.Label(
            details_frame,
            text="Target:",
            font=("Helvetica Neue", 12),
            bg="white",
            fg="#7F8C8D",
            width=10,
            anchor="w"
        )
        target_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)  # Add padx

        target_value = tk.Label(
            details_frame,
            text=f"Rs{goal['target_amount']}",
            font=("Helvetica Neue", 14, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        target_value.grid(row=0, column=1, sticky="w", pady=5, padx=5)  # Add padx

        # Saved amount
        saved_label = tk.Label(
            details_frame,
            text="Saved:",
            font=("Helvetica Neue", 12),
            bg="white",
            fg="#7F8C8D",
            width=10,
            anchor="w"
        )
        saved_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)  # Add padx

        saved_value = tk.Label(
            details_frame,
            text=f"Rs{goal['saved_amount']}",
            font=("Helvetica Neue", 14, "bold"),
            bg="white",
            fg="#27AE60"  # Green for saved amount
        )
        saved_value.grid(row=1, column=1, sticky="w", pady=5, padx=5)  # Add padx

        # Deadline
        deadline_label = tk.Label(
            details_frame,
            text="Deadline:",
            font=("Helvetica Neue", 12),
            bg="white",
            fg="#7F8C8D",
            width=10,
            anchor="w"
        )
        deadline_label.grid(row=2, column=0, sticky="w", pady=5, padx=5)  # Add padx

        deadline_value = tk.Label(
            details_frame,
            text=goal['deadline'],
            font=("Helvetica Neue", 14, "bold"),
            bg="white",
            fg="#E74C3C" if datetime.strptime(goal['deadline'], "%Y-%m-%d").date() < datetime.now().date() else "#2C3E50"
        )
        deadline_value.grid(row=2, column=1, sticky="w", pady=5, padx=5)  # Add padx

        # Progress bar
        progress_frame = tk.Frame(goal_details, bg="white", pady=15)
        progress_frame.pack(fill="x")

        progress_pct = (float(goal['saved_amount']) / float(goal['target_amount'])) * 100

        # Progress bar background
        progress_bg = tk.Canvas(progress_frame, width=200, height=20, bg="#EEEEEE", highlightthickness=0)
        progress_bg.pack(side="left", padx=10)  # Add side and padx

        # Progress bar fill
        progress_fill = progress_bg.create_rectangle(0, 0, progress_pct * 2, 20, fill="#3498DB")

        # Progress text
        progress_text = tk.Label(
            progress_frame,
            text=f"{progress_pct:.1f}% Complete",
            font=("Helvetica Neue", 12, "bold"),
            bg="white",
            fg="#2C3E50"
        )
        progress_text.pack(side="left", padx=10)  # Add side and padx

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()