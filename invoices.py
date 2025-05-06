import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from styles import SmartStockStyles
from datetime import datetime, timedelta
import json
import os
from fpdf import FPDF

class InvoicesView:
    def __init__(self, parent, products, save_to_json_callback, show_message_callback):
        self.parent = parent
        self.products = products
        self.save_to_json = save_to_json_callback
        self.show_message = show_message_callback
        self.invoices = self.load_invoices()
        self.selected_products = []  # Track products added to invoice
        self.create_invoices_ui()
    
    def load_invoices(self):
        """Load invoices from JSON file"""
        try:
            if os.path.exists("invoices.json"):
                with open("invoices.json", "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.show_message(f"Error loading invoices: {str(e)}", "error")
            return []
    
    def save_invoices(self):
        """Save invoices to JSON file"""
        try:
            with open("invoices.json", "w") as f:
                json.dump(self.invoices, f, indent=4)
        except Exception as e:
            self.show_message(f"Error saving invoices: {str(e)}", "error")
    
    def create_invoices_ui(self):
        """Create the invoices UI"""
        self.create_header()
        
        content_container = ttk.Frame(self.parent, style="Main.TFrame")
        content_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Create left panel for invoice list
        list_frame = ttk.Frame(content_container, style="Main.TFrame")
        list_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.create_invoice_list(list_frame)
        
        # Create right panel for invoice details/form
        details_frame = ttk.Frame(content_container, style="Main.TFrame")
        details_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        self.create_invoice_form(details_frame)
    
    def create_header(self):
        """Create the header section"""
        header_frame = ttk.Frame(self.parent, style="Main.TFrame")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Invoice Manager",
            style="Title.TLabel"
        )
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Create and manage client invoices",
            font=("Segoe UI", 12),
            background=SmartStockStyles.COLORS["bg_light"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        subtitle_label.pack(side="left", padx=(10, 0), pady=5)
        
        date_label = ttk.Label(
            header_frame,
            text=datetime.now().strftime("%B %d, %Y"),
            font=("Segoe UI", 12),
            background=SmartStockStyles.COLORS["bg_light"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        date_label.pack(side="right", pady=5)
    
    def create_invoice_list(self, parent):
        """Create the invoice list section"""
        header_frame = ttk.Frame(parent, style="Main.TFrame")
        header_frame.pack(fill="x", pady=(0, 15))
        
        section_title = ttk.Label(
            header_frame,
            text="Recent Invoices",
            style="Subtitle.TLabel"
        )
        section_title.pack(side="left")
        
        # Delete button for selected invoices
        delete_button = tk.Button(
            header_frame,
            text="Delete Selected",
            command=self.delete_selected_invoice,
            bg=SmartStockStyles.COLORS["error"],
            fg="white",
            font=("Segoe UI", 10),
            relief="raised",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        delete_button.pack(side="right", padx=(0, 10))

        # Save as PDF button
        save_pdf_button = tk.Button(
            header_frame,
            text="Save as PDF",
            command=self.export_selected_invoice_pdf,
            bg=SmartStockStyles.COLORS["primary"],
            fg="white",
            font=("Segoe UI", 10),
            relief="raised",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        save_pdf_button.pack(side="right")
        
        list_card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        list_card.pack(fill="both", expand=True)
        
        self.invoice_tree = ttk.Treeview(
            list_card,
            columns=("Invoice Number", "Date", "Client", "Amount", "Status"),
            show="headings",
            height=15
        )
        
        self.invoice_tree.heading("Invoice Number", text="Invoice #")
        self.invoice_tree.heading("Date", text="Date")
        self.invoice_tree.heading("Client", text="Client")
        self.invoice_tree.heading("Amount", text="Amount")
        self.invoice_tree.heading("Status", text="Status")
        
        self.invoice_tree.column("Invoice Number", width=100)
        self.invoice_tree.column("Date", width=100)
        self.invoice_tree.column("Client", width=150)
        self.invoice_tree.column("Amount", width=100)
        self.invoice_tree.column("Status", width=80)
        
        scrollbar = ttk.Scrollbar(list_card, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        self.invoice_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.invoice_tree.bind("<<TreeviewSelect>>", self.on_invoice_select)
        
        self.update_invoice_list()
    
    def create_invoice_form(self, parent):
        """Create the invoice form section"""
        form_card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        form_card.pack(fill="both", expand=True)
        
        # Title and button header
        title_frame = ttk.Frame(form_card, style="Card.TFrame")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="Create New Invoice",
            style="Subtitle.TLabel"
        )
        title_label.pack(side="left")
        
        # Improved Create Invoice button with explicit styling
        create_button = tk.Button(
            title_frame,
            text="Create Invoice",
            command=self.create_invoice,
            bg=SmartStockStyles.COLORS["primary"],
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="raised",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        create_button.pack(side="right")
        
        # Client Information
        client_frame = ttk.Frame(form_card, style="Card.TFrame")
        client_frame.pack(fill="x", pady=(0, 20))
        
        client_label = ttk.Label(
            client_frame,
            text="Client Information",
            font=("Segoe UI", 12, "bold"),
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        client_label.pack(anchor="w", pady=(0, 10))
        
        # Client Name
        name_label = ttk.Label(
            client_frame,
            text="Client Name",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        name_label.pack(anchor="w", pady=(0, 5))
        
        self.client_name_entry = tk.Entry(client_frame)
        SmartStockStyles.apply_entry_style(self.client_name_entry)
        self.client_name_entry.pack(fill="x", pady=(0, 10))
        
        # Client Email
        email_label = ttk.Label(
            client_frame,
            text="Client Email",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        email_label.pack(anchor="w", pady=(0, 5))
        
        self.client_email_entry = tk.Entry(client_frame)
        SmartStockStyles.apply_entry_style(self.client_email_entry)
        self.client_email_entry.pack(fill="x", pady=(0, 10))
        
        # Client Address
        address_label = ttk.Label(
            client_frame,
            text="Billing Address",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        address_label.pack(anchor="w", pady=(0, 5))
        
        self.client_address_entry = tk.Entry(client_frame)
        SmartStockStyles.apply_entry_style(self.client_address_entry)
        self.client_address_entry.pack(fill="x", pady=(0, 10))
        
        # Product Selection
        products_frame = ttk.Frame(form_card, style="Card.TFrame")
        products_frame.pack(fill="x", pady=(0, 20))
        
        # Products header with search
        products_header = ttk.Frame(products_frame, style="Card.TFrame")
        products_header.pack(fill="x", pady=(0, 10))
        
        products_label = ttk.Label(
            products_header,
            text="Select Products",
            font=("Segoe UI", 12, "bold"),
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        products_label.pack(side="left")
        
        # Search bar
        search_label = ttk.Label(
            products_header,
            text="Search:",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        search_label.pack(side="right", padx=(0, 5))
        
        self.search_entry = tk.Entry(products_header, width=30)
        SmartStockStyles.apply_entry_style(self.search_entry)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self.filter_products)
        
        # Available Products Treeview
        self.product_tree = ttk.Treeview(
            products_frame,
            columns=("Name", "Price", "Quantity"),
            show="headings",
            height=5
        )
        self.product_tree.heading("Name", text="Product Name")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Quantity", text="Available")
        self.product_tree.column("Name", width=150)
        self.product_tree.column("Price", width=80)
        self.product_tree.column("Quantity", width=80)
        self.product_tree.pack(fill="x", pady=(0, 10))
        
        # Quantity Entry
        qty_frame = ttk.Frame(products_frame, style="Card.TFrame")
        qty_frame.pack(fill="x", pady=(0, 10))
        
        qty_label = ttk.Label(
            qty_frame,
            text="Quantity:",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        qty_label.pack(side="left")
        
        self.qty_entry = tk.Entry(qty_frame, width=10)
        SmartStockStyles.apply_entry_style(self.qty_entry)
        self.qty_entry.pack(side="left", padx=5)
        
        # Improved Add button with explicit styling
        add_button = tk.Button(
            qty_frame,
            text="Add to Invoice",
            command=self.add_product_to_invoice,
            bg=SmartStockStyles.COLORS["primary"],
            fg="white",
            font=("Segoe UI", 10),
            relief="raised",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        add_button.pack(side="left")
        
        # Selected Products Treeview
        selected_header = ttk.Frame(products_frame, style="Card.TFrame")
        selected_header.pack(fill="x", pady=(10, 10))
        
        selected_label = ttk.Label(
            selected_header,
            text="Selected Products",
            font=("Segoe UI", 12, "bold"),
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        selected_label.pack(side="left")
        
        # Improved Remove button with explicit styling
        remove_button = tk.Button(
            selected_header,
            text="Remove Selected",
            command=self.remove_product_from_invoice,
            bg=SmartStockStyles.COLORS["error"],
            fg="white",
            font=("Segoe UI", 10),
            relief="raised",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        remove_button.pack(side="right")
        
        self.selected_tree = ttk.Treeview(
            products_frame,
            columns=("Name", "Price", "Quantity"),
            show="headings",
            height=5
        )
        self.selected_tree.heading("Name", text="Product Name")
        self.selected_tree.heading("Price", text="Price")
        self.selected_tree.heading("Quantity", text="Quantity")
        self.selected_tree.column("Name", width=150)
        self.selected_tree.column("Price", width=80)
        self.selected_tree.column("Quantity", width=80)
        self.selected_tree.pack(fill="x", pady=(0, 20))
        
        # Update product list
        self.update_product_list()
    
    def update_product_list(self):
        """Update the available products Treeview"""
        self.product_tree.delete(*self.product_tree.get_children())
        for product in self.products:
            self.product_tree.insert(
                "",
                "end",
                values=(product["name"], f"${product['price']:.2f}", product["quantity"])
            )
    
    def update_selected_products(self):
        """Update the selected products Treeview"""
        self.selected_tree.delete(*self.selected_tree.get_children())
        for product in self.selected_products:
            self.selected_tree.insert(
                "",
                "end",
                values=(product["name"], f"${product['price']:.2f}", product["quantity"])
            )
    
    def update_invoice_list(self):
        """Update the invoice list"""
        self.invoice_tree.delete(*self.invoice_tree.get_children())
        for invoice in self.invoices:
            self.invoice_tree.insert(
                "",
                "end",
                values=(
                    invoice["invoice_number"],
                    invoice["date"],
                    invoice["client_name"],
                    f"${invoice['total_amount']:.2f}",
                    invoice["status"]
                )
            )
    
    def add_product_to_invoice(self):
        """Add a selected product with quantity to the invoice"""
        selected = self.product_tree.selection()
        if not selected:
            self.show_message("Please select a product", "warning")
            return
        
        qty_str = self.qty_entry.get().strip()
        try:
            qty = int(qty_str)
            if qty <= 0:
                self.show_message("Quantity must be a positive number", "error")
                return
        except ValueError:
            self.show_message("Please enter a valid quantity", "error")
            return
        
        index = self.product_tree.index(selected[0])
        product = self.products[index]
        
        if qty > product["quantity"]:
            self.show_message(f"Requested quantity ({qty}) exceeds available stock ({product['quantity']})", "error")
            return
        
        self.selected_products.append({
            "name": product["name"],
            "price": product["price"],
            "quantity": qty
        })
        
        self.update_selected_products()
        self.qty_entry.delete(0, tk.END)
        self.show_message(f"Added {qty} x {product['name']} to invoice", "success")
    
    def remove_product_from_invoice(self):
        """Remove a product from the selected products list"""
        selected = self.selected_tree.selection()
        if not selected:
            self.show_message("Please select a product to remove", "warning")
            return
        
        index = self.selected_tree.index(selected[0])
        product_name = self.selected_products[index]["name"]
        del self.selected_products[index]
        self.update_selected_products()
        self.show_message(f"Removed {product_name} from invoice", "success")
    
    def on_invoice_select(self, event):
        """Handle invoice selection"""
        selected_items = self.invoice_tree.selection()
        if selected_items:
            invoice = self.invoices[self.invoice_tree.index(selected_items[0])]
            self.client_name_entry.delete(0, tk.END)
            self.client_name_entry.insert(0, invoice["client_name"])
            self.client_email_entry.delete(0, tk.END)
            self.client_email_entry.insert(0, invoice["client_email"])
            self.client_address_entry.delete(0, tk.END)
            self.client_address_entry.insert(0, invoice["client_address"])
            self.selected_products = [
                {"name": p["name"], "price": p["price"], "quantity": p["quantity"]}
                for p in invoice["products"]
            ]
            self.update_selected_products()
    
    def create_invoice(self):
        """Create a new invoice and update inventory"""
        try:
            # Get client information
            client_name = self.client_name_entry.get().strip()
            client_email = self.client_email_entry.get().strip()
            client_address = self.client_address_entry.get().strip()
            
            if not client_name:
                self.show_message("Please enter client name", "error")
                return
            if not client_email:
                self.show_message("Please enter client email", "error")
                return
            if not client_address:
                self.show_message("Please enter client billing address", "error")
                return
            if not self.selected_products:
                self.show_message("Please add at least one product to the invoice", "error")
                return
            
            # Calculate total amount
            total_amount = sum(p["price"] * p["quantity"] for p in self.selected_products)
            
            # Generate invoice number
            invoice_number = f"INV-{datetime.now().year}-{len(self.invoices) + 1:03d}"
            
            # Create invoice
            invoice = {
                "invoice_number": invoice_number,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "seller": {
                    "company_name": "SmartStock Electronics",
                    "address": "123 Tech Lane, Innovation City, TX 75001",
                    "contact": "contact@smartstock.com | +1-800-555-1234",
                    "tax_id": "US-TAX-123456789"
                },
                "client_name": client_name,
                "client_email": client_email,
                "client_address": client_address,
                "products": [
                    {
                        "name": p["name"],
                        "price": p["price"],
                        "quantity": p["quantity"]
                    } for p in self.selected_products
                ],
                "total_amount": total_amount,
                "status": "Pending",
                "logo": "[Company Logo]"
            }
            
            # Update inventory
            for selected_product in self.selected_products:
                for product in self.products:
                    if product["name"] == selected_product["name"]:
                        product["quantity"] -= selected_product["quantity"]
                        if product["quantity"] < 0:
                            self.show_message(f"Error: Insufficient stock for {product['name']}", "error")
                            return
            
            # Save updated inventory to data.json
            self.save_to_json()
            
            # Add to invoices list and save
            self.invoices.append(invoice)
            self.save_invoices()
            
            # Update UI
            self.update_invoice_list()
            self.update_product_list()
            
            # Clear form
            self.client_name_entry.delete(0, tk.END)
            self.client_email_entry.delete(0, tk.END)
            self.client_address_entry.delete(0, tk.END)
            self.selected_products.clear()
            self.update_selected_products()
            
            self.show_message(f"Invoice {invoice_number} created successfully", "success")
            
        except Exception as e:
            self.show_message(f"Error creating invoice: {str(e)}", "error")
    
    def update_invoices(self, products):
        """Update products and refresh UI"""
        self.products = products
        self.update_product_list()
    
    def filter_products(self, event=None):
        """Filter products based on search text"""
        search_text = self.search_entry.get().lower()
        self.product_tree.delete(*self.product_tree.get_children())
        
        for product in self.products:
            if search_text in product["name"].lower():
                self.product_tree.insert(
                    "",
                    "end",
                    values=(product["name"], f"${product['price']:.2f}", product["quantity"])
                )
    
    def delete_selected_invoice(self):
        """Delete the selected invoice"""
        selected_items = self.invoice_tree.selection()
        if not selected_items:
            self.show_message("Please select an invoice to delete", "warning")
            return
        
        # Get the selected invoice
        index = self.invoice_tree.index(selected_items[0])
        invoice = self.invoices[index]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", 
                             f"Are you sure you want to delete invoice {invoice['invoice_number']}?"):
            # Restore product quantities
            for product in invoice["products"]:
                for p in self.products:
                    if p["name"] == product["name"]:
                        p["quantity"] += product["quantity"]
            
            # Remove the invoice
            del self.invoices[index]
            
            # Save changes
            self.save_invoices()
            self.save_to_json()  # Save updated product quantities
            
            # Update UI
            self.update_invoice_list()
            self.update_product_list()
            
            self.show_message(f"Invoice {invoice['invoice_number']} deleted successfully", "success")
    
    def export_selected_invoice_pdf(self):
        """Export the selected invoice as PDF"""
        selected_items = self.invoice_tree.selection()
        if not selected_items:
            self.show_message("Please select an invoice to save", "warning")
            return
        
        # Get the selected invoice
        index = self.invoice_tree.index(selected_items[0])
        invoice = self.invoices[index]
        
        try:
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Header Section
            # Company Logo placeholder (you can add actual logo later)
            pdf.set_font("Arial", "B", 24)
            pdf.cell(0, 20, "SmartStock Electronics", ln=True, align="C")
            
            # Invoice Title
            pdf.set_font("Arial", "B", 20)
            pdf.cell(0, 15, "INVOICE", ln=True, align="C")
            pdf.ln(5)
            
            # Invoice Details
            pdf.set_font("Arial", "", 12)
            pdf.cell(60, 10, f"Invoice Number: {invoice['invoice_number']}", ln=0)
            pdf.cell(60, 10, f"Date: {invoice['date']}", ln=0)
            pdf.cell(60, 10, f"Due Date: {invoice['due_date']}", ln=True)
            pdf.ln(10)
            
            # Seller Information
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "From:", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, "SmartStock Electronics", ln=True)
            pdf.cell(0, 10, "123 Tech Lane, Innovation City, TX 75001", ln=True)
            pdf.cell(0, 10, "contact@smartstock.com | +1-800-555-1234", ln=True)
            pdf.cell(0, 10, "Tax ID: US-TAX-123456789", ln=True)
            pdf.ln(10)
            
            # Client Information
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Bill To:", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, invoice["client_name"], ln=True)
            pdf.cell(0, 10, invoice["client_address"], ln=True)
            pdf.cell(0, 10, invoice["client_email"], ln=True)
            pdf.ln(10)
            
            # Line Items Table Header
            pdf.set_font("Arial", "B", 12)
            pdf.cell(80, 10, "Description", 1)
            pdf.cell(30, 10, "Quantity", 1)
            pdf.cell(40, 10, "Unit Price", 1)
            pdf.cell(40, 10, "Amount", 1)
            pdf.ln()
            
            # Line Items
            pdf.set_font("Arial", "", 12)
            total = 0
            for product in invoice["products"]:
                amount = product["price"] * product["quantity"]
                total += amount
                pdf.cell(80, 10, product["name"], 1)
                pdf.cell(30, 10, str(product["quantity"]), 1)
                pdf.cell(40, 10, f"${product['price']:.2f}", 1)
                pdf.cell(40, 10, f"${amount:.2f}", 1)
                pdf.ln()
            
            # Total
            pdf.set_font("Arial", "B", 12)
            pdf.cell(150, 10, "Total Amount:", 1)
            pdf.cell(40, 10, f"${total:.2f}", 1)
            pdf.ln(15)
            
            # Footer
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, "SmartStock Electronics | 123 Tech Lane, Innovation City, TX 75001", ln=True)
            pdf.cell(0, 10, "contact@smartstock.com | +1-800-555-1234", ln=True)
            pdf.cell(0, 10, "Tax included per local regulations", ln=True)
            
            # Ask user where to save the PDF
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
                title="Save Invoice As",
                initialfile=f"invoice_{invoice['invoice_number']}.pdf"
            )
            
            if file_path:
                pdf.output(file_path)
                self.show_message(f"Invoice saved as {os.path.basename(file_path)}", "success")
            
        except Exception as e:
            self.show_message(f"Error saving invoice: {str(e)}", "error")