"""
SmartStock Styling System
This module provides consistent styling for the SmartStock application.
"""

class SmartStockStyles:
    """
    Centralized styling class for SmartStock application
    """
    
    # Main color palette
    COLORS = {
        "primary": "#5271FF",        # Bright blue
        "primary_dark": "#3A56E8",   # Darker blue for hover states
        "secondary": "#FF7D54",      # Coral orange for accent
        "success": "#2DD4BF",        # Turquoise for success states
        "warning": "#F5B14C",        # Amber yellow for warnings
        "error": "#F87171",          # Soft red for errors
        "bg_light": "#F8FAFC",       # Very light gray-blue for backgrounds
        "bg_card": "#FFFFFF",        # White for cards
        "text_dark": "#1E293B",      # Dark slate for primary text
        "text_muted": "#64748B",     # Muted blue-gray for secondary text
        "border": "#E2E8F0"          # Light gray for borders
    }
    
    # Font configurations
    FONTS = {
        "header": ("Segoe UI", 18, "bold"),
        "subheader": ("Segoe UI", 14, "bold"),
        "body": ("Segoe UI", 12),
        "small": ("Segoe UI", 10),
        "button": ("Segoe UI", 11, "bold")
    }
    
    # Spacing system (in pixels)
    SPACING = {
        "xs": 5,
        "sm": 10,
        "md": 15,
        "lg": 20,
        "xl": 30
    }
    
    # Button styles
    BUTTON_STYLES = {
        "primary": {
            "bg": COLORS["primary"],
            "fg": "#FFFFFF",
            "active_bg": COLORS["primary_dark"],
            "padx": 15,
            "pady": 8
        },
        "secondary": {
            "bg": COLORS["secondary"],
            "fg": "#FFFFFF",
            "active_bg": "#E86A42",
            "padx": 15,
            "pady": 8
        },
        "outline": {
            "bg": "#FFFFFF",
            "fg": COLORS["primary"],
            "active_bg": "#F1F5FF",
            "padx": 15,
            "pady": 8,
            "border_color": COLORS["primary"]
        }
    }
    
    # Entry field styles
    ENTRY_STYLES = {
        "bg": "#FFFFFF",
        "fg": COLORS["text_dark"],
        "border_color": COLORS["border"],
        "focus_border_color": COLORS["primary"]
    }
    
    # Card styling
    CARD_STYLES = {
        "bg": COLORS["bg_card"],
        "border_color": COLORS["border"],
        "border_width": 1,
        "relief": "solid",
        "padding": SPACING["md"]
    }
    
    @classmethod
    def configure_ttk_styles(cls, style):
        """Configure ttk styles for the application"""
        # Configure the theme
        style.theme_use('clam')
        
        # Configure frame styles
        style.configure('Main.TFrame', background=cls.COLORS["bg_light"])
        style.configure('Card.TFrame', 
                       background=cls.COLORS["bg_card"],
                       borderwidth=1,
                       relief="solid")
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       font=cls.FONTS["header"],
                       background=cls.COLORS["bg_light"],
                       foreground=cls.COLORS["text_dark"])
        
        style.configure('Subtitle.TLabel', 
                       font=cls.FONTS["subheader"],
                       background=cls.COLORS["bg_light"],
                       foreground=cls.COLORS["text_dark"])
                       
        style.configure('Body.TLabel', 
                       font=cls.FONTS["body"],
                       background=cls.COLORS["bg_light"],
                       foreground=cls.COLORS["text_dark"])
                       
        style.configure('Muted.TLabel', 
                       font=cls.FONTS["body"],
                       background=cls.COLORS["bg_light"],
                       foreground=cls.COLORS["text_muted"])
        
        # Configure entry styles
        style.configure('TEntry', 
                       font=cls.FONTS["body"],
                       fieldbackground=cls.ENTRY_STYLES["bg"])
        
        style.map('TEntry',
                 bordercolor=[('focus', cls.ENTRY_STYLES["focus_border_color"])])
        
        # Configure button styles
        style.configure('Primary.TButton',
                       font=cls.FONTS["button"],
                       background=cls.BUTTON_STYLES["primary"]["bg"],
                       foreground=cls.BUTTON_STYLES["primary"]["fg"])
        
        style.map('Primary.TButton',
                 background=[('active', cls.BUTTON_STYLES["primary"]["active_bg"])])
                 
        style.configure('Secondary.TButton',
                       font=cls.FONTS["button"],
                       background=cls.BUTTON_STYLES["secondary"]["bg"],
                       foreground=cls.BUTTON_STYLES["secondary"]["fg"])
        
        style.map('Secondary.TButton',
                 background=[('active', cls.BUTTON_STYLES["secondary"]["active_bg"])])
                 
        # Configure treeview styles
        style.configure("Treeview",
                       background=cls.COLORS["bg_card"],
                       foreground=cls.COLORS["text_dark"],
                       rowheight=30,
                       fieldbackground=cls.COLORS["bg_card"])
        
        style.configure("Treeview.Heading",
                       font=cls.FONTS["button"],
                       background=cls.COLORS["bg_light"],
                       foreground=cls.COLORS["text_dark"])
                       
        style.map("Treeview",
                 background=[('selected', cls.COLORS["primary"])],
                 foreground=[('selected', '#FFFFFF')])
    
    @classmethod
    def apply_button_style(cls, button, style_type="primary"):
        """Apply custom styling to a tk.Button widget"""
        button_style = cls.BUTTON_STYLES.get(style_type, cls.BUTTON_STYLES["primary"])
        
        button.configure(
            bg=button_style["bg"],
            fg=button_style["fg"],
            activebackground=button_style["active_bg"],
            activeforeground=button_style["fg"],
            padx=button_style["padx"],
            pady=button_style["pady"],
            borderwidth=0,
            cursor="hand2",
            font=cls.FONTS["button"]
        )
        
        # Add border for outline style
        if style_type == "outline":
            button.configure(borderwidth=1, highlightthickness=1, 
                           highlightbackground=button_style["border_color"])
    
    @classmethod        
    def apply_entry_style(cls, entry):
        """Apply custom styling to a tk.Entry widget"""
        entry.configure(
            bg=cls.ENTRY_STYLES["bg"],
            fg=cls.ENTRY_STYLES["fg"],
            insertbackground=cls.COLORS["text_dark"],
            highlightthickness=1,
            highlightbackground=cls.ENTRY_STYLES["border_color"],
            highlightcolor=cls.ENTRY_STYLES["focus_border_color"],
            font=cls.FONTS["body"],
            relief="flat"
        )