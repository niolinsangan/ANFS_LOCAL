"""
Public Panel for ANFS Application - View Only Access
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.flight import Flight
from models.airport import Airport
from models.passenger import Passenger
from ui.dialogs import FlightDetailsDialog
from ui.styles import AppStyles
import config


class PublicPanel:
    """Public panel for viewing flight information (no edit rights)"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Create main container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = ttk.Label(main_container, 
                          text="Flight Information Portal", 
                          font=('Segoe UI', 18, 'bold'))
        header.pack(pady=(0, 10))
        
        subheader = ttk.Label(main_container,
                             text="View real-time flight schedules and status",
                             font=('Segoe UI', 10))
        subheader.pack(pady=(0, 15))
        
        # Search/Filter Section
        filter_frame = ttk.LabelFrame(main_container, text="Search & Filter", padding=10)
        filter_frame.pack(fill=tk.X, pady=5)
        
        # Origin Airport
        ttk.Label(filter_frame, text="From:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.origin_combo = ttk.Combobox(filter_frame, width=20)
        self.origin_combo.grid(row=0, column=1, padx=5, pady=3)
        
        # Destination Airport
        ttk.Label(filter_frame, text="To:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.dest_combo = ttk.Combobox(filter_frame, width=20)
        self.dest_combo.grid(row=0, column=3, padx=5, pady=3)
        
        # Flight Number Search
        ttk.Label(filter_frame, text="Flight #:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.flight_search = ttk.Entry(filter_frame, width=15)
        self.flight_search.grid(row=1, column=1, padx=5, pady=3)
        
        # Status Filter
        ttk.Label(filter_frame, text="Status:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['All'] + config.FLIGHT_STATUS, width=15)
        self.status_filter.grid(row=1, column=3, padx=5, pady=3)
        self.status_filter.set('All')
        
        # Buttons
        btn_frame = ttk.Frame(filter_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Search", command=self._search_flights).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Show All Flights", command=self._load_all_flights).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Details", command=self._view_details).pack(side=tk.LEFT, padx=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_container, text="Flight Results", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview columns
        cols = ('Flight', 'Airline', 'Origin', 'Destination', 'Departure', 'Arrival', 'Status', 'Gate')
        self.flights_tree = ttk.Treeview(results_frame, columns=cols, show='headings', height=15)
        
        # Configure columns
        column_widths = {
            'Flight': 80,
            'Airline': 120,
            'Origin': 60,
            'Destination': 60,
            'Departure': 120,
            'Arrival': 120,
            'Status': 90,
            'Gate': 60
        }
        
        for col in cols:
            self.flights_tree.heading(col, text=col)
            self.flights_tree.column(col, width=column_widths.get(col, 100))
        
        # Configure status column colors
        self.flights_tree.column('Status', width=90)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.flights_tree.yview)
        self.flights_tree.configure(yscroll=scrollbar.set)
        
        self.flights_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click
        self.flights_tree.bind('<Double-1>', lambda e: self._view_details())
        
        # Status Summary Section
        summary_frame = ttk.LabelFrame(main_container, text="Status Summary", padding=10)
        summary_frame.pack(fill=tk.X, pady=5)
        
        self.status_labels = {}
        for i, status in enumerate(config.FLIGHT_STATUS):
            lbl = ttk.Label(summary_frame, text=f"{status}: 0", font=('Segoe UI', 9))
            lbl.pack(side=tk.LEFT, padx=10)
            self.status_labels[status] = lbl
        
        # Load data
        self._load_airports()
        self._load_all_flights()
    
    def _load_airports(self):
        """Load airports into filter comboboxes"""
        airports = Airport.get_all()
        airport_options = ['All Airports']
        
        for a in airports:
            airport_options.append(f"{a['code']} - {a['city']}")
        
        self.origin_combo['values'] = airport_options
        self.origin_combo.set('All Airports')
        
        self.dest_combo['values'] = airport_options
        self.dest_combo.set('All Airports')
        
        # Store airport mappings
        self.airports_map = {f"{a['code']} - {a['city']}": a['id'] for a in airports}
    
    def _load_all_flights(self):
        """Load all flights"""
        flights = Flight.get_all(limit=200)
        self._display_flights(flights)
        self._update_status_summary(flights)
    
    def _search_flights(self):
        """Search flights based on filters"""
        origin_val = self.origin_combo.get()
        dest_val = self.dest_combo.get()
        flight_num = self.flight_search.get().strip()
        status_val = self.status_filter.get()
        
        # Get all flights
        flights = Flight.get_all(limit=200)
        
        # Filter by origin
        if origin_val != 'All Airports':
            origin_id = self.airports_map.get(origin_val)
            if origin_id:
                flights = [f for f in flights if f.get('origin_airport_id') == origin_id]
        
        # Filter by destination
        if dest_val != 'All Airports':
            dest_id = self.airports_map.get(dest_val)
            if dest_id:
                flights = [f for f in flights if f.get('destination_airport_id') == dest_id]
        
        # Filter by flight number
        if flight_num:
            flights = [f for f in flights if flight_num.upper() in f.get('flight_number', '').upper()]
        
        # Filter by status
        if status_val != 'All':
            flights = [f for f in flights if f.get('status') == status_val]
        
        self._display_flights(flights)
        self._update_status_summary(flights)
    
    def _display_flights(self, flights):
        """Display flights in treeview"""
        self.flights_tree.delete(*self.flights_tree.get_children())
        
        for f in flights:
            dep_time = self._format_datetime(f.get('departure_time'))
            arr_time = self._format_datetime(f.get('arrival_time'))
            
            item_id = self.flights_tree.insert('', tk.END, iid=f['id'], values=(
                f.get('flight_number', ''),
                f.get('airline', ''),
                f.get('origin_code', ''),
                f.get('dest_code', ''),
                dep_time,
                arr_time,
                f.get('status', ''),
                f.get('gate_number', 'N/A')
            ))
            
            # Color code based on status
            status = f.get('status', '')
            color = AppStyles.get_status_color(status)
            self.flights_tree.item(item_id, tags=(status,))
        
        # Configure tag colors
        self.flights_tree.tag_configure('On Time', foreground='#27AE60')
        self.flights_tree.tag_configure('Delayed', foreground='#F39C12')
        self.flights_tree.tag_configure('Cancelled', foreground='#E74C3C')
        self.flights_tree.tag_configure('Boarding', foreground='#3498DB')
        self.flights_tree.tag_configure('Departed', foreground='#9B59B6')
        self.flights_tree.tag_configure('Landed', foreground='#1ABC9C')
    
    def _update_status_summary(self, flights):
        """Update status summary labels"""
        status_counts = {s: 0 for s in config.FLIGHT_STATUS}
        
        for f in flights:
            status = f.get('status')
            if status in status_counts:
                status_counts[status] += 1
        
        for status, count in status_counts.items():
            self.status_labels[status].config(text=f"{status}: {count}")
    
    def _format_datetime(self, dt):
        """Format datetime for display"""
        if dt is None:
            return 'N/A'
        
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except:
                return dt[:16] if len(dt) > 16 else dt
        
        try:
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return str(dt)[:16]
    
    def _view_details(self):
        """View flight details"""
        selected = self.flights_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a flight to view details")
            return
        
        flight_id = selected[0]
        flight_data = Flight.get_by_id(flight_id)
        
        if flight_data:
            dialog = FlightDetailsDialog(self.parent, flight_data)
    
    def get_frame(self):
        """Get the main frame"""
        return self.frame

