"""
UI Styles and Theme Configuration
"""
import tkinter as tk
from tkinter import ttk


class AppStyles:
    """Application styling configuration"""
    
    # Color palette
    PRIMARY_COLOR = "#2C3E50"      # Dark blue-gray
    SECONDARY_COLOR = "#3498DB"    # Blue
    ACCENT_COLOR = "#27AE60"       # Green
    WARNING_COLOR = "#F39C12"       # Orange
    DANGER_COLOR = "#E74C3C"        # Red
    LIGHT_COLOR = "#ECF0F1"        # Light gray
    DARK_COLOR = "#1A252F"         # Very dark
    WHITE = "#FFFFFF"
    
    # Status colors
    STATUS_COLORS = {
        'On Time': '#27AE60',
        'Delayed': '#F39C12',
        'Cancelled': '#E74C3C',
        'Boarding': '#3498DB',
        'Departed': '#9B59B6',
        'Landed': '#1ABC9C'
    }
    
    @staticmethod
    def configure_styles(root):
        """Configure ttk styles for the application"""
        style = ttk.Style(root)
        
        # Configure main theme
        style.theme_use('clam')
        
        # Configure Treeview style
        style.configure('Treeview',
                       background=AppStyles.WHITE,
                       foreground='#2C3E50',
                       fieldbackground=AppStyles.WHITE,
                       rowheight=25,
                       font=('Segoe UI', 9))
        
        style.configure('Treeview.Heading',
                       background=AppStyles.PRIMARY_COLOR,
                       foreground=AppStyles.WHITE,
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure buttons
        style.configure('Primary.TButton',
                       background=AppStyles.SECONDARY_COLOR,
                       foreground=AppStyles.WHITE,
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Success.TButton',
                       background=AppStyles.ACCENT_COLOR,
                       foreground=AppStyles.WHITE,
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Danger.TButton',
                       background=AppStyles.DANGER_COLOR,
                       foreground=AppStyles.WHITE,
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        # Configure frames
        style.configure('Card.TFrame',
                       background=AppStyles.WHITE)
        
        return style
    
    @staticmethod
    def get_status_color(status):
        """Get color for flight status"""
        return AppStyles.STATUS_COLORS.get(status, AppStyles.PRIMARY_COLOR)


class Fonts:
    """Font configurations"""
    HEADER = ('Segoe UI', 16, 'bold')
    SUBHEADER = ('Segoe UI', 12, 'bold')
    NORMAL = ('Segoe UI', 10)
    SMALL = ('Segoe UI', 8)
    MONO = ('Consolas', 9)

