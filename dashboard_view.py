import tkinter as tk
from tkinter import ttk
from styles import SmartStockStyles

class DashboardView:
    def __init__(self, parent, products):
        self.parent = parent
        self.products = products
        self.create_dashboard()
    
    def create_dashboard(self):
        """Create the dashboard UI"""
        header_frame = ttk.Frame(self.parent, style="Main.TFrame")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Dashboard",
            style="Title.TLabel"
        )
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Overview of your inventory",
            font=("Segoe UI", 12),
            background=SmartStockStyles.COLORS["bg_light"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        subtitle_label.pack(side="left", padx=(10, 0), pady=5)
        
        content_frame = ttk.Frame(self.parent, style="Main.TFrame")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Metrics cards
        metrics_frame = ttk.Frame(content_frame, style="Card.TFrame")
        metrics_frame.pack(fill="x", pady=(0, 20))
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.columnconfigure(1, weight=1)
        metrics_frame.columnconfigure(2, weight=1)
        
        # Total Products
        total_products = len(self.products)
        total_card = ttk.Frame(metrics_frame, style="Card.TFrame", padding=20)
        total_card.grid(row=0, column=0, padx=5, sticky="ew")
        total_label = ttk.Label(
            total_card,
            text="Total Products",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        total_label.pack()
        total_value = ttk.Label(
            total_card,
            text=str(total_products),
            font=SmartStockStyles.FONTS["header"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["primary"]
        )
        total_value.pack(pady=5)
        
        # Total Inventory Value
        total_value = sum(p["quantity"] * p["price"] for p in self.products)
        value_card = ttk.Frame(metrics_frame, style="Card.TFrame", padding=20)
        value_card.grid(row=0, column=1, padx=5, sticky="ew")
        value_label = ttk.Label(
            value_card,
            text="Inventory Value",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        value_label.pack()
        value_value = ttk.Label(
            value_card,
            text=f"${total_value:.2f}",
            font=SmartStockStyles.FONTS["header"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["primary"]
        )
        value_value.pack(pady=5)
        
        # Low Stock Items
        low_stock = len([p for p in self.products if p["quantity"] < 5])
        low_card = ttk.Frame(metrics_frame, style="Card.TFrame", padding=20)
        low_card.grid(row=0, column=2, padx=5, sticky="ew")
        low_label = ttk.Label(
            low_card,
            text="Low Stock Items",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        low_label.pack()
        low_value = ttk.Label(
            low_card,
            text=str(low_stock),
            font=SmartStockStyles.FONTS["header"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["error"]
        )
        low_value.pack(pady=5)
        
        # Recent Activity
        activity_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=20)
        activity_frame.pack(fill="both", expand=True)
        activity_label = ttk.Label(
            activity_frame,
            text="Recent Activity",
            style="Subtitle.TLabel"
        )
        activity_label.pack(anchor="w")
        
        activity_text = tk.Text(
            activity_frame,
            wrap="word",
            height=10,
            font=SmartStockStyles.FONTS["body"],
            bg=SmartStockStyles.COLORS["bg_card"],
            fg=SmartStockStyles.COLORS["text_dark"],
            relief="flat",
            padx=5,
            pady=5
        )
        activity_text.pack(fill="both", expand=True, pady=10)
        activity_text.insert("1.0", "No recent activity recorded.\nAdd products to see updates here.")
        activity_text.config(state="disabled")
    
    def update_products(self, products):
        """Update products and refresh metrics"""
        self.products = products
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.create_dashboard()