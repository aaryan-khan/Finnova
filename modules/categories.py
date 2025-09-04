import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.core import load_data, save_data

class CategoriesWindow:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        self.data = load_data()
        
        # Define color mapping with friendly names and hexcodes
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

        # Title with matching style
        title_frame = ttk.Frame(self.frame, style='Header.TFrame')
        title_frame.pack(fill=tk.X)
        ttk.Label(title_frame, text="Categories", font=("Arial", 16, "bold"), 
                  foreground="white", background="#1e2a3a").pack(pady=10, padx=15, anchor=tk.W)

        # Main Containers with matching style
        main_container = ttk.Frame(self.frame, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Category List Container (Left Side) - styled as panel
        list_container = ttk.Frame(main_container, style='Panel.TFrame')
        list_container.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(list_container, style='PanelHeader.TFrame')
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Expense Categories", style='PanelHeader.TLabel').pack(pady=8, padx=10, anchor=tk.W)

        content_frame = ttk.Frame(list_container, style='PanelContent.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for Scrollbar
        self.canvas = tk.Canvas(content_frame, background="#f0f2f5", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.category_container = ttk.Frame(self.canvas, style='PanelContent.TFrame')
        self.canvas.create_window((0, 0), window=self.category_container, anchor=tk.NW, width=self.canvas.winfo_width())
        
        self.update_category_list()

        # Add New Category Container (Right Side) - styled as panel
        add_container = ttk.Frame(main_container, style='Panel.TFrame')
        add_container.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(add_container, style='PanelHeader.TFrame')
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Add New Category", style='PanelHeader.TLabel').pack(pady=8, padx=10, anchor=tk.W)

        content_frame = ttk.Frame(add_container, style='PanelContent.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(content_frame, text="Category Name", style='Label.TLabel').pack(pady=(10, 2), anchor=tk.W)
        self.category_entry = ttk.Entry(content_frame, style='Entry.TEntry')
        self.category_entry.pack(fill=tk.X, pady=3)

        ttk.Label(content_frame, text="Icon (Emoji/Category)", style='Label.TLabel').pack(pady=(10, 2), anchor=tk.W)
        self.icon_combobox = ttk.Combobox(content_frame, values=["🏠 Home", "🍔 Food", "🚗 Transport", "🧾 Bills", 
                                                               "🛍️ Shopping", "🎮 Entertainment", "📚 Study", 
                                                               "🏖️ Leisure", "😃 Other"])
        self.icon_combobox.pack(fill=tk.X, pady=3)
        self.icon_combobox.current(8)  # Default to "Other"

        ttk.Label(content_frame, text="Color", style='Label.TLabel').pack(pady=(10, 2), anchor=tk.W)
        
        # Create a frame to hold color swatches and the combobox
        color_frame = ttk.Frame(content_frame)
        color_frame.pack(fill=tk.X, pady=3)
        
        # Create the combobox with just color names
        self.color_combobox = ttk.Combobox(color_frame, values=list(self.color_mapping.keys()))
        self.color_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.color_combobox.current(0)  # Default to Blue
        
        # Create color preview
        self.color_preview = tk.Frame(color_frame, width=25, height=25, background=self.color_mapping["Blue"])
        self.color_preview.pack(side=tk.RIGHT, padx=5)
        
        # Bind the combobox selection to update the color preview
        self.color_combobox.bind('<<ComboboxSelected>>', self.update_color_preview)

        # Add Category button with blue style to match dashboard
        ttk.Button(content_frame, text="+ Add Category", command=self.add_category, 
                   style='Blue.TButton').pack(pady=15, fill=tk.X)

    def update_color_preview(self, event=None):
        selected_color = self.color_combobox.get()
        if selected_color in self.color_mapping:
            self.color_preview.configure(background=self.color_mapping[selected_color])

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
        
        # Form elements
        style.configure('Label.TLabel', font=('Arial', 10), background='white')
        style.configure('Entry.TEntry', font=('Arial', 10))
        
        # Button styles
        style.configure('Blue.TButton', font=('Arial', 10, 'bold'))
        style.map('Blue.TButton',
                  background=[('!active', '#4899d4'), ('active', '#3a87c4'), ('pressed', '#2d6da3')],
                  foreground=[('!active', 'white'), ('active', 'white'), ('pressed', 'white')])
        
        style.configure('Small.TButton', font=('Arial', 9))
        style.configure('SmallDanger.TButton', font=('Arial', 9))
        style.map('SmallDanger.TButton',
                  background=[('!active', '#e74c3c'), ('active', '#c0392b')],
                  foreground=[('!active', 'white'), ('active', 'white')])

    def update_category_list(self):
        # Clear existing category containers
        for widget in self.category_container.winfo_children():
            widget.destroy()

        # Use the categories from the data
        for i, category in enumerate(self.data["categories"]):
            # In a real app, color and icon would be stored with the category
            # For demonstration, we'll cycle through colors
            color_name = list(self.color_mapping.keys())[i % len(self.color_mapping)]
            color_hex = self.color_mapping[color_name]
            
            # Create category item frame
            category_frame = ttk.Frame(self.category_container)
            category_frame.pack(fill=tk.X, pady=2, padx=5)
            
            # Color indicator
            color_indicator = tk.Frame(category_frame, width=10, background=color_hex)
            color_indicator.pack(side=tk.LEFT, fill=tk.Y)
            
            # Get icon (in a real app, these would be stored with the category)
            icon = "🔹"  # Default icon
            
            # Content frame for the category item
            content_frame = ttk.Frame(category_frame, style='CategoryItem.TFrame')
            content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Display category with icon and color name
            ttk.Label(content_frame, text=f"{icon} {category}", 
                     font=("Arial", 11)).pack(side=tk.LEFT, padx=10, pady=8)
            
            ttk.Label(content_frame, text=f"({color_name})", 
                     font=("Arial", 9), foreground="gray").pack(side=tk.LEFT, pady=8)

            # Action buttons
            button_frame = ttk.Frame(content_frame)
            button_frame.pack(side=tk.RIGHT, padx=5)
            
            edit_button = ttk.Button(button_frame, text="Edit", 
                                    command=lambda cat=category: self.edit_category(cat), 
                                    style='Small.TButton', width=5)
            edit_button.pack(side=tk.LEFT, padx=2)

            delete_button = ttk.Button(button_frame, text="Delete", 
                                      command=lambda cat=category: self.delete_category(cat), 
                                      style='SmallDanger.TButton', width=6)
            delete_button.pack(side=tk.LEFT, padx=2)

        # Update scroll region
        self.category_container.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Make sure the canvas width adjusts to its container
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(
            self.canvas.find_withtag('all')[0] if self.canvas.find_withtag('all') else 0, 
            width=e.width))

    def add_category(self):
        category = self.category_entry.get()
        if not category:
            messagebox.showerror("Error", "Category name cannot be empty.")
            return
            
        if category in self.data["categories"]:
            messagebox.showerror("Error", "Category already exists.")
            return
            
        # In a real app, you would save the icon and color selection too
        icon = self.icon_combobox.get().split(" ")[0]
        color = self.color_combobox.get()
        
        # For demonstration, we'll just print what would be saved
        print(f"Adding category: {category} with icon {icon} and color {color}")
            
        self.data["categories"].append(category)
        save_data(self.data)
        self.update_category_list()
        messagebox.showinfo("Success", "Category added successfully!")
        self.category_entry.delete(0, tk.END)

    def edit_category(self, category_to_edit):
        # In a real app, this would open a dialog to edit name, icon, and color
        new_category = simpledialog.askstring("Edit Category", "Enter new category name:", 
                                             initialvalue=category_to_edit)
        if new_category and new_category != category_to_edit and new_category not in self.data["categories"]:
            index = self.data["categories"].index(category_to_edit)
            self.data["categories"][index] = new_category
            save_data(self.data)
            self.update_category_list()
        elif new_category == category_to_edit:
            pass  # No change needed
        else:
            messagebox.showerror("Error", "Category already exists or is empty.")

    def delete_category(self, category_to_delete):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the category '{category_to_delete}'?"):
            self.data["categories"].remove(category_to_delete)
            save_data(self.data)
            self.update_category_list()