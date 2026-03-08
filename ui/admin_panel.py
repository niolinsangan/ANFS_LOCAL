"""
Admin Panel for ANFS Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.flight import Flight
from models.airport import Airport
from models.passenger import Passenger
from models.gate import Gate
from models.runway import Runway
from ui.dialogs import FlightDialog, PassengerDialog, FlightDetailsDialog, AirportDialog, GateDialog
from ui.styles import AppStyles
import config


class AdminPanel:
    """Admin panel with CRUD operations"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_flights_tab()
        self._create_airports_tab()
        self._create_gates_tab()
        self._create_passengers_tab()
        
        # Buttons frame at bottom
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_all).pack(side=tk.LEFT, padx=5)
    
    def _create_flights_tab(self):
        """Create flights management tab"""
        flights_tab = ttk.Frame(self.notebook)
        self.notebook.add(flights_tab, text="Flights")
        
        # Toolbar
        toolbar = ttk.Frame(flights_tab)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add Flight", command=self._add_flight).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Flight", command=self._edit_flight).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Flight", command=self._delete_flight).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="View Details", command=self._view_flight_details).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="  Status:").pack(side=tk.LEFT, padx=5)
        self.flight_status_filter = ttk.Combobox(toolbar, values=['All'] + config.FLIGHT_STATUS, width=12)
        self.flight_status_filter.pack(side=tk.LEFT)
        self.flight_status_filter.set('All')
        self.flight_status_filter.bind('<<ComboboxSelected>>', lambda e: self._filter_flights())
        
        ttk.Button(toolbar, text="Filter", command=self._filter_flights).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        cols = ('Flight', 'Airline', 'Origin', 'Destination', 'Departure', 'Arrival', 'Status', 'Gate')
        self.flights_tree = ttk.Treeview(flights_tab, columns=cols, show='headings')
        
        for col in cols:
            self.flights_tree.heading(col, text=col)
            self.flights_tree.column(col, width=100)
        
        self.flights_tree.column('Flight', width=80)
        self.flights_tree.column('Status', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(flights_tab, orient=tk.VERTICAL, command=self.flights_tree.yview)
        self.flights_tree.configure(yscroll=scrollbar.set)
        
        self.flights_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self._load_flights()
    
    def _create_airports_tab(self):
        """Create airports management tab"""
        airports_tab = ttk.Frame(self.notebook)
        self.notebook.add(airports_tab, text="Airports")
        
        toolbar = ttk.Frame(airports_tab)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add Airport", command=self._add_airport).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Airport", command=self._edit_airport).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Airport", command=self._delete_airport).pack(side=tk.LEFT, padx=2)
        
        cols = ('Code', 'Name', 'City', 'Country')
        self.airports_tree = ttk.Treeview(airports_tab, columns=cols, show='headings')
        
        for col in cols:
            self.airports_tree.heading(col, text=col)
            self.airports_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(airports_tab, orient=tk.VERTICAL, command=self.airports_tree.yview)
        self.airports_tree.configure(yscroll=scrollbar.set)
        
        self.airports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self._load_airports()
    
    def _create_gates_tab(self):
        """Create gates management tab"""
        gates_tab = ttk.Frame(self.notebook)
        self.notebook.add(gates_tab, text="Gates & Runways")
        
        toolbar = ttk.Frame(gates_tab)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add Gate", command=self._add_gate).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Gate", command=self._delete_gate).pack(side=tk.LEFT, padx=2)
        
        # Gates section
        ttk.Label(gates_tab, text="Gates:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, padx=5)
        
        cols = ('Gate', 'Airport', 'Terminal', 'Status')
        self.gates_tree = ttk.Treeview(gates_tab, columns=cols, show='headings', height=8)
        
        for col in cols:
            self.gates_tree.heading(col, text=col)
            self.gates_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(gates_tab, orient=tk.VERTICAL, command=self.gates_tree.yview)
        self.gates_tree.configure(yscroll=scrollbar.set)
        
        self.gates_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self._load_gates()
    
    def _create_passengers_tab(self):
        """Create passengers management tab"""
        passengers_tab = ttk.Frame(self.notebook)
        self.notebook.add(passengers_tab, text="Passengers")
        
        toolbar = ttk.Frame(passengers_tab)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Add Passenger", command=self._add_passenger).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Edit Passenger", command=self._edit_passenger).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Delete Passenger", command=self._delete_passenger).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Refresh", command=self._load_passengers).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="  Flight:").pack(side=tk.LEFT, padx=5)
        self.passenger_flight_filter = ttk.Combobox(toolbar, width=15)
        self.passenger_flight_filter.pack(side=tk.LEFT)
        self.passenger_flight_filter.bind('<<ComboboxSelected>>', lambda e: self._filter_passengers())
        
        cols = ('Name', 'Passport', 'Flight', 'Seat', 'Booking Ref')
        self.passengers_tree = ttk.Treeview(passengers_tab, columns=cols, show='headings')
        
        for col in cols:
            self.passengers_tree.heading(col, text=col)
            self.passengers_tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(passengers_tab, orient=tk.VERTICAL, command=self.passengers_tree.yview)
        self.passengers_tree.configure(yscroll=scrollbar.set)
        
        self.passengers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self._load_passengers()
    
    def _load_flights(self):
        """Load flights into treeview"""
        self.flights_tree.delete(*self.flights_tree.get_children())
        
        flights = Flight.get_all()
        
        # Load flights for filter
        self.flights_map = {}
        for f in flights:
            key = f"{f['flight_number']} - {f['origin_code']}→{f['dest_code']}"
            self.flights_map[key] = f['id']
        
        for f in flights:
            dep_time = str(f.get('departure_time', ''))[:16] if f.get('departure_time') else 'N/A'
            arr_time = str(f.get('arrival_time', ''))[:16] if f.get('arrival_time') else 'N/A'
            
            self.flights_tree.insert('', tk.END, iid=f['id'], values=(
                f.get('flight_number', ''),
                f.get('airline', ''),
                f.get('origin_code', ''),
                f.get('dest_code', ''),
                dep_time,
                arr_time,
                f.get('status', ''),
                f.get('gate_number', 'N/A')
            ))
        
        # Update flight filter combobox
        flight_options = ['All'] + [f"{f['flight_number']}" for f in flights]
        if hasattr(self, 'passenger_flight_filter'):
            self.passenger_flight_filter['values'] = flight_options
    
    def _load_airports(self):
        """Load airports into treeview"""
        self.airports_tree.delete(*self.airports_tree.get_children())
        
        airports = Airport.get_all()
        self.airports_map = {a['id']: a for a in airports}
        
        for a in airports:
            self.airports_tree.insert('', tk.END, iid=a['id'], values=(
                a.get('code', ''),
                a.get('name', ''),
                a.get('city', ''),
                a.get('country', '')
            ))
    
    def _load_gates(self):
        """Load gates into treeview"""
        self.gates_tree.delete(*self.gates_tree.get_children())
        
        gates = Gate.get_all()
        
        for g in gates:
            status = 'Operational' if g.get('is_operational') else 'Closed'
            self.gates_tree.insert('', tk.END, iid=g['id'], values=(
                g.get('gate_number', ''),
                g.get('airport_code', ''),
                g.get('terminal', ''),
                status
            ))
    
    def _load_passengers(self):
        """Load passengers into treeview"""
        self.passengers_tree.delete(*self.passengers_tree.get_children())
        
        passengers = Passenger.get_all()
        
        for p in passengers:
            self.passengers_tree.insert('', tk.END, iid=p['id'], values=(
                f"{p.get('first_name', '')} {p.get('last_name', '')}",
                p.get('passport_number', ''),
                p.get('flight_number', ''),
                p.get('seat_number', 'N/A'),
                p.get('booking_reference', '')
            ))
    
    def _filter_flights(self):
        """Filter flights by status"""
        status = self.flight_status_filter.get()
        
        self.flights_tree.delete(*self.flights_tree.get_children())
        
        flights = Flight.get_all()
        
        for f in flights:
            if status == 'All' or f.get('status') == status:
                dep_time = str(f.get('departure_time', ''))[:16] if f.get('departure_time') else 'N/A'
                arr_time = str(f.get('arrival_time', ''))[:16] if f.get('arrival_time') else 'N/A'
                
                self.flights_tree.insert('', tk.END, iid=f['id'], values=(
                    f.get('flight_number', ''),
                    f.get('airline', ''),
                    f.get('origin_code', ''),
                    f.get('dest_code', ''),
                    dep_time,
                    arr_time,
                    f.get('status', ''),
                    f.get('gate_number', 'N/A')
                ))
    
    def _filter_passengers(self):
        """Filter passengers by flight"""
        flight_num = self.passenger_flight_filter.get()
        
        self.passengers_tree.delete(*self.passengers_tree.get_children())
        
        if flight_num == 'All':
            self._load_passengers()
            return
        
        passengers = Passenger.get_all()
        
        for p in passengers:
            if p.get('flight_number') == flight_num:
                self.passengers_tree.insert('', tk.END, iid=p['id'], values=(
                    f"{p.get('first_name', '')} {p.get('last_name', '')}",
                    p.get('passport_number', ''),
                    p.get('flight_number', ''),
                    p.get('seat_number', 'N/A'),
                    p.get('booking_reference', '')
                ))
    
    def _add_flight(self):
        """Add new flight"""
        dialog = FlightDialog(self.parent)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.result:
            flight = Flight(**dialog.result)
            if flight.save():
                messagebox.showinfo("Success", "Flight added successfully!")
                self._load_flights()
            else:
                messagebox.showerror("Error", "Failed to add flight")
    
    def _edit_flight(self):
        """Edit selected flight"""
        selected = self.flights_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a flight to edit")
            return
        
        flight_id = selected[0]
        flight_data = Flight.get_by_id(flight_id)
        
        if flight_data:
            dialog = FlightDialog(self.parent, flight_data)
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                flight = Flight(id=flight_id, **dialog.result)
                if flight.update():
                    messagebox.showinfo("Success", "Flight updated successfully!")
                    self._load_flights()
                else:
                    messagebox.showerror("Error", "Failed to update flight")
    
    def _delete_flight(self):
        """Delete selected flight"""
        selected = self.flights_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a flight to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this flight?"):
            flight_id = selected[0]
            if Flight.delete(flight_id):
                messagebox.showinfo("Success", "Flight deleted successfully!")
                self._load_flights()
            else:
                messagebox.showerror("Error", "Failed to delete flight")
    
    def _view_flight_details(self):
        """View flight details with passengers"""
        selected = self.flights_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a flight to view")
            return
        
        flight_id = selected[0]
        flight_data = Flight.get_by_id(flight_id)
        
        if flight_data:
            dialog = FlightDetailsDialog(self.parent, flight_data)
    
    def _add_airport(self):
        """Add new airport"""
        dialog = AirportDialog(self.parent)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.result:
            airport = Airport(**dialog.result)
            if airport.save():
                messagebox.showinfo("Success", "Airport added successfully!")
                self._load_airports()
            else:
                messagebox.showerror("Error", "Failed to add airport")
    
    def _edit_airport(self):
        """Edit selected airport"""
        selected = self.airports_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an airport to edit")
            return
        
        airport_id = selected[0]
        airport_data = self.airports_map.get(airport_id)
        
        if airport_data:
            dialog = AirportDialog(self.parent, airport_data)
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                airport = Airport(id=airport_id, **dialog.result)
                if airport.update():
                    messagebox.showinfo("Success", "Airport updated successfully!")
                    self._load_airports()
                else:
                    messagebox.showerror("Error", "Failed to update airport")
    
    def _delete_airport(self):
        """Delete selected airport"""
        selected = self.airports_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an airport to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this airport?"):
            airport_id = selected[0]
            if Airport.delete(airport_id):
                messagebox.showinfo("Success", "Airport deleted successfully!")
                self._load_airports()
            else:
                messagebox.showerror("Error", "Failed to delete airport (may have flights)")
    
    def _add_gate(self):
        """Add new gate"""
        dialog = GateDialog(self.parent)
        self.parent.wait_window(dialog.dialog)
        
        if dialog.result:
            gate = Gate(**dialog.result)
            if gate.save():
                messagebox.showinfo("Success", "Gate added successfully!")
                self._load_gates()
            else:
                messagebox.showerror("Error", "Failed to add gate")
    
    def _delete_gate(self):
        """Delete selected gate"""
        selected = self.gates_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a gate to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this gate?"):
            gate_id = selected[0]
            if Gate.delete(gate_id):
                messagebox.showinfo("Success", "Gate deleted successfully!")
                self._load_gates()
            else:
                messagebox.showerror("Error", "Failed to delete gate")
    
    def _add_passenger(self):
        """Add new passenger"""
        # First select a flight
        flights = Flight.get_all()
        if not flights:
            messagebox.showwarning("Warning", "No flights available")
            return
        
        # Create a simple dialog to select flight
        flight_dialog = tk.Toplevel(self.parent)
        flight_dialog.title("Select Flight")
        flight_dialog.geometry("300x150")
        flight_dialog.transient(self.parent)
        
        ttk.Label(flight_dialog, text="Select Flight:").pack(pady=10)
        flight_combo = ttk.Combobox(flight_dialog, values=[f['flight_number'] for f in flights], width=20)
        flight_combo.pack(pady=5)
        
        selected_flight_id = [None]
        
        def on_select():
            for f in flights:
                if f['flight_number'] == flight_combo.get():
                    selected_flight_id[0] = f['id']
                    break
            flight_dialog.destroy()
        
        ttk.Button(flight_dialog, text="Select", command=on_select).pack(pady=10)
        
        self.parent.wait_window(flight_dialog)
        
        if selected_flight_id[0]:
            dialog = PassengerDialog(self.parent, selected_flight_id[0])
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                passenger = Passenger(**dialog.result)
                if passenger.save():
                    messagebox.showinfo("Success", "Passenger added successfully!")
                    self._load_passengers()
                else:
                    messagebox.showerror("Error", "Failed to add passenger")
    
    def _edit_passenger(self):
        """Edit selected passenger"""
        selected = self.passengers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a passenger to edit")
            return
        
        passenger_id = selected[0]
        passenger_data = Passenger.get_by_id(passenger_id)
        
        if passenger_data:
            dialog = PassengerDialog(self.parent, passenger_data['flight_id'], passenger_data)
            self.parent.wait_window(dialog.dialog)
            
            if dialog.result:
                passenger = Passenger(id=passenger_id, **dialog.result)
                if passenger.update():
                    messagebox.showinfo("Success", "Passenger updated successfully!")
                    self._load_passengers()
                else:
                    messagebox.showerror("Error", "Failed to update passenger")
    
    def _delete_passenger(self):
        """Delete selected passenger"""
        selected = self.passengers_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a passenger to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this passenger?"):
            passenger_id = selected[0]
            if Passenger.delete(passenger_id):
                messagebox.showinfo("Success", "Passenger deleted successfully!")
                self._load_passengers()
            else:
                messagebox.showerror("Error", "Failed to delete passenger")
    
    def refresh_all(self):
        """Refresh all data"""
        self._load_flights()
        self._load_airports()
        self._load_gates()
        self._load_passengers()
        messagebox.showinfo("Refresh", "Data refreshed successfully!")
    
    def get_frame(self):
        """Get the main frame"""
        return self.frame

