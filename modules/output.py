#!/usr/bin/env python3
"""
main.py

Main entry point for the DarkForge toolkit. Provides a command-line interface for
password generation, analysis, and attack simulation.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import os
import sys
import json
import click
import logging
from pathlib import Path

# Ensure we're using the correct path resolution
# Get the directory containing this script
BASE_DIR = Path(__file__).resolve().parent

# Add the base directory to sys.path to ensure modules can be found
sys.path.insert(0, str(BASE_DIR))

# Then use relative imports within the package
from modules.data_input.collector import UserProfile, get_user_profile
from modules.pattern_generator import generate_passwords
from modules.password_analyzer import cli as analyzer_cli
from modules.attack_simulator import cli as attack_cli
from modules.art import get_logo, get_section_art
from modules.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Initialize colorama for colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    USE_COLOR = True
except ImportError:
    USE_COLOR = False
    logger.warning("Colorama not found. Running without color support.")

def print_logo():
    """Print the DarkForge logo with color if available."""
    logo = get_logo()
    if USE_COLOR:
        print(Fore.RED + logo)
    else:
        print(logo)

@click.group()
def cli():
    """DarkForge - Password Analysis and Generation Toolkit"""
    # Print logo at the start of each command
    print_logo()
    pass

@cli.command()
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def debug(verbose):
    """Run diagnostic checks on the DarkForge installation."""
    print("Running DarkForge diagnostics...")
    
    # Check file paths
    print(f"Base directory: {BASE_DIR}")
    
    # Check module imports
    modules_to_check = [
        ("data_input.collector", ["UserProfile", "get_user_profile"]),
        ("pattern_generator", ["generate_passwords"]),
        ("password_analyzer", ["cli"]),
        ("attack_simulator", ["cli"]),
        ("database", ["Database"]),
        ("art", ["get_logo", "get_section_art"])
    ]
    
    for module_name, expected_attrs in modules_to_check:
        try:
            module_path = f"modules.{module_name}"
            __import__(module_path)
            module = sys.modules[module_path]
            
            print(f"✓ Module {module_name} imported successfully")
            
            for attr in expected_attrs:
                if hasattr(module, attr):
                    print(f"  ✓ Found {attr} in {module_name}")
                else:
                    print(f"  ✗ Missing {attr} in {module_name}")
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {e}")
    
    # Check database connection
    try:
        db = Database()
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
    
    # Check filesystem access
    dirs_to_check = ["data", "config", "modules"]
    for dir_name in dirs_to_check:
        dir_path = BASE_DIR / dir_name
        if dir_path.exists():
            print(f"✓ Directory {dir_name} exists")
        else:
            print(f"✗ Directory {dir_name} missing")
            
    print("\nDiagnostics complete.")

def get_file_path(relative_path):
    """Convert relative path to absolute path based on module location."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / relative_path

# Define file_path before using it
file_path = get_file_path("config/settings.json")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.read()
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    print(f"Error: Could not find file {file_path}.")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Absolute path attempted: {Path(file_path).absolute()}")
    sys.exit(1)
except PermissionError:
    logger.error(f"Permission denied: {file_path}")
    print(f"Error: No permission to read {file_path}.")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error reading file {file_path}: {e}")
    print(f"Error: Could not read file {file_path}: {e}")
    sys.exit(1)

# ... rest of your command definitions ...
