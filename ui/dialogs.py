"""
Dialog Windows for ANFS Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import config
from models.airport import Airport
from models.flight import Flight
from models.gate import Gate
from models.runway import Runway
from models.passenger import Passenger


class FlightDialog:
    """Dialog for adding/editing flights"""
    
    def __init__(self, parent, flight=None):
        self.result = None
        self.flight = flight
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Flight" if not flight else "Edit Flight")
        self.dialog.geometry("600x550")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self._create_widgets()
        self._load_data()
        
        if flight:
            self._populate_fields()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Flight Number
        ttk.Label(main_frame, text="Flight Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.flight_number = ttk.Entry(main_frame, width=15)
        self.flight_number.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Airline
        ttk.Label(main_frame, text="Airline:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.airline = ttk.Combobox(main_frame, values=config.AIRLINES, width=25)
        self.airline.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Origin Airport
        ttk.Label(main_frame, text="Origin:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.origin = ttk.Combobox(main_frame, width=25)
        self.origin.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Destination Airport
        ttk.Label(main_frame, text="Destination:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.destination = ttk.Combobox(main_frame, width=25)
        self.destination.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Departure Time
        ttk.Label(main_frame, text="Departure:").grid(row=4, column=0, sticky=tk.W, pady=5)
        dep_frame = ttk.Frame(main_frame)
        dep_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.dep_date = ttk.Entry(dep_frame, width=12)
        self.dep_date.pack(side=tk.LEFT, padx=2)
        self.dep_time = ttk.Entry(dep_frame, width=8)
        self.dep_time.pack(side=tk.LEFT, padx=2)
        ttk.Label(dep_frame, text="(YYYY-MM-DD HH:MM)").pack(side=tk.LEFT, font=('Segoe UI', 8))
        
        # Arrival Time
        ttk.Label(main_frame, text="Arrival:").grid(row=5, column=0, sticky=tk.W, pady=5)
        arr_frame = ttk.Frame(main_frame)
        arr_frame.grid(row=5, column=1, sticky=tk.W, pady=5)
        self.arr_date = ttk.Entry(arr_frame, width=12)
        self.arr_date.pack(side=tk.LEFT, padx=2)
        self.arr_time = ttk.Entry(arr_frame, width=8)
        self.arr_time.pack(side=tk.LEFT, padx=2)
        ttk.Label(arr_frame, text="(YYYY-MM-DD HH:MM)").pack(side=tk.LEFT, font=('Segoe UI', 8))
        
        # Status
        ttk.Label(main_frame, text="Status:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.status = ttk.Combobox(main_frame, values=config.FLIGHT_STATUS, width=15)
        self.status.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Gate
        ttk.Label(main_frame, text="Gate:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.gate = ttk.Combobox(main_frame, width=15)
        self.gate.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Runway
        ttk.Label(main_frame, text="Runway:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.runway = ttk.Combobox(main_frame, width=15)
        self.runway.grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Aircraft Type
        ttk.Label(main_frame, text="Aircraft:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.aircraft = ttk.Combobox(main_frame, values=config.AIRCRAFT_TYPES, width=20)
        self.aircraft.grid(row=9, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _load_data(self):
        """Load data into comboboxes"""
        airports = Airport.get_all()
        self.airports_map = {f"{a['code']} - {a['name']}": a['id'] for a in airports}
        self.origin['values'] = list(self.airports_map.keys())
        self.destination['values'] = list(self.airports_map.keys())
        
        self.gates_map = {}
        for g in Gate.get_all():
            key = f"{g['gate_number']} ({g['airport_code']})"
            self.gates_map[key] = g['id']
        self.gate['values'] = list(self.gates_map.keys())
        
        self.runways_map = {}
        for r in Runway.get_all():
            key = f"{r['runway_name']} ({r['airport_code']})"
            self.runways_map[key] = r['id']
        self.runway['values'] = list(self.runways_map.keys())
        
        self.status['values'] = config.FLIGHT_STATUS
    
    def _populate_fields(self):
        """Populate fields with existing flight data"""
        f = self.flight
        self.flight_number.insert(0, f.get('flight_number', ''))
        self.airline.set(f.get('airline', ''))
        self.status.set(f.get('status', 'On Time'))
        self.aircraft.set(f.get('aircraft_type', ''))
        
        # Set origin/destination
        for key, val in self.airports_map.items():
            if val == f.get('origin_airport_id'):
                self.origin.set(key)
            if val == f.get('destination_airport_id'):
                self.destination.set(key)
        
        # Set times
        if f.get('departure_time'):
            dep = f['departure_time']
            self.dep_date.insert(0, dep.strftime('%Y-%m-%d') if hasattr(dep, 'strftime') else str(dep)[:10])
            self.dep_time.insert(0, dep.strftime('%H:%M') if hasattr(dep, 'strftime') else str(dep)[11:16])
        
        if f.get('arrival_time'):
            arr = f['arrival_time']
            self.arr_date.insert(0, arr.strftime('%Y-%m-%d') if hasattr(arr, 'strftime') else str(arr)[:10])
            self.arr_time.insert(0, arr.strftime('%H:%M') if hasattr(arr, 'strftime') else str(arr)[11:16])
        
        # Set gate/runway
        for key, val in self.gates_map.items():
            if val == f.get('gate_id'):
                self.gate.set(key)
        
        for key, val in self.runways_map.items():
            if val == f.get('runway_id'):
                self.runway.set(key)
    
    def _save(self):
        """Save the flight"""
        try:
            dep_datetime = f"{self.dep_date.get()} {self.dep_time.get()}"
            arr_datetime = f"{self.arr_date.get()} {self.arr_time.get()}"
            
            data = {
                'flight_number': self.flight_number.get(),
                'airline': self.airline.get(),
                'origin_airport_id': self.airports_map.get(self.origin.get()),
                'destination_airport_id': self.airports_map.get(self.destination.get()),
                'departure_time': dep_datetime,
                'arrival_time': arr_datetime,
                'status': self.status.get(),
                'gate_id': self.gates_map.get(self.gate.get()),
                'runway_id': self.runways_map.get(self.runway.get()),
                'aircraft_type': self.aircraft.get()
            }
            
            if not all([data['flight_number'], data['airline'], data['origin_airport_id'],
                       data['destination_airport_id'], data['departure_time'], data['arrival_time']]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            self.result = data
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save flight: {str(e)}")


class PassengerDialog:
    """Dialog for adding/editing passengers"""
    
    def __init__(self, parent, flight_id, passenger=None):
        self.result = None
        self.passenger = passenger
        self.flight_id = flight_id
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Passenger" if not passenger else "Edit Passenger")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
        if passenger:
            self._populate_fields()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # First Name
        ttk.Label(main_frame, text="First Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.first_name = ttk.Entry(main_frame, width=25)
        self.first_name.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Last Name
        ttk.Label(main_frame, text="Last Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.last_name = ttk.Entry(main_frame, width=25)
        self.last_name.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Passport Number
        ttk.Label(main_frame, text="Passport Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.passport = ttk.Entry(main_frame, width=25)
        self.passport.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Seat Number
        ttk.Label(main_frame, text="Seat Number:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.seat = ttk.Entry(main_frame, width=10)
        self.seat.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Booking Reference
        ttk.Label(main_frame, text="Booking Ref:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.booking = ttk.Entry(main_frame, width=15)
        self.booking.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _populate_fields(self):
        """Populate fields with existing data"""
        p = self.passenger
        self.first_name.insert(0, p.get('first_name', ''))
        self.last_name.insert(0, p.get('last_name', ''))
        self.passport.insert(0, p.get('passport_number', ''))
        self.seat.insert(0, p.get('seat_number', ''))
        self.booking.insert(0, p.get('booking_reference', ''))
    
    def _save(self):
        """Save the passenger"""
        try:
            data = {
                'first_name': self.first_name.get(),
                'last_name': self.last_name.get(),
                'passport_number': self.passport.get(),
                'flight_id': self.flight_id,
                'seat_number': self.seat.get(),
                'booking_reference': self.booking.get()
            }
            
            if not all([data['first_name'], data['last_name'], data['passport_number'],
                       data['booking_reference']]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            self.result = data
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save passenger: {str(e)}")


class LoginDialog:
    """Admin login dialog"""
    
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Admin Login")
        self.dialog.geometry("300x180")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create login widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(main_frame, width=20)
        self.username.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password = ttk.Entry(main_frame, width=20, show="*")
        self.password.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Login", command=self._login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _login(self):
        """Authenticate user"""
        username = self.username.get()
        password = self.password.get()
        
        if username == config.ADMIN_CREDENTIALS['username'] and password == config.ADMIN_CREDENTIALS['password']:
            self.result = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


class FlightDetailsDialog:
    """Dialog to show flight details and passengers"""
    
    def __init__(self, parent, flight_data):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Flight Details - {flight_data.get('flight_number', 'N/A')}")
        self.dialog.geometry("800x500")
        self.dialog.transient(parent)
        
        self.flight_data = flight_data
        self._create_widgets()
    
    def _create_widgets(self):
        """Create detail view"""
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Flight Info Section
        info_frame = ttk.LabelFrame(main_frame, text="Flight Information", padding=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        f = self.flight_data
        
        info_text = f"""
Flight Number: {f.get('flight_number', 'N/A')}
Airline: {f.get('airline', 'N/A')}
Route: {f.get('origin_code', 'N/A')} ({f.get('origin_city', '')}) → {f.get('dest_code', 'N/A')} ({f.get('dest_city', '')})
Departure: {f.get('departure_time', 'N/A')}
Arrival: {f.get('arrival_time', 'N/A')}
Status: {f.get('status', 'N/A')}
Gate: {f.get('gate_number', 'Not Assigned')}
Runway: {f.get('runway_name', 'Not Assigned')}
Aircraft: {f.get('aircraft_type', 'N/A')}
        """
        
        ttk.Label(info_frame, text=info_text.strip(), font=('Segoe UI', 10), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Passengers Section
        passenger_frame = ttk.LabelFrame(main_frame, text="Passengers", padding=10)
        passenger_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview for passengers
        cols = ('Name', 'Passport', 'Seat', 'Booking Ref')
        self.passenger_tree = ttk.Treeview(passenger_frame, columns=cols, show='headings', height=10)
        
        for col in cols:
            self.passenger_tree.heading(col, text=col)
            self.passenger_tree.column(col, width=150)
        
        self.passenger_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(passenger_frame, orient=tk.VERTICAL, command=self.passenger_tree.yview)
        self.passenger_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load passengers
        self._load_passengers()
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack(pady=10)
    
    def _load_passengers(self):
        """Load passengers for this flight"""
        passengers = Passenger.get_by_flight(self.flight_data['id'])
        
        for p in passengers:
            self.passenger_tree.insert('', tk.END, values=(
                f"{p['first_name']} {p['last_name']}",
                p['passport_number'],
                p['seat_number'] or 'N/A',
                p['booking_reference']
            ))


class AirportDialog:
    """Dialog for adding/editing airports"""
    
    def __init__(self, parent, airport=None):
        self.result = None
        self.airport = airport
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Airport" if not airport else "Edit Airport")
        self.dialog.geometry("350x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        
        if airport:
            self._populate_fields()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="IATA Code:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.code = ttk.Entry(main_frame, width=10)
        self.code.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Airport Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name = ttk.Entry(main_frame, width=25)
        self.name.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="City:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.city = ttk.Entry(main_frame, width=20)
        self.city.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Country:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.country = ttk.Entry(main_frame, width=20)
        self.country.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _populate_fields(self):
        """Populate fields"""
        a = self.airport
        self.code.insert(0, a.get('code', ''))
        self.name.insert(0, a.get('name', ''))
        self.city.insert(0, a.get('city', ''))
        self.country.insert(0, a.get('country', ''))
    
    def _save(self):
        """Save airport"""
        try:
            data = {
                'code': self.code.get().upper(),
                'name': self.name.get(),
                'city': self.city.get(),
                'country': self.country.get()
            }
            
            if not all([data['code'], data['name'], data['city'], data['country']]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if len(data['code']) != 3:
                messagebox.showerror("Error", "IATA code must be 3 characters")
                return
            
            self.result = data
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")


class GateDialog:
    """Dialog for adding/editing gates"""
    
    def __init__(self, parent, gate=None):
        self.result = None
        self.gate = gate
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Gate" if not gate else "Edit Gate")
        self.dialog.geometry("350x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._load_airports()
        
        if gate:
            self._populate_fields()
    
    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Gate Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.gate_number = ttk.Entry(main_frame, width=10)
        self.gate_number.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Airport:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.airport = ttk.Combobox(main_frame, width=20)
        self.airport.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Terminal:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.terminal = ttk.Combobox(main_frame, values=['T1', 'T2', 'T3', 'T4'], width=10)
        self.terminal.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.terminal.set('T1')
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def _load_airports(self):
        airports = Airport.get_all()
        self.airports_map = {f"{a['code']} - {a['name']}": a['id'] for a in airports}
        self.airport['values'] = list(self.airports_map.keys())
    
    def _populate_fields(self):
        g = self.gate
        self.gate_number.insert(0, g.get('gate_number', ''))
        self.terminal.set(g.get('terminal', 'T1'))
        
        for key, val in self.airports_map.items():
            if val == g.get('airport_id'):
                self.airport.set(key)
                break
    
    def _save(self):
        try:
            data = {
                'gate_number': self.gate_number.get().upper(),
                'airport_id': self.airports_map.get(self.airport.get()),
                'terminal': self.terminal.get()
            }
            
            if not all([data['gate_number'], data['airport_id']]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            self.result = data
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

