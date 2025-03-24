#!/usr/bin/env python3
"""Test script to verify imports work properly."""

try:
    print("Importing UserProfile...")
    from modules.data_input.collector import UserProfile
    print("UserProfile imported successfully!")
    
    print("Importing generate_passwords...")
    from modules.pattern_generator import generate_passwords
    print("generate_passwords imported successfully!")
    
    print("All imports successful!")
except Exception as e:
    print(f"Error importing: {e}")
    import traceback
    traceback.print_exc() 