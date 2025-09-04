import tkinter as tk
from tkinter import ttk, messagebox
from database.core import load_data, save_data
from datetime import datetime

def add_goal(name, target_amount, deadline):
    """
    Add a new goal to the database.
    """
    data = load_data()
    goal = {
        "name": name,
        "target_amount": target_amount,
        "deadline": deadline,
        "saved_amount": 0
    }
    data["goals"].append(goal)
    save_data(data)  # Ensure data is saved
    return goal

def update_goal_savings(goal_name, amount):
    """
    Update the saved amount for a specific goal.
    """
    data = load_data()
    for goal in data["goals"]:
        if goal["name"] == goal_name:
            goal["saved_amount"] += amount
            save_data(data)  # Ensure data is saved
            break

def get_goals():
    """
    Retrieve all goals from the database.
    """
    return load_data().get("goals", [])

def calculate_goal_progress(goal):
    """
    Calculate progress, time remaining, and required monthly savings for a goal.
    """
    target_amount = goal["target_amount"]
    saved_amount = goal["saved_amount"]
    deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d").date()
    today = datetime.now().date()

    # Calculate progress
    progress = (saved_amount / target_amount) * 100 if target_amount > 0 else 0

    # Calculate time remaining
    days_remaining = (deadline - today).days
    months_remaining = max(days_remaining / 30, 0.1)  # Avoid division by zero

    # Calculate required monthly savings
    remaining_amount = target_amount - saved_amount
    required_monthly_savings = remaining_amount / months_remaining if months_remaining > 0 else 0

    return {
        "progress": progress,
        "days_remaining": days_remaining,
        "required_monthly_savings": required_monthly_savings
    }

class ScrollableFrame(ttk.Frame):
    """A scrollable frame widget"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas object and a vertical scrollbar for scrolling
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Add mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Create a window inside the canvas with the scrollable frame
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure the canvas to resize with the window
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Pack the scrollbar and canvas
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

    def _on_canvas_resize(self, event):
        # Update the width of the canvas window when canvas size changes
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def clear(self):
        """Clear all widgets in the scrollable frame"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

