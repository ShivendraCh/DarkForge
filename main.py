#!/usr/bin/env python3
"""
main.py

Main entry point for the DarkForge toolkit with an interactive menu.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import os
import sys
import json
import click
import logging
from pathlib import Path
from colorama import init, Fore, Style
from modules.data_input.collector import UserProfile, get_user_profile
from modules.pattern_generator import generate_passwords
from modules.password_analyzer import cli as analyzer_cli
from modules.attack_simulator import cli as attack_cli
from modules.art import get_logo, get_section_art
from modules.database import Database

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Get absolute path to the script directory
BASE_DIR = Path(__file__).resolve().parent
# Construct file paths relative to the base directory
CONFIG_PATH = BASE_DIR / "config" / "settings.json"

def print_logo():
    """Print the DarkForge logo with color."""
    logo = get_logo()
    print(Fore.RED + logo)
    print(Fore.CYAN + "DarkForge - Password Analysis and Generation Toolkit")
    print(Fore.CYAN + "=" * 60)
    print(Style.RESET_ALL)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    """Display the main menu and handle user input."""
    while True:
        clear_screen()
        print_logo()
        
        print(Fore.GREEN + "\nMAIN MENU:")
        print(Fore.WHITE + "1. Generate Passwords")
        print(Fore.WHITE + "2. Analyze Passwords")
        print(Fore.WHITE + "3. Attack Simulation")
        print(Fore.WHITE + "4. View History")
        print(Fore.WHITE + "5. Help")
        print(Fore.RED + "0. Exit")
        
        choice = input(Fore.YELLOW + "\nEnter your choice (0-5): " + Style.RESET_ALL)
        
        if choice == '1':
            generate_menu()
        elif choice == '2':
            analyze_menu()
        elif choice == '3':
            attack_menu()
        elif choice == '4':
            history_menu()
        elif choice == '5':
            help_menu()
        elif choice == '0':
            print(Fore.RED + "\nExiting DarkForge. Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "\nInvalid choice. Please try again.")
            input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

def generate_menu():
    """Display the generate submenu."""
    clear_screen()
    print(Fore.GREEN + get_section_art("password_generation"))
    print(Fore.GREEN + "\nGENERATE PASSWORDS MENU:")
    print(Fore.WHITE + "1. Generate from interactive input")
    print(Fore.WHITE + "2. Generate from saved profile")
    print(Fore.WHITE + "3. Save user profile")
    print(Fore.RED + "0. Back to main menu")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-3): " + Style.RESET_ALL)
    
    if choice == '1':
        # Call the generate command with interactive input
        print(Fore.CYAN + "\nGenerating passwords from interactive input...")
        
        try:
            # Collect user profile data interactively
            user_data = get_user_profile(source="cli")
            profile = UserProfile(**user_data)
            
            # Generate passwords
            passwords = generate_passwords(profile)
            
            # Ask user if they want to save the passwords
            save_option = input(Fore.YELLOW + f"\n{len(passwords)} passwords generated. Do you want to save them to a file? (y/n): " + Style.RESET_ALL).lower()
            
            if save_option == 'y':
                output_file = input(Fore.YELLOW + "\nEnter the output file path: " + Style.RESET_ALL)
                # Create directory if it doesn't exist
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save passwords to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    for password in passwords:
                        f.write(f"{password}\n")
                
                print(Fore.GREEN + f"\nPasswords saved to {output_file}")
            else:
                # Display a sample of passwords
                sample_size = min(20, len(passwords))
                print(Fore.GREEN + f"\nSample of generated passwords ({sample_size} of {len(passwords)}):")
                for i, pwd in enumerate(passwords[:sample_size]):
                    print(f"{i+1}. {pwd}")
                print(Fore.YELLOW + f"... and {len(passwords) - sample_size} more.")
        
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
            
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    elif choice == '2':
        # Call the generate command with file input
        profile_file = input("\nEnter the profile file path: ")
        try:
            # Load user profile from file
            user_data = get_user_profile(source="file", file_path=profile_file)
            profile = UserProfile(**user_data)
            
            # Generate passwords
            passwords = generate_passwords(profile)
            
            # Ask user if they want to save the passwords
            save_option = input(Fore.YELLOW + f"\n{len(passwords)} passwords generated. Do you want to save them to a file? (y/n): " + Style.RESET_ALL).lower()
            
            if save_option == 'y':
                output_file = input(Fore.YELLOW + "\nEnter the output file path: " + Style.RESET_ALL)
                # Create directory if it doesn't exist
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save passwords to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    for password in passwords:
                        f.write(f"{password}\n")
                
                print(Fore.GREEN + f"\nPasswords saved to {output_file}")
            else:
                # Display a sample of passwords
                sample_size = min(20, len(passwords))
                print(Fore.GREEN + f"\nSample of generated passwords ({sample_size} of {len(passwords)}):")
                for i, pwd in enumerate(passwords[:sample_size]):
                    print(f"{i+1}. {pwd}")
                print(Fore.YELLOW + f"... and {len(passwords) - sample_size} more.")
                
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
            
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    elif choice == '3':
        # Call the collect command to save user profile
        try:
            # Collect user profile data interactively
            user_data = get_user_profile(source="cli")
            profile = UserProfile(**user_data)
            
            # Ask for output file path
            output_file = input(Fore.YELLOW + "\nEnter the output file path: " + Style.RESET_ALL)
            
            # Create directory if it doesn't exist
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save profile to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4)
            
            print(Fore.GREEN + f"\nUser profile saved to {output_file}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
            
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    elif choice == '0':
        return
    else:
        print(Fore.RED + "\nInvalid choice. Please try again.")
        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
        generate_menu()

def analyze_menu():
    """Display the analyze submenu."""
    clear_screen()
    print(Fore.BLUE + get_section_art("password_analysis"))
    print(Fore.BLUE + "\nANALYZE PASSWORDS MENU:")
    print(Fore.WHITE + "1. Analyze password file")
    print(Fore.WHITE + "2. Check single password")
    print(Fore.WHITE + "3. Pattern analysis only")
    print(Fore.RED + "0. Back to main menu")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-3): " + Style.RESET_ALL)
    
    # Implement menu options similar to generate_menu()
    input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

def attack_menu():
    """Display the attack simulation submenu."""
    clear_screen()
    print(Fore.MAGENTA + get_section_art("attack_simulation"))
    print(Fore.MAGENTA + "\nATTACK SIMULATION MENU:")
    print(Fore.WHITE + "1. Export passwords for cracking tools")
    print(Fore.WHITE + "2. Simulate brute force attack")
    print(Fore.WHITE + "3. Simulate dictionary attack")
    print(Fore.RED + "0. Back to main menu")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-3): " + Style.RESET_ALL)
    
    # Implement menu options
    input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

def history_menu():
    """Display the history submenu."""
    clear_screen()
    print(Fore.CYAN + get_section_art("database"))
    print(Fore.CYAN + "\nHISTORY MENU:")
    print(Fore.WHITE + "1. View user profiles")
    print(Fore.WHITE + "2. View password analysis history")
    print(Fore.WHITE + "3. View attack simulation history")
    print(Fore.WHITE + "4. View password generation history")
    print(Fore.RED + "0. Back to main menu")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-4): " + Style.RESET_ALL)
    
    # Implement menu options
    input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

def help_menu():
    """Display the help submenu."""
    clear_screen()
    print(Fore.YELLOW + get_section_art("help"))
    print(Fore.YELLOW + "\nHELP MENU:")
    print(Fore.WHITE + "1. Getting started")
    print(Fore.WHITE + "2. Command reference")
    print(Fore.WHITE + "3. Examples")
    print(Fore.WHITE + "4. Troubleshooting")
    print(Fore.RED + "0. Back to main menu")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-4): " + Style.RESET_ALL)
    
    # Implement menu options
    input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    # Initialize database
    db = Database()
    
    # Check if running with command-line arguments
    if len(sys.argv) > 1:
        # Pass to Click CLI
        # cli() # This would call your existing Click CLI
        pass
    else:
        # Interactive menu mode
        try:
            main_menu()
        except KeyboardInterrupt:
            print(Fore.RED + "\n\nOperation cancelled by user. Exiting.")
            sys.exit(0) 