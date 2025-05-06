import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from styles import SmartStockStyles
import os

class AnalyticsView:
    def __init__(self, parent, products):
        self.parent = parent
        self.products = products
        self.create_analytics_ui()
    
    def create_analytics_ui(self):
        """Create the analytics UI"""
        header_frame = ttk.Frame(self.parent, style="Main.TFrame")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Analytics",
            style="Title.TLabel"
        )
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Visualize your inventory data",
            font=("Segoe UI", 12),
            background=SmartStockStyles.COLORS["bg_light"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        subtitle_label.pack(side="left", padx=(10, 0), pady=5)
        
        content_frame = ttk.Frame(self.parent, style="Main.TFrame")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        if not self.products:
            no_data_label = ttk.Label(
                content_frame,
                text="No products to analyze. Add products in the Products section.",
                font=SmartStockStyles.FONTS["body"],
                background=SmartStockStyles.COLORS["bg_light"],
                foreground=SmartStockStyles.COLORS["text_muted"]
            )
            no_data_label.pack(pady=20)
            return
        
        # Charts
        charts_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=20)
        charts_frame.pack(fill="both", expand=True)
        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)
        
        # Quantity Distribution
        self.create_quantity_chart()
        quantity_img = tk.PhotoImage(file="quantity_chart.png")
        quantity_label = ttk.Label(
            charts_frame,
            image=quantity_img,
            background=SmartStockStyles.COLORS["bg_card"]
        )
        quantity_label.image = quantity_img  # Keep reference
        quantity_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Price Distribution
        self.create_price_chart()
        price_img = tk.PhotoImage(file="price_chart.png")
        price_label = ttk.Label(
            charts_frame,
            image=price_img,
            background=SmartStockStyles.COLORS["bg_card"]
        )
        price_label.image = price_img  # Keep reference
        price_label.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    
    def create_quantity_chart(self):
        """Create a bar chart for product quantities"""
        names = [p["name"] for p in self.products]
        quantities = [p["quantity"] for p in self.products]
        
        plt.figure(figsize=(6, 4))
        plt.bar(names, quantities, color=SmartStockStyles.COLORS["primary"])
        plt.title("Product Quantities")
        plt.xlabel("Product")
        plt.ylabel("Quantity")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("quantity_chart.png")
        plt.close()
    
    def create_price_chart(self):
        """Create a histogram for product prices"""
        prices = [p["price"] for p in self.products]
        
        plt.figure(figsize=(6, 4))
        plt.hist(prices, bins=10, color=SmartStockStyles.COLORS["secondary"], edgecolor="black")
        plt.title("Price Distribution")
        plt.xlabel("Price ($)")
        plt.ylabel("Number of Products")
        plt.tight_layout()
        plt.savefig("price_chart.png")
        plt.close()
    
    def update_products(self, products):
        """Update products and refresh charts"""
        self.products = products
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.create_analytics_ui()