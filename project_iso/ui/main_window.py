"""
Main Window for ANFS Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
import config
from ui.styles import AppStyles
from ui.admin_panel import AdminPanel
from ui.public_panel import PublicPanel
from ui.dialogs import LoginDialog
from database.connection import DatabaseConnection


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(config.APP_TITLE)
        self.root.geometry(f"{config.APP_WIDTH}x{config.APP_HEIGHT}")
        self.root.minsize(900, 600)
        
        # Configure styles
        AppStyles.configure_styles(self.root)
        
        # Initialize variables
        self.is_logged_in = False
        self.current_user = None
        
        # Test database connection
        self._test_database_connection()
        
        # Create UI
        self._create_login_screen()
        
        # Start main loop
        self.root.mainloop()
    
    def _test_database_connection(self):
        """Test database connection on startup"""
        try:
            db = DatabaseConnection()
            conn = db.connect()
            if conn:
                print("✓ Database connected successfully!")
                db.close()
            else:
                self._show_db_error()
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            self._show_db_error()
    
    def _show_db_error(self):
        """Show database connection error"""
        error_win = tk.Toplevel(self.root)
        error_win.title("Database Connection Error")
        error_win.geometry("400x200")
        
        ttk.Label(error_win, 
                 text="Cannot connect to MySQL Database",
                 font=('Segoe UI', 12, 'bold')).pack(pady=20)
        
        ttk.Label(error_win, 
                 text="Please ensure:\n1. MySQL server is running\n2. Database credentials in config.py are correct\n3. Run 'python database/seed_data.py' to create database",
                 justify=tk.CENTER).pack(pady=10)
        
        ttk.Button(error_win, text="OK", command=error_win.destroy).pack(pady=10)
        
        error_win.grab_set()
    
    def _create_login_screen(self):
        """Create login screen"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Login container
        login_frame = ttk.Frame(self.root)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title = ttk.Label(login_frame, 
                         text="Airport Network\nFlight Scheduler",
                         font=('Segoe UI', 24, 'bold'),
                         justify=tk.CENTER)
        title.pack(pady=(0, 30))
        
        # Login options
        btn_frame = ttk.Frame(login_frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, 
                  text="Admin Login",
                  command=self._show_login,
                  width=20).pack(pady=5)
        
        ttk.Button(btn_frame,
                  text="Public View",
                  command=self._show_public_view,
                  width=20).pack(pady=5)
        
        # Info
        info = ttk.Label(login_frame,
                        text="Public View allows read-only access\nto flight information",
                        font=('Segoe UI', 9),
                        justify=tk.CENTER)
        info.pack(pady=20)
    
    def _show_login(self):
        """Show admin login dialog"""
        dialog = LoginDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.is_logged_in = True
            self.current_user = config.ADMIN_CREDENTIALS['username']
            self._create_main_app()
            messagebox.showinfo("Welcome", f"Welcome, Admin!")
    
    def _show_public_view(self):
        """Show public view without login"""
        self.is_logged_in = False
        self.current_user = "Public User"
        self._create_main_app()
    
    def _create_main_app(self):
        """Create main application interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top menu bar
        self._create_menu_bar()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create panels
        self.admin_panel = AdminPanel(self.notebook)
        self.public_panel = PublicPanel(self.notebook)
        
        # Add tabs based on login status
        if self.is_logged_in:
            self.notebook.add(self.admin_panel.get_frame(), text="Admin Panel")
        
        self.notebook.add(self.public_panel.get_frame(), text="Public Flight View")
        
        # Status bar
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Data", command=self._refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(status_frame, 
                 text=f"Logged in as: {self.current_user}",
                 font=('Segoe UI', 8)).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(status_frame,
                 text="ANFS v1.0",
                 font=('Segoe UI', 8)).pack(side=tk.RIGHT, padx=5)
    
    def _refresh_data(self):
        """Refresh all data"""
        try:
            # Refresh current tab
            current_tab = self.notebook.index(self.notebook.select())
            
            if self.is_logged_in and current_tab == 0:
                self.admin_panel.refresh_all()
            else:
                self.public_panel._load_all_flights()
            
            messagebox.showinfo("Success", "Data refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh: {str(e)}")
    
    def _logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.is_logged_in = False
            self.current_user = None
            self._create_login_screen()
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About",
                           "Airport Network Flight Scheduler (ANFS)\n\n"
                           "Version 1.0\n\n"
                           "A real-time flight scheduling system\n"
                           "with admin and public access panels.\n\n"
                           "Built with Python, Tkinter & MySQL")


def run():
    """Run the application"""
    MainWindow()


if __name__ == '__main__':
    run()

