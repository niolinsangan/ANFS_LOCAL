"""
Airport Network Flight Scheduler (ANFS)
Main Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import run

if __name__ == '__main__':
    print("=" * 50)
    print("Airport Network Flight Scheduler (ANFS)")
    print("=" * 50)
    print("\nStarting application...")
    print("\nTo initialize the database with sample data, run:")
    print("    python database/seed_data.py")
    print("\n" + "=" * 50 + "\n")
    
    run()