class GoalsWindow:
    def __init__(self, notebook):
        """
        Initialize the Goals tab.
        """
        # Create a frame for the Goals tab
        self.frame = ttk.Frame(notebook)
        self.data = load_data()

        # Debug: Print to verify GoalsWindow is initialized
        print("GoalsWindow initialized")

        # Create a form to add new goals
        self.create_goal_form()
        
        # Create a scrollable container for goals
        self.goals_frame = ttk.LabelFrame(self.frame, text="Your Goals")
        self.goals_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.scrollable = ScrollableFrame(self.goals_frame)
        self.scrollable.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.goals_container = self.scrollable.scrollable_frame

        # Display existing goals
        self.display_goals()

    def create_goal_form(self):
        """
        Create a form to add new goals.
        """
        self.form_frame = ttk.LabelFrame(self.frame, text="Set a New Goal", name="set_goal_form")
        self.form_frame.pack(fill='x', padx=10, pady=10)

        form_content = ttk.Frame(self.form_frame)
        form_content.pack(fill='x', padx=10, pady=10)

        # Create a better layout with proper spacing
        # Goal Name
        ttk.Label(form_content, text="Goal Name:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.goal_name_entry = ttk.Entry(form_content, width=30)
        self.goal_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Target Amount
        ttk.Label(form_content, text="Target Amount:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.target_amount_entry = ttk.Entry(form_content, width=15)
        self.target_amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Deadline
        ttk.Label(form_content, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.deadline_entry = ttk.Entry(form_content, width=15)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Save Goal Button
        ttk.Button(form_content, text="Save Goal", command=self.save_goal).grid(row=3, column=1, padx=10, pady=10, sticky='e')
        
        # Make first column expandable
        form_content.columnconfigure(1, weight=1)

    def save_goal(self):
        """
        Save a new goal to the database and add it to the display.
        """
        try:
            name = self.goal_name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Goal name cannot be empty!")
                return
                
            target_amount_str = self.target_amount_entry.get().strip()
            if not target_amount_str:
                messagebox.showerror("Error", "Target amount cannot be empty!")
                return
                
            target_amount = float(target_amount_str)
            
            deadline = self.deadline_entry.get().strip()
            if not deadline:
                messagebox.showerror("Error", "Deadline cannot be empty!")
                return
                
            # Validate deadline format
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return

            # Add goal to database and get the new goal
            new_goal = add_goal(name, target_amount, deadline)
            
            # Refresh the display to include the new goal
            self.display_goals()
            
            messagebox.showinfo("Success", "Goal added successfully!")

            # Clear form fields
            self.goal_name_entry.delete(0, tk.END)
            self.target_amount_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_goals(self):
        """
        Display existing goals in containers with progress bars and required monthly savings.
        """
        # Clear existing widgets in the goals container
        self.scrollable.clear()
        
        goals = get_goals()
        
        if not goals:
            ttk.Label(self.goals_container, text="No goals found. Create your first goal above!").pack(pady=20)
            return

        # Sort goals by deadline (chronologically)
        goals.sort(key=lambda x: datetime.strptime(x["deadline"], "%Y-%m-%d"))

        # Display each goal in a container
        for goal in goals:
            self.add_goal_to_display(goal)

    def add_goal_to_display(self, goal):
        """
        Add a single goal to the display.
        """
        # Determine goal status based on days remaining
        deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d").date()
        today = datetime.now().date()
        days_remaining = (deadline - today).days
        
        # Style settings based on status
        if days_remaining < 0:
            bg_color = "#ffcccc"  # Light red for overdue
            status_text = "OVERDUE"
        elif days_remaining < 7:
            bg_color = "#ffffcc"  # Light yellow for urgent
            status_text = f"URGENT: {days_remaining} days left"
        else:
            bg_color = "#f0f0f0"  # Light gray for normal
            status_text = f"{days_remaining} days left"
        
        # Create a frame with custom styling
        goal_frame = ttk.Frame(self.goals_container)
        goal_frame.pack(fill='x', padx=5, pady=5)
        
        # Apply background color using a label underneath
        bg_label = tk.Label(goal_frame, bg=bg_color)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Content frame on top of the background
        content = ttk.Frame(goal_frame)
        content.pack(fill='x', padx=5, pady=5)
        
        # Left side: goal details
        details_frame = ttk.Frame(content)
        details_frame.pack(side='left', fill='both', expand=True)
        
        # Goal title with larger font
        title_label = ttk.Label(details_frame, text=goal["name"], font=('TkDefaultFont', 11, 'bold'))
        title_label.grid(row=0, column=0, sticky='w', columnspan=2)
        
        # Goal details in two columns
        ttk.Label(details_frame, text=f"Target: Rs{goal['target_amount']:.2f}").grid(row=1, column=0, sticky='w', padx=(0, 10))
        ttk.Label(details_frame, text=f"Saved: Rs{goal['saved_amount']:.2f}").grid(row=1, column=1, sticky='w')
        ttk.Label(details_frame, text=f"Deadline: {goal['deadline']}").grid(row=2, column=0, sticky='w')
        ttk.Label(details_frame, text=status_text).grid(row=2, column=1, sticky='w')

        # Right side: progress and buttons
        progress_frame = ttk.Frame(content)
        progress_frame.pack(side='right', padx=10)
        
        # Calculate progress
        progress = calculate_goal_progress(goal)
        
        # Progress percentage
        progress_text = f"{progress['progress']:.1f}%"
        ttk.Label(progress_frame, text=progress_text).pack(anchor='e')
        
        # Progress Bar
        progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=150, mode='determinate')
        progress_bar['value'] = min(progress["progress"], 100)  # Cap at 100%
        progress_bar.pack(pady=5)
        
        # Required monthly savings
        monthly_text = f"Monthly needed: Rs{progress['required_monthly_savings']:.2f}"
        ttk.Label(progress_frame, text=monthly_text).pack(anchor='e')
        
        # Action buttons
        buttons_frame = ttk.Frame(progress_frame)
        buttons_frame.pack(pady=5)
        
        edit_button = ttk.Button(buttons_frame, text="Update Savings", 
                                command=lambda name=goal["name"]: self.update_savings(name))
        edit_button.pack(side='left', padx=2)
        
        # Add a separator after each goal
        separator = ttk.Separator(self.goals_container, orient='horizontal')
        separator.pack(fill='x', padx=5, pady=5)

    def update_savings(self, goal_name):
        """
        Open a dialog to update the saved amount for a goal.
        """
        # Create a top-level window
        update_window = tk.Toplevel()
        update_window.title(f"Update Savings for {goal_name}")
        update_window.geometry("300x150")
        update_window.resizable(False, False)
        
        # Center the window
        update_window.update_idletasks()
        width = update_window.winfo_width()
        height = update_window.winfo_height()
        x = (update_window.winfo_screenwidth() // 2) - (width // 2)
        y = (update_window.winfo_screenheight() // 2) - (height // 2)
        update_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Add widgets
        ttk.Label(update_window, text=f"Add savings for: {goal_name}").pack(pady=10)
        
        # Entry for amount
        amount_frame = ttk.Frame(update_window)
        amount_frame.pack(pady=5)
        
        ttk.Label(amount_frame, text="Amount: Rs").pack(side="left")
        amount_entry = ttk.Entry(amount_frame, width=15)
        amount_entry.pack(side="left")
        amount_entry.focus_set()
        
        # Buttons
        button_frame = ttk.Frame(update_window)
        button_frame.pack(pady=10)
        
        def save_update():
            try:
                amount = float(amount_entry.get())
                update_goal_savings(goal_name, amount)
                update_window.destroy()
                # Refresh display
                self.display_goals()
                messagebox.showinfo("Success", f"Added Rs{amount:.2f} to {goal_name}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        ttk.Button(button_frame, text="Save", command=save_update).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=update_window.destroy).pack(side="left", padx=5)