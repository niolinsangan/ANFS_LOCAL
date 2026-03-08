"""
Helper utilities for ANFS Application
"""
from datetime import datetime, timedelta


def format_datetime(dt, format_str='%Y-%m-%d %H:%M'):
    """Format datetime object to string"""
    if dt is None:
        return 'N/A'
    
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt[:16] if len(dt) > 16 else dt
    
    try:
        return dt.strftime(format_str)
    except:
        return str(dt)[:16]


def parse_datetime(datetime_str):
    """Parse datetime string to datetime object"""
    if not datetime_str:
        return None
    
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d',
        '%d/%m/%Y %H:%M',
        '%d/%m/%Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    
    return None


def calculate_duration(departure, arrival):
    """Calculate flight duration"""
    if not departure or not arrival:
        return 'N/A'
    
    dep = parse_datetime(departure) if isinstance(departure, str) else departure
    arr = parse_datetime(arrival) if isinstance(arrival, str) else arrival
    
    if dep and arr:
        duration = arr - dep
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    
    return 'N/A'


def validate_flight_number(flight_number):
    """Validate flight number format"""
    if not flight_number:
        return False
    
    # Basic validation: uppercase letters and numbers
    return flight_number.replace(' ', '').isalnum()


def generate_booking_reference():
    """Generate random booking reference"""
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def validate_passport(passport_number):
    """Validate passport number format"""
    if not passport_number:
        return False
    
    # Basic validation: alphanumeric
    return passport_number.replace(' ', '').isalnum()

