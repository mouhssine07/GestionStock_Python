import tkinter as tk
from tkinter import ttk, filedialog
from docx import Document
from fpdf import FPDF
from styles import SmartStockStyles
from datetime import datetime
import os

class ProductsView:
    def __init__(self, parent, products, save_to_json_callback, show_message_callback):
        self.parent = parent
        self.products = products
        self.save_to_json = save_to_json_callback
        self.show_message = show_message_callback
        self.create_products_ui()
    
    def create_products_ui(self):
        """Create the products UI"""
        self.create_header()
        
        content_container = ttk.Frame(self.parent, style="Main.TFrame")
        content_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        form_frame = ttk.Frame(content_container, style="Main.TFrame")
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        self.create_product_form(form_frame)
        
        products_frame = ttk.Frame(content_container, style="Main.TFrame")
        products_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))
        self.create_products_display(products_frame)
    
    def create_header(self):
        """Create the header section"""
        header_frame = ttk.Frame(self.parent, style="Main.TFrame")
        header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Product Manager",
            style="Title.TLabel"
        )
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Manage your inventory with ease",
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
    
    def create_product_form(self, parent):
        """Create the product input form"""
        section_title = ttk.Label(
            parent,
            text="Add New Product",
            style="Subtitle.TLabel"
        )
        section_title.pack(anchor="w", pady=(0, 15))
        
        form_card = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=SmartStockStyles.SPACING["lg"]
        )
        form_card.pack(fill="both", expand=True)
        
        name_label = ttk.Label(
            form_card,
            text="Product Name",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        name_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_name = tk.Entry(form_card)
        SmartStockStyles.apply_entry_style(self.entry_name)
        self.entry_name.pack(fill="x", pady=(0, 15))
        
        quantity_label = ttk.Label(
            form_card,
            text="Quantity",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        quantity_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_quantity = tk.Entry(form_card)
        SmartStockStyles.apply_entry_style(self.entry_quantity)
        self.entry_quantity.pack(fill="x", pady=(0, 15))
        
        price_label = ttk.Label(
            form_card,
            text="Price ($)",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        price_label.pack(anchor="w", pady=(0, 5))
        
        self.entry_price = tk.Entry(form_card)
        SmartStockStyles.apply_entry_style(self.entry_price)
        self.entry_price.pack(fill="x", pady=(0, 15))
        
        add_button = tk.Button(
            form_card,
            text="Add Product",
            command=self.add_product
        )
        SmartStockStyles.apply_button_style(add_button, "primary")
        add_button.pack(fill="x", pady=(15, 0), ipady=8)
        
        button_frame = ttk.Frame(form_card, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(20, 0))
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        ai_button = tk.Button(
            button_frame,
            text="AI Assistant 🤖",
            command=self.show_ai_assistant
        )
        SmartStockStyles.apply_button_style(ai_button, "secondary")
        ai_button.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="ew")
        
        word_button = tk.Button(
            button_frame,
            text="Save to Word",
            command=self.save_to_word
        )
        SmartStockStyles.apply_button_style(word_button, "outline")
        word_button.grid(row=0, column=1, padx=(5, 0), pady=(0, 5), sticky="ew")
        
        pdf_button = tk.Button(
            button_frame,
            text="Export to PDF",
            command=self.export_to_pdf
        )
        SmartStockStyles.apply_button_style(pdf_button, "outline")
        pdf_button.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="ew")
        
        load_button = tk.Button(
            button_frame,
            text="Load from Word",
            command=self.load_from_word
        )
        SmartStockStyles.apply_button_style(load_button, "outline")
        load_button.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="ew")
    
    def create_products_display(self, parent):
        """Create the products display section"""
        header_frame = ttk.Frame(parent, style="Main.TFrame")
        header_frame.pack(fill="x", pady=(0, 15))
        
        section_title = ttk.Label(
            header_frame,
            text="Product List",
            style="Subtitle.TLabel"
        )
        section_title.pack(side="left")
        
        search_frame = ttk.Frame(header_frame, style="Main.TFrame")
        search_frame.pack(side="right")
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=20
        )
        SmartStockStyles.apply_entry_style(search_entry)
        search_entry.pack(side="left", padx=(0, 5))
        
        search_button = tk.Button(
            search_frame,
            text="🔍 Search",
            command=self.search_product
        )
        SmartStockStyles.apply_button_style(search_button, "secondary")
        search_button.pack(side="right")
        
        table_card = ttk.Frame(
            parent,
            style="Card.TFrame",
            padding=(10, 10, 10, 10)
        )
        table_card.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(
            table_card, 
            columns=("Name", "Quantity", "Price"), 
            show="headings",
            height=12
        )
        
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Quantity", width=80, anchor="center")
        self.tree.column("Price", width=80, anchor="e")
        
        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add delete button
        delete_button = tk.Button(
            table_card,
            text="🗑️ Delete Selected",
            command=self.delete_selected_product
        )
        SmartStockStyles.apply_button_style(delete_button, "error")
        delete_button.pack(pady=10)
        
        # Add update button
        update_button = tk.Button(
            table_card,
            text="✏️ Update Selected",
            command=self.update_selected_product
        )
        SmartStockStyles.apply_button_style(update_button, "secondary")
        update_button.pack(pady=(0, 10))
        
        status_frame = ttk.Frame(parent, style="Main.TFrame")
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ttk.Label(
            status_frame,
            text="0 products in inventory",
            font=SmartStockStyles.FONTS["small"],
            background=SmartStockStyles.COLORS["bg_light"],
            foreground=SmartStockStyles.COLORS["text_muted"]
        )
        self.status_label.pack(side="left")
        
        self.update_tree()
    
    def add_product(self):
        """Add a product to the inventory"""
        name = self.entry_name.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()
        
        if not name:
            self.show_message("Please enter a product name", "error")
            return
            
        try:
            quantity = int(quantity)
            if quantity < 0:
                self.show_message("Quantity must be a positive number", "error")
                return
        except ValueError:
            self.show_message("Quantity must be a valid number", "error")
            return
            
        try:
            price = float(price)
            if price < 0:
                self.show_message("Price must be a positive number", "error")
                return
        except ValueError:
            self.show_message("Price must be a valid number", "error")
            return
        
        product = {"name": name, "quantity": quantity, "price": price}
        self.products.append(product)
        
        self.update_tree()
        self.save_to_json()
        
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        
        self.show_message(f"Product '{name}' added successfully", "success")
    
    def update_tree(self):
        """Update the treeview with current products"""
        self.tree.delete(*self.tree.get_children())
        
        for p in self.products:
            self.tree.insert(
                "", 
                "end", 
                values=(p["name"], p["quantity"], f"${p['price']:.2f}")
            )
        
        count = len(self.products)
        self.status_label.config(
            text=f"{count} {'product' if count == 1 else 'products'} in inventory"
        )
    
    def save_to_word(self):
        """Save products to a Word document"""
        if not self.products:
            self.show_message("No products to save", "warning")
            return
            
        try:
            doc = Document()
            doc.add_heading("SmartStock - Product List", 0)
            
            doc.add_paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}")
            doc.add_paragraph("")
            
            table = doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'
            
            header_cells = table.rows[0].cells
            header_cells[0].text = 'Product Name'
            header_cells[1].text = 'Quantity'
            header_cells[2].text = 'Price'
            
            for cell in header_cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.bold = True
            
            for p in self.products:
                row_cells = table.add_row().cells
                row_cells[0].text = p["name"]
                row_cells[1].text = str(p["quantity"])
                row_cells[2].text = f"${p['price']:.2f}"
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
                title="Save Product List As",
                initialfile="products.docx"
            )
            
            if file_path:
                doc.save(file_path)
                self.show_message(f"Products saved to {os.path.basename(file_path)}", "success")
            
        except Exception as e:
            self.show_message(f"Error saving to Word: {str(e)}", "error")
    
    def export_to_pdf(self):
        """Export products to a PDF document"""
        if not self.products:
            self.show_message("No products to export", "warning")
            return
            
        try:
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", size=12)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="SmartStock - Product List", ln=True, align='C')
            
            pdf.set_font("Arial", '', 10)
            pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(90, 10, "Product Name", border=1)
            pdf.cell(40, 10, "Quantity", border=1, align='C')
            pdf.cell(60, 10, "Price", border=1, align='R')
            pdf.ln()
            
            pdf.set_font("Arial", '', 12)
            for p in self.products:
                pdf.cell(90, 10, p["name"], border=1)
                pdf.cell(40, 10, str(p["quantity"]), border=1, align='C')
                pdf.cell(60, 10, f"${p['price']:.2f}", border=1, align='R')
                pdf.ln()
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
                title="Save Product List As",
                initialfile="products.pdf"
            )
            
            if file_path:
                pdf.output(file_path)
                self.show_message(f"Products exported to {os.path.basename(file_path)}", "success")
            
        except Exception as e:
            self.show_message(f"Error exporting to PDF: {str(e)}", "error")
    
    def load_from_word(self):
        """Load products from a Word document"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
                title="Open Product List",
                initialfile="products.docx"
            )
            
            if not file_path:
                return
                
            doc = Document(file_path)
            tables = doc.tables
            
            if not tables:
                self.show_message("No table found in the Word document", "warning")
                return
                
            table = tables[0]
            self.products.clear()
            
            for row in table.rows[1:]:
                try:
                    name = row.cells[0].text.strip()
                    quantity = int(row.cells[1].text.strip())
                    price = float(row.cells[2].text.strip().replace('$', ''))
                    
                    self.products.append({
                        "name": name,
                        "quantity": quantity,
                        "price": price
                    })
                except (ValueError, IndexError) as e:
                    self.show_message(f"Skipping invalid row: {str(e)}", "warning")
                    continue
            
            self.update_tree()
            self.save_to_json()
            self.show_message(f"Products loaded from {os.path.basename(file_path)}", "success")
            
        except Exception as e:
            self.show_message(f"Error loading products: {str(e)}", "error")
    
    def search_product(self):
        """Search for a product by name"""
        search_term = self.search_var.get().strip().lower()
        
        self.tree.delete(*self.tree.get_children())
        
        if not search_term:
            for p in self.products:
                self.tree.insert(
                    "", 
                    "end", 
                    values=(p["name"], p["quantity"], f"${p['price']:.2f}")
                )
            count = len(self.products)
            self.status_label.config(
                text=f"{count} {'product' if count == 1 else 'products'} in inventory"
            )
            return
            
        found = False
        for p in self.products:
            if search_term in p["name"].lower():
                self.tree.insert(
                    "", 
                    "end", 
                    values=(p["name"], p["quantity"], f"${p['price']:.2f}")
                )
                found = True
        
        count = len(self.tree.get_children())
        self.status_label.config(
            text=f"{count} {'result' if count == 1 else 'results'} found"
        )
        if not found:
            self.show_message("No products matching your search", "warning")
    
    def show_ai_assistant(self):
        """Show AI assistant tips"""
        if not self.products:
            self.show_message("No products to analyze", "warning")
            return
            
        tips = self.get_ai_tips()
        
        popup = tk.Toplevel(self.parent)
        popup.title("SmartStock AI Assistant")
        popup.geometry("400x300")
        popup.configure(bg=SmartStockStyles.COLORS["bg_light"])
        popup.transient(self.parent)
        
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        popup.geometry(f"400x300+{x}+{y}")
        
        frame = ttk.Frame(popup, style="Card.TFrame", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ttk.Label(
            frame,
            text="AI Inventory Insights",
            font=SmartStockStyles.FONTS["subheader"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        tips_frame = ttk.Frame(frame, style="Card.TFrame")
        tips_frame.pack(fill="both", expand=True)
        
        tips_text = tk.Text(
            tips_frame,
            wrap="word",
            height=8,
            font=SmartStockStyles.FONTS["body"],
            bg=SmartStockStyles.COLORS["bg_card"],
            fg=SmartStockStyles.COLORS["text_dark"],
            relief="flat",
            padx=5,
            pady=5
        )
        tips_text.pack(fill="both", expand=True)
        tips_text.insert("1.0", tips)
        tips_text.config(state="disabled")
        
        close_btn = tk.Button(frame, text="Got it!", command=popup.destroy)
        SmartStockStyles.apply_button_style(close_btn, "primary")
        close_btn.pack(pady=(15, 0), ipady=5)
    
    def get_ai_tips(self):
        """Generate AI tips based on product data"""
        tips = []
        
        low_stock = [p for p in self.products if p["quantity"] < 5]
        if low_stock:
            tips.append("⚠️ Low Stock Alerts:")
            for p in low_stock:
                tips.append(f"   • {p['name']}: {p['quantity']} units left")
        
        expensive_products = [p for p in self.products if p["price"] > 100]
        if expensive_products:
            tips.append("\n💡 High-Value Items (Consider Promotions):")
            for p in expensive_products:
                tips.append(f"   • {p['name']}: ${p['price']:.2f}")
        
        total_value = sum(p["quantity"] * p["price"] for p in self.products)
        tips.append(f"\n💰 Total Inventory Value: ${total_value:.2f}")
        
        avg_price = sum(p["price"] for p in self.products) / len(self.products) if self.products else 0
        tips.append(f"📊 Average Product Price: ${avg_price:.2f}")
        
        if not tips:
            tips.append("✅ All inventory levels look good! No action needed.")
            
        return "\n".join(tips)
    
    def update_products(self, products):
        """Update products and refresh UI"""
        self.products = products
        self.update_tree()
    
    def delete_selected_product(self):
        """Delete the selected product from the inventory and data.json"""
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_message("Please select a product to delete", "warning")
            return
        
        # Get the product name from the selected item
        product_name = self.tree.item(selected_item[0])['values'][0]
        
        # Create a new list excluding the selected product
        new_products = [p for p in self.products if p["name"] != product_name]
        
        # Update the products list only if the save is successful
        try:
            self.products[:] = new_products  # Update the list in-place
            self.save_to_json()  # Save to data.json
            self.update_tree()   # Refresh the Treeview
            self.show_message(f"Product '{product_name}' deleted successfully", "success")
        except Exception as e:
            self.show_message(f"Error deleting product: {str(e)}", "error")
            self.update_tree()  # Refresh Treeview to reflect unchanged products
    
    def update_selected_product(self):
        """Update the selected product in the inventory and data.json"""
        selected_item = self.tree.selection()
        if not selected_item:
            self.show_message("Please select a product to update", "warning")
            return
            
        # Get the current product details
        current_values = self.tree.item(selected_item[0])['values']
        current_name = current_values[0]
        
        # Create update popup
        popup = tk.Toplevel(self.parent)
        popup.title("Update Product")
        popup.geometry("500x600")
        popup.configure(bg=SmartStockStyles.COLORS["bg_light"])
        popup.transient(self.parent)
        popup.minsize(500, 600)
        
        # Center the popup
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 600) // 2
        popup.geometry(f"500x600+{x}+{y}")
        
        # Create form frame with enhanced styling
        form_frame = ttk.Frame(popup, style="Card.TFrame", padding=40)
        form_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Title with enhanced styling
        title_label = ttk.Label(
            form_frame,
            text="Update Product",
            style="Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 30))
        
        # Name field with enhanced styling
        name_label = ttk.Label(
            form_frame,
            text="Product Name",
            font=("Segoe UI", 12, "bold"),
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        name_label.pack(anchor="w", pady=(0, 10))
        
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        SmartStockStyles.apply_entry_style(name_entry)
        name_entry.insert(0, current_values[0])
        name_entry.pack(fill="x", pady=(0, 25))
        
        # Quantity field with enhanced styling
        quantity_label = ttk.Label(
            form_frame,
            text="Quantity",
            font=("Segoe UI", 12, "bold"),
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        quantity_label.pack(anchor="w", pady=(0, 10))
        
        quantity_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        SmartStockStyles.apply_entry_style(quantity_entry)
        quantity_entry.insert(0, current_values[1])
        quantity_entry.pack(fill="x", pady=(0, 25))
        
        # Price field with enhanced styling
        price_label = ttk.Label(
            form_frame,
            text="Price ($)",
            font=("Segoe UI", 12, "bold"),
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        price_label.pack(anchor="w", pady=(0, 10))
        
        price_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        SmartStockStyles.apply_entry_style(price_entry)
        price_entry.insert(0, current_values[2].replace('$', ''))
        price_entry.pack(fill="x", pady=(0, 30))
        
        def save_update():
            try:
                # Get new values
                new_name = name_entry.get().strip()
                new_quantity = int(quantity_entry.get().strip())
                new_price = float(price_entry.get().strip())
                
                # Validate inputs
                if not new_name:
                    self.show_message("Please enter a product name", "error")
                    return
                    
                if new_quantity < 0:
                    self.show_message("Quantity must be a positive number", "error")
                    return
                    
                if new_price < 0:
                    self.show_message("Price must be a positive number", "error")
                    return
                
                # Update the product
                for product in self.products:
                    if product["name"] == current_name:
                        product["name"] = new_name
                        product["quantity"] = new_quantity
                        product["price"] = new_price
                        break
                
                # Save to JSON and update UI
                self.save_to_json()
                self.update_tree()
                self.show_message(f"Product updated successfully", "success")
                popup.destroy()
                
            except ValueError:
                self.show_message("Please enter valid numbers for quantity and price", "error")
            except Exception as e:
                self.show_message(f"Error updating product: {str(e)}", "error")
        
        # Save button with enhanced styling
        save_button = tk.Button(
            form_frame,
            text="Save Changes",
            command=save_update,
            font=("Segoe UI", 12, "bold")
        )
        SmartStockStyles.apply_button_style(save_button, "primary")
        save_button.pack(fill="x", pady=(20, 0), ipady=12)