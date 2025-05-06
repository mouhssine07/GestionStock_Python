import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from styles import SmartStockStyles
from datetime import datetime
import os
import json
from dashboard_view import DashboardView
from products_view import ProductsView
from analytics_view import AnalyticsView
from reports_view import ReportsView
from settings_view import SettingsView

class SmartStock:
    def __init__(self, username="admin"):
        self.username = username
        self.products = []
        self.data_file = "data.json"
        self.current_view = None
        self.nav_frames = {}
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("SmartStock - Dashboard")
        self.root.state('zoomed')  # Start maximized
        self.root.minsize(900, 600)
        self.root.configure(bg=SmartStockStyles.COLORS["bg_light"])
        
        # Configure ttk styles
        self.style = ttk.Style()
        SmartStockStyles.configure_ttk_styles(self.style)
        
        # Load products from JSON
        self.load_from_json()
        
        # Create main UI
        self.create_main_ui()
        
        # Navigate to Dashboard by default
        self.navigate("Dashboard")
    
    def create_main_ui(self):
        """Create the main application UI"""
        self.create_sidebar()
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(side="right", fill="both", expand=True)
    
    def create_sidebar(self):
        """Create the application sidebar"""
        sidebar_width = 240
        
        sidebar = tk.Frame(
            self.root, 
            bg=SmartStockStyles.COLORS["primary_dark"],
            width=sidebar_width
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        logo_frame = tk.Frame(sidebar, bg=SmartStockStyles.COLORS["primary_dark"])
        logo_frame.pack(fill="x", pady=(30, 40))
        
        logo_text = tk.Label(
            logo_frame,
            text="📊",
            font=("Segoe UI", 28),
            bg=SmartStockStyles.COLORS["primary_dark"],
            fg="white"
        )
        logo_text.pack(side="left", padx=(25, 10))
        
        app_name = tk.Label(
            logo_frame,
            text="SmartStock",
            font=("Segoe UI", 18, "bold"),
            bg=SmartStockStyles.COLORS["primary_dark"],
            fg="white"
        )
        app_name.pack(side="left")
        
        nav_items = [
            {"text": "Dashboard", "icon": "🏠", "active": True},
            {"text": "Products", "icon": "📦"},
            {"text": "Invoices", "icon": "📄"},
            {"text": "Analytics", "icon": "📈"},
            {"text": "Reports", "icon": "📊"},
            {"text": "Settings", "icon": "⚙️"}
        ]
        
        for item in nav_items:
            bg_color = SmartStockStyles.COLORS["primary"] if item.get("active") else SmartStockStyles.COLORS["primary_dark"]
            nav_frame = tk.Frame(sidebar, bg=bg_color)
            nav_frame.pack(fill="x", pady=2)
            self.nav_frames[item["text"]] = nav_frame
            
            if item.get("active"):
                indicator = tk.Frame(nav_frame, bg=SmartStockStyles.COLORS["secondary"], width=4, height=40)
                indicator.pack(side="left", fill="y")
            
            icon_label = tk.Label(
                nav_frame,
                text=item["icon"],
                font=("Segoe UI", 16),
                bg=bg_color,
                fg="white",
                padx=20 if not item.get("active") else 16,
                pady=10
            )
            icon_label.pack(side="left")
            
            text_label = tk.Label(
                nav_frame,
                text=item["text"],
                font=("Segoe UI", 12),
                bg=bg_color,
                fg="white",
                pady=10
            )
            text_label.pack(side="left")
            
            for widget in [nav_frame, icon_label, text_label]:
                widget.bind("<Button-1>", lambda e, text=item["text"]: self.navigate(text))
                widget.bind("<Enter>", lambda e, frame=nav_frame: self.on_hover_nav(frame, True))
                widget.bind("<Leave>", lambda e, frame=nav_frame, active=item.get("active", False): 
                           self.on_hover_nav(frame, False, active))
        
        profile_frame = tk.Frame(
            sidebar, 
            bg=SmartStockStyles.COLORS["primary"],
            padx=20,
            pady=15
        )
        profile_frame.pack(side="bottom", fill="x")
        
        user_icon = tk.Label(
            profile_frame,
            text="👤",
            font=("Segoe UI", 16),
            bg=SmartStockStyles.COLORS["primary"],
            fg="white"
        )
        user_icon.pack(side="left")
        
        user_name = tk.Label(
            profile_frame,
            text=self.username,
            font=("Segoe UI", 12),
            bg=SmartStockStyles.COLORS["primary"],
            fg="white"
        )
        user_name.pack(side="left", padx=10)
        
        logout_btn = tk.Button(
            profile_frame,
            text="🚪",
            font=("Segoe UI", 14),
            bg=SmartStockStyles.COLORS["primary"],
            fg="white",
            bd=0,
            cursor="hand2",
            activebackground=SmartStockStyles.COLORS["primary_dark"],
            activeforeground="white",
            command=self.logout
        )
        logout_btn.pack(side="right")
    
    def navigate(self, section):
        """Handle navigation between sections"""
        # Update active state in sidebar
        for text, frame in self.nav_frames.items():
            is_active = (text == section)
            frame.config(bg=SmartStockStyles.COLORS["primary"] if is_active else SmartStockStyles.COLORS["primary_dark"])
            # Update indicator
            for child in frame.winfo_children():
                if isinstance(child, tk.Frame):  # Indicator frame
                    child.destroy()
            if is_active:
                indicator = tk.Frame(frame, bg=SmartStockStyles.COLORS["secondary"], width=4, height=40)
                indicator.pack(side="left", fill="y")
            # Update icon padding
            for child in frame.winfo_children():
                if isinstance(child, tk.Label) and child.cget("text") == self.get_icon(text):
                    child.config(padx=16 if is_active else 20)
        
        # Clear current view
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Load new view
        if section == "Dashboard":
            self.current_view = DashboardView(self.main_frame, self.products)
        elif section == "Products":
            self.current_view = ProductsView(self.main_frame, self.products, self.save_to_json, self.show_message)
        elif section == "Invoices":
            from invoices import InvoicesView
            self.current_view = InvoicesView(self.main_frame, self.products, self.save_to_json, self.show_message)
        elif section == "Analytics":
            self.current_view = AnalyticsView(self.main_frame, self.products)
        elif section == "Reports":
            self.current_view = ReportsView(self.main_frame, self.products, self.username)
        elif section == "Settings":
            self.current_view = SettingsView(self.main_frame, self.set_username, self.set_data_file)
        
        self.show_message(f"Navigated to {section} section", "info")
    
    def on_hover_nav(self, frame, is_hover, is_active=False):
        """Handle hover effect for navigation items"""
        if is_hover:
            frame.config(bg=SmartStockStyles.COLORS["primary"])
        else:
            frame.config(bg=SmartStockStyles.COLORS["primary"] if is_active else SmartStockStyles.COLORS["primary_dark"])
    
    def get_icon(self, section):
        """Get icon for a navigation section"""
        icons = {
            "Dashboard": "🏠",
            "Products": "📦",
            "Analytics": "📈",
            "Reports": "📄",
            "Settings": "⚙️"
        }
        return icons.get(section, "")
    
    def set_username(self, new_username):
        """Update username"""
        self.username = new_username
        self.show_message(f"Username updated to {new_username}", "success")
        # Update sidebar username
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_y() > 500:  # Profile frame at bottom
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label) and label.cget("text") == self.username:
                                label.config(text=new_username)
                                break
    
    def set_data_file(self, new_data_file):
        """Update data file path and reload products"""
        self.data_file = new_data_file
        self.load_from_json()
        self.show_message(f"Data file updated to {new_data_file}", "success")
    
    def save_to_json(self):
        """Save products to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.products, f, indent=4)
        except Exception as e:
            self.show_message(f"Error saving to JSON: {str(e)}", "error")
    
    def load_from_json(self):
        """Load products from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.products = json.load(f)
                if self.current_view:
                    self.current_view.update_products(self.products)
        except Exception as e:
            self.show_message(f"Error loading from JSON: {str(e)}", "error")
    
    def logout(self):
        """Handle logout and return to login screen"""
        self.save_to_json()
        self.root.destroy()
        from smartstock_login import SmartStockLogin
        login_app = SmartStockLogin()
        login_app.run()
    
    def show_message(self, message, message_type="info"):
        """Show a status message to the user"""
        colors = {
            "success": SmartStockStyles.COLORS["success"],
            "error": SmartStockStyles.COLORS["error"],
            "warning": SmartStockStyles.COLORS["warning"],
            "info": SmartStockStyles.COLORS["primary"]
        }
        bg_color = colors.get(message_type, SmartStockStyles.COLORS["primary"])
        
        msg_frame = tk.Frame(
            self.root,
            bg=bg_color,
            padx=20,
            pady=10
        )
        msg_frame.place(relx=1, rely=0.05, anchor="ne", relwidth=0.3)
        
        msg_label = tk.Label(
            msg_frame,
            text=message,
            bg=bg_color,
            fg="white",
            font=SmartStockStyles.FONTS["body"],
            wraplength=250,
            justify="left"
        )
        msg_label.pack(fill="both")
        
        self.root.after(3000, msg_frame.destroy)
    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def run(self):
        """Run the main application"""
        self.root.mainloop()