import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from styles import SmartStockStyles

class SmartStockLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SmartStock Login")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg=SmartStockStyles.COLORS["bg_light"])
        
        # Center window on screen
        self.center_window(400, 500)
        
        # Configure styles
        self.style = ttk.Style()
        SmartStockStyles.configure_ttk_styles(self.style)
        
        # Create login UI
        self.create_login_ui()
        
    def center_window(self, width, height):
        """Center window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_login_ui(self):
        """Create the login user interface"""
        # Main container frame
        main_frame = ttk.Frame(self.root, style='Main.TFrame', padding=(20, 20, 20, 20))
        main_frame.pack(fill='both', expand=True)
        
        # Logo and title
        logo_frame = ttk.Frame(main_frame, style='Main.TFrame')
        logo_frame.pack(fill='x', pady=(0, 30))
        
        # Logo
        logo_label = ttk.Label(
            logo_frame, 
            text="📊", 
            font=("Segoe UI", 48),
            background=SmartStockStyles.COLORS["bg_light"]
        )
        logo_label.pack(pady=(20, 0))
        
        # Title
        title_label = ttk.Label(
            logo_frame, 
            text="SmartStock", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(5, 0))
        
        # Subtitle
        subtitle_label = ttk.Label(
            logo_frame, 
            text="Inventory Management System",
            font=("Segoe UI", 12),
            foreground=SmartStockStyles.COLORS["text_muted"],
            background=SmartStockStyles.COLORS["bg_light"]
        )
        subtitle_label.pack()
        
        # Login form - wrapped in a card-like frame
        login_card = ttk.Frame(
            main_frame, 
            style='Card.TFrame',
            padding=(SmartStockStyles.SPACING["lg"], 
                    SmartStockStyles.SPACING["lg"],
                    SmartStockStyles.SPACING["lg"],
                    SmartStockStyles.SPACING["lg"])
        )
        login_card.pack(fill='x', padx=20)
        
        # Username
        username_label = ttk.Label(
            login_card, 
            text="Username",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        username_label.pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(login_card, width=30)
        SmartStockStyles.apply_entry_style(self.username_entry)
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        # Password
        password_label = ttk.Label(
            login_card, 
            text="Password",
            font=SmartStockStyles.FONTS["body"],
            background=SmartStockStyles.COLORS["bg_card"],
            foreground=SmartStockStyles.COLORS["text_dark"]
        )
        password_label.pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(login_card, width=30, show="•")
        SmartStockStyles.apply_entry_style(self.password_entry)
        self.password_entry.pack(fill='x', pady=(0, 15))
        
        # Login button
        login_button = tk.Button(login_card, text="Login", command=self.login)
        SmartStockStyles.apply_button_style(login_button, "primary")
        login_button.pack(fill='x', pady=(10, 0), ipady=8)
        
        # Footer
        footer_frame = ttk.Frame(main_frame, style='Main.TFrame')
        footer_frame.pack(fill='x', side='bottom', pady=(20, 0))
        
        version_label = ttk.Label(
            footer_frame, 
            text="v2.0.0", 
            font=SmartStockStyles.FONTS["small"],
            foreground=SmartStockStyles.COLORS["text_muted"],
            background=SmartStockStyles.COLORS["bg_light"]
        )
        version_label.pack(side='right')
        
        # Bind enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
    def login(self):
        """Handle login process"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "pass123":
            messagebox.showinfo("Login Success", "Welcome to SmartStock!")
            self.root.destroy()
            # Import main application here to avoid circular imports
            from smartstock import SmartStock
            app = SmartStock(username)
            app.run()
        else:
            error_frame = tk.Frame(
                self.root, 
                bg=SmartStockStyles.COLORS["error"],
                height=40
            )
            error_frame.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.9)
            
            error_label = tk.Label(
                error_frame,
                text="Invalid username or password",
                bg=SmartStockStyles.COLORS["error"],
                fg="white",
                font=SmartStockStyles.FONTS["body"]
            )
            error_label.pack(fill='both', expand=True)
            
            # Remove the error message after 3 seconds
            self.root.after(3000, error_frame.destroy)
    
    def run(self):
        """Run the login application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the login application
    login_app = SmartStockLogin()
    login_app.run()