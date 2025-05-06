import tkinter as tk
from tkinter import ttk, filedialog
from styles import SmartStockStyles

class SettingsView:
    def __init__(self, parent, set_username_callback, set_data_file_callback):
        self.parent = parent
        self.set_username = set_username_callback
        self.set_data_file = set_data_file_callback
        self.create_settings_ui()
    
    def create_settings_ui(self):
        """Create the settings UI"""
        header_frame = ttk.Frame(self.parent, style="Main.TFrame")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Settings",
            style="Title.TLabel"
        )
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Configure application preferences",
            font=("Segoe UI", 12),
            background=SmartStockStyles.COLORS["bg_light"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        subtitle_label.pack(side="left", padx=(10, 0), pady=5)
        
        content_frame = ttk.Frame(self.parent, style="Main.TFrame")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        settings_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=20)
        settings_frame.pack(fill="x")
        
        # Username
        ttk.Label(
            settings_frame,
            text="Username",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(settings_frame)
        SmartStockStyles.apply_entry_style(self.username_entry)
        self.username_entry.pack(fill="x", pady=(0, 15))
        
        # Data File
        ttk.Label(
            settings_frame,
            text="Data File Path",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        ).pack(anchor="w", pady=(0, 5))
        
        data_frame = ttk.Frame(settings_frame, style="Card.TFrame")
        data_frame.pack(fill="x", pady=(0, 15))
        
        self.data_file_var = tk.StringVar()
        data_entry = tk.Entry(
            data_frame,
            textvariable=self.data_file_var,
            state="readonly"
        )
        SmartStockStyles.apply_entry_style(data_entry)
        data_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_button = tk.Button(
            data_frame,
            text="Browse",
            command=self.browse_data_file
        )
        SmartStockStyles.apply_button_style(browse_button, "primary")
        browse_button.pack(side="right")
        
        # Theme
        ttk.Label(
            settings_frame,
            text="Theme",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.theme_var = tk.StringVar(value="Light")
        theme_menu = ttk.Combobox(
            settings_frame,
            textvariable=self.theme_var,
            values=["Light", "Dark"],
            state="readonly"
        )
        theme_menu.pack(fill="x", pady=(0, 15))
        
        # Save Button
        save_button = tk.Button(
            settings_frame,
            text="Save Settings",
            command=self.save_settings
        )
        SmartStockStyles.apply_button_style(save_button, "primary")
        save_button.pack(fill="x", pady=10, ipady=8)
    
    def browse_data_file(self):
        """Browse for a JSON data file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Select Data File",
            initialfile="data.json"
        )
        if file_path:
            self.data_file_var.set(file_path)
    
    def save_settings(self):
        """Save the settings"""
        username = self.username_entry.get().strip()
        data_file = self.data_file_var.get().strip()
        theme = self.theme_var.get()
        
        if username:
            self.set_username(username)
        
        if data_file:
            self.set_data_file(data_file)
        
        # Theme is a placeholder for future implementation
        if theme == "Dark":
            ttk.Label(self.parent, text="Dark theme not yet implemented", style="Warning.TLabel").pack()
    
    def update_products(self, products):
        """Update products (no action needed in settings)"""
        pass