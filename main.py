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
from modules.pattern_generator import generate_passwords, ALGORITHM_TEMPLATE, TRANSFORMATIONS
from modules.password_analyzer import rate_password_strength, detect_patterns
from modules.attack_simulator import export_hashcat_format, export_john_format, simulate_brute_force, simulate_dictionary_attack
from modules.database import Database
from datetime import datetime

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
    print(Fore.RED + "DarkForge")
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
        
        print(Fore.CYAN + "╔" + "═" * 58 + "╗")
        print(Fore.CYAN + "║" + Fore.GREEN + " MAIN MENU:".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "╠" + "═" * 58 + "╣")
        print(Fore.CYAN + "║" + Fore.WHITE + " 1. Generate Passwords".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " 2. Analyze Passwords".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " 3. Export Formats".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " 4. View History".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.WHITE + " 5. Help".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.RED + " 0. Exit".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * 58 + "╝")
        
        choice = input(Fore.YELLOW + "\nEnter your choice (0-5): " + Style.RESET_ALL)
        
        if choice == '1':
            generate_menu()
        elif choice == '2':
            analyze_menu()
        elif choice == '3':
            export_menu()
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
    print(Fore.GREEN + "\nPASSWORD GENERATION")
    
    print(Fore.CYAN + "╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + Fore.GREEN + " GENERATE PASSWORDS MENU:".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 58 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + " 1. Generate from interactive input".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 2. Generate from saved profile".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 3. Save user profile".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.RED + " 0. Back to main menu".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-3): " + Style.RESET_ALL)
    
    if choice == '1':
        # Call the generate command with interactive input
        print(Fore.CYAN + "\nGenerating passwords from interactive input...")
        
        try:
            # Collect user profile data interactively
            user_data = get_user_profile(source="cli")
            profile = UserProfile(**user_data)
            
            # Save to database
            db = Database()
            profile_data = {
                "name": f"{user_data['first_name']} {user_data['last_name']}",
                "email": user_data['email'],
                "birth_date": f"{user_data['birthdate']}/{user_data['birth_month']}/{user_data['birth_year']}",
                "phone": user_data['phone_number'],
                "address": user_data['residence']
            }
            profile_id = db.save_user_profile(profile_data)
            
            # Generate passwords
            passwords = generate_passwords(profile)
            
            # Ask user if they want to save the passwords
            save_option = input(Fore.YELLOW + f"\n{len(passwords)} passwords generated. Do you want to save them to a file? (y/n): " + Style.RESET_ALL).lower()
            
            if save_option == 'y':
                # Get output filename (without extension)
                output_filename = input(Fore.YELLOW + "\nEnter output filename (without extension): " + Style.RESET_ALL)
                if not output_filename:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"passwords_{timestamp}"
                
                # Save to output/txt directory by default
                output_dir = Path("output/txt")
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / f"{output_filename}.txt"
                
                # Save passwords to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    for password in passwords:
                        f.write(f"{password}\n")
                
                # Record in database
                db.save_password_generation(profile_id, len(passwords), str(output_file))
                
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
        try:
            # First check the templates directory
            template_dir = Path("templates")
            if template_dir.exists():
                templates = list(template_dir.glob("*.json"))
                if templates:
                    print(Fore.CYAN + "\nAvailable templates:")
                    for i, template in enumerate(templates, 1):
                        print(f"{i}. {template.name}")
                    
                    use_template = input(Fore.YELLOW + "\nUse a template? (y/n): " + Style.RESET_ALL).lower()
                    if use_template == 'y':
                        template_num = input(Fore.YELLOW + "Enter template number: " + Style.RESET_ALL)
                        try:
                            template_idx = int(template_num) - 1
                            if 0 <= template_idx < len(templates):
                                profile_file = str(templates[template_idx])
                            else:
                                print(Fore.RED + "\nInvalid template number.")
                                profile_file = input(Fore.YELLOW + "\nEnter the profile file path: " + Style.RESET_ALL)
                        except ValueError:
                            print(Fore.RED + "\nInvalid input.")
                            profile_file = input(Fore.YELLOW + "\nEnter the profile file path: " + Style.RESET_ALL)
                    else:
                        profile_file = input(Fore.YELLOW + "\nEnter the profile file path: " + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNo templates found in templates directory.")
                    profile_file = input(Fore.YELLOW + "\nEnter the profile file path: " + Style.RESET_ALL)
            else:
                profile_file = input(Fore.YELLOW + "\nEnter the profile file path: " + Style.RESET_ALL)
            
            # Check if file exists
            if not Path(profile_file).exists():
                print(Fore.RED + f"\nError: File not found: {profile_file}")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
            
            # Load user profile from file
            user_data = get_user_profile(source="file", file_path=profile_file)
            profile = UserProfile(**user_data)
            
            # Save to database
            db = Database()
            profile_data = {
                "name": f"{user_data['first_name']} {user_data['last_name']}",
                "email": user_data['email'],
                "birth_date": f"{user_data['birthdate']}/{user_data['birth_month']}/{user_data['birth_year']}",
                "phone": user_data['phone_number'],
                "address": user_data['residence']
            }
            profile_id = db.save_user_profile(profile_data)
            
            # Generate passwords
            passwords = generate_passwords(profile)
            
            # Ask user if they want to save the passwords
            save_option = input(Fore.YELLOW + f"\n{len(passwords)} passwords generated. Do you want to save them to a file? (y/n): " + Style.RESET_ALL).lower()
            
            if save_option == 'y':
                # Get output filename (without extension)
                output_filename = input(Fore.YELLOW + "\nEnter output filename (without extension): " + Style.RESET_ALL)
                if not output_filename:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"passwords_{timestamp}"
                
                # Save to output/txt directory by default
                output_dir = Path("output/txt")
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / f"{output_filename}.txt"
                
                # Save passwords to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    for password in passwords:
                        f.write(f"{password}\n")
                
                # Record in database
                db.save_password_generation(profile_id, len(passwords), str(output_file))
                
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
            
            # Save to database
            db = Database()
            profile_data = {
                "name": f"{user_data['first_name']} {user_data['last_name']}",
                "email": user_data['email'],
                "birth_date": f"{user_data['birthdate']}/{user_data['birth_month']}/{user_data['birth_year']}",
                "phone": user_data['phone_number'],
                "address": user_data['residence']
            }
            profile_id = db.save_user_profile(profile_data)
            
            # Get output filename (without extension)
            output_filename = input(Fore.YELLOW + "\nEnter output filename (without extension): " + Style.RESET_ALL)
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"profile_{timestamp}"
            
            # Save to templates directory by default
            output_dir = Path("templates")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{output_filename}.json"
            
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
    print(Fore.BLUE + "\nPASSWORD ANALYSIS")
    
    print(Fore.CYAN + "╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + Fore.BLUE + " ANALYZE PASSWORDS MENU:".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 58 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + " 1. Analyze password file".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 2. Check single password".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 3. Pattern analysis only".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.RED + " 0. Back to main menu".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-3): " + Style.RESET_ALL)
    
    if choice == '1':
        try:
            password_file = input(Fore.YELLOW + "\nEnter the password file path: " + Style.RESET_ALL)
            
            # Check if file exists
            if not Path(password_file).exists():
                print(Fore.RED + f"\nError: File not found: {password_file}")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
                
            output_dir = input(Fore.YELLOW + "\nEnter output directory for analysis results (default: ./analysis_results): " + Style.RESET_ALL)
            if not output_dir:
                output_dir = "./analysis_results"
                
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Read passwords from file
            with open(password_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
                
            print(Fore.CYAN + f"\nAnalyzing {len(passwords)} passwords...")
            
            # Analyze each password
            analysis_results = {
                "total_passwords": len(passwords),
                "passwords": [],
                "length_stats": {},
                "strength_distribution": {
                    "Very Weak": 0,
                    "Weak": 0,
                    "Moderate": 0,
                    "Strong": 0,
                    "Very Strong": 0
                }
            }
            
            strengths = []
            lengths = []
            
            for password in passwords:
                result = rate_password_strength(password)
                analysis_results["passwords"].append(result)
                analysis_results["strength_distribution"][result["strength"]] += 1
                strengths.append(result["strength"])
                lengths.append(len(password))
            
            # Calculate length statistics
            analysis_results["length_stats"] = {
                "min": min(lengths),
                "max": max(lengths),
                "avg": sum(lengths) / len(lengths),
            }
            
            # Generate timestamp for the report filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = output_path / f"analysis_report_{timestamp}.json"
            
            # Save analysis results
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=4)
            
            print(Fore.GREEN + f"\nAnalysis complete! Results saved to {report_file}")
            
            # Save to database
            db = Database()
            for result in analysis_results["passwords"]:
                db.save_password_analysis(result)
            
            # Show summary
            print(Fore.CYAN + "\nAnalysis Summary:")
            print(f"Total Passwords: {len(passwords)}")
            print(f"Average Length: {analysis_results['length_stats']['avg']:.2f}")
            print(f"Strength Distribution:")
            for strength, count in analysis_results["strength_distribution"].items():
                percentage = (count / len(passwords)) * 100
                print(f"  {strength}: {count} ({percentage:.2f}%)")
                
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '2':
        try:
            password = input(Fore.YELLOW + "\nEnter password to analyze: " + Style.RESET_ALL)
            
            if not password:
                print(Fore.RED + "\nError: Password cannot be empty")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
                
            print(Fore.CYAN + "\nAnalyzing password...")
            
            # Analyze password
            result = rate_password_strength(password)
            
            # Display results
            print(Fore.GREEN + "\nAnalysis Results:")
            print(f"Password: {password}")
            print(f"Length: {result['length']}")
            print(f"Entropy: {result['entropy']:.2f} bits")
            print(f"Strength: {result['strength']}")
            print(f"Score: {result['score']}/5")
            
            if result["patterns"]:
                print("\nDetected Patterns:")
                for pattern_type, matches in result["patterns"].items():
                    print(f"  {pattern_type}: {', '.join(matches)}")
            
            # Save to database
            db = Database()
            db.save_password_analysis(result)
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '3':
        try:
            password_file = input(Fore.YELLOW + "\nEnter the password file path: " + Style.RESET_ALL)
            
            # Check if file exists
            if not Path(password_file).exists():
                print(Fore.RED + f"\nError: File not found: {password_file}")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
                
            # Read passwords from file
            with open(password_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
                
            print(Fore.CYAN + f"\nPerforming pattern analysis on {len(passwords)} passwords...")
            
            # Analyze patterns across all passwords
            pattern_counts = {}
            for password in passwords:
                patterns = detect_patterns(password)
                for pattern_type, matches in patterns.items():
                    if pattern_type not in pattern_counts:
                        pattern_counts[pattern_type] = 0
                    pattern_counts[pattern_type] += 1
            
            # Display results
            print(Fore.GREEN + "\nPattern Analysis Results:")
            print(f"Total Passwords: {len(passwords)}")
            print("\nPattern Frequency:")
            
            for pattern_type, count in pattern_counts.items():
                percentage = (count / len(passwords)) * 100
                print(f"  {pattern_type}: {count} ({percentage:.2f}%)")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '0':
        return
    else:
        print(Fore.RED + "\nInvalid choice. Please try again.")
        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
        analyze_menu()

def export_menu():
    """Display the export formats submenu."""
    clear_screen()
    print(Fore.MAGENTA + "\nEXPORT FORMATS")
    
    print(Fore.CYAN + "╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + Fore.MAGENTA + " EXPORT FORMATS MENU:".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 58 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + " 1. Export passwords to plain text".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 2. Export passwords to Hashcat format".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 3. Export passwords to John the Ripper format".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.RED + " 0. Back to main menu".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-3): " + Style.RESET_ALL)
    
    if choice == '1':
        try:
            password_file = input(Fore.YELLOW + "\nEnter the password file path: " + Style.RESET_ALL)
            
            # Check if file exists
            if not Path(password_file).exists():
                print(Fore.RED + f"\nError: File not found: {password_file}")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
            
            # Get output filename (without extension)
            output_filename = input(Fore.YELLOW + "\nEnter output filename (without extension): " + Style.RESET_ALL)
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"passwords_{timestamp}"
            
            # Save to output/txt directory by default
            output_dir = Path("output/txt")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{output_filename}.txt"
            
            # Read passwords
            with open(password_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            # Export passwords
            with open(output_file, 'w', encoding='utf-8') as f:
                for password in passwords:
                    f.write(f"{password}\n")
            
            print(Fore.GREEN + f"\nExported {len(passwords)} passwords to {output_file}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '2':
        try:
            password_file = input(Fore.YELLOW + "\nEnter the password file path: " + Style.RESET_ALL)
            
            # Check if file exists
            if not Path(password_file).exists():
                print(Fore.RED + f"\nError: File not found: {password_file}")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
            
            # Choose hash type
            print(Fore.CYAN + "\nChoose hash type:")
            print(Fore.WHITE + "1. MD5")
            print(Fore.WHITE + "2. SHA1")
            print(Fore.WHITE + "3. SHA256")
            print(Fore.WHITE + "4. SHA512")
            print(Fore.WHITE + "5. NTLM")
            
            hash_choice = input(Fore.YELLOW + "\nEnter your choice (1-5): " + Style.RESET_ALL)
            
            if hash_choice == '1':
                hash_type = "md5"
            elif hash_choice == '2':
                hash_type = "sha1"
            elif hash_choice == '3':
                hash_type = "sha256"
            elif hash_choice == '4':
                hash_type = "sha512"
            elif hash_choice == '5':
                hash_type = "ntlm"
            else:
                print(Fore.RED + "\nInvalid choice. Using SHA256.")
                hash_type = "sha256"
            
            # Get output filename (without extension)
            output_filename = input(Fore.YELLOW + "\nEnter output filename (without extension): " + Style.RESET_ALL)
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"hashcat_{hash_type}_{timestamp}"
            
            # Save to output/hashcat directory by default
            output_dir = Path("output/hashcat")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{output_filename}.hash"
            
            # Read passwords
            with open(password_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            # Export passwords in hashcat format
            export_hashcat_format(passwords, output_file, hash_type)
            
            print(Fore.GREEN + f"\nExported {len(passwords)} passwords in {hash_type} format to {output_file}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '3':
        try:
            password_file = input(Fore.YELLOW + "\nEnter the password file path: " + Style.RESET_ALL)
            
            # Check if file exists
            if not Path(password_file).exists():
                print(Fore.RED + f"\nError: File not found: {password_file}")
                input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
                return
            
            # Choose hash type
            print(Fore.CYAN + "\nChoose hash type:")
            print(Fore.WHITE + "1. MD5")
            print(Fore.WHITE + "2. SHA1")
            print(Fore.WHITE + "3. SHA256")
            print(Fore.WHITE + "4. SHA512")
            print(Fore.WHITE + "5. NTLM")
            
            hash_choice = input(Fore.YELLOW + "\nEnter your choice (1-5): " + Style.RESET_ALL)
            
            if hash_choice == '1':
                hash_type = "md5"
            elif hash_choice == '2':
                hash_type = "sha1"
            elif hash_choice == '3':
                hash_type = "sha256"
            elif hash_choice == '4':
                hash_type = "sha512"
            elif hash_choice == '5':
                hash_type = "ntlm"
            else:
                print(Fore.RED + "\nInvalid choice. Using SHA256.")
                hash_type = "sha256"
            
            # Get output filename (without extension)
            output_filename = input(Fore.YELLOW + "\nEnter output filename (without extension): " + Style.RESET_ALL)
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"john_{hash_type}_{timestamp}"
            
            # Save to output/john directory by default
            output_dir = Path("output/john")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{output_filename}.john"
            
            # Read passwords
            with open(password_file, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            # Export passwords in john format
            export_john_format(passwords, output_file, hash_type)
            
            print(Fore.GREEN + f"\nExported {len(passwords)} passwords in {hash_type} format to {output_file}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '0':
        return
    else:
        print(Fore.RED + "\nInvalid choice. Please try again.")
        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
        export_menu()

def history_menu():
    """Display the history submenu."""
    clear_screen()
    print(Fore.CYAN + "\nHISTORY")
    
    print(Fore.CYAN + "╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + Fore.CYAN + " HISTORY MENU:".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 58 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + " 1. View user profiles".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 2. View password analysis history".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 3. View attack simulation history".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 4. View password generation history".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.RED + " 0. Back to main menu".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-4): " + Style.RESET_ALL)
    
    db = Database()
    
    if choice == '1':
        try:
            limit = input(Fore.YELLOW + "\nEnter number of records to view (default: 10): " + Style.RESET_ALL)
            limit = int(limit) if limit and limit.isdigit() else 10
            
            print(Fore.CYAN + f"\nRetrieving user profiles (limit: {limit})...")
            
            # Get profile IDs from password generation history
            generation_history = db.get_password_generation_history(limit)
            
            if not generation_history:
                print(Fore.YELLOW + "\nNo user profiles found.")
            else:
                print(Fore.GREEN + "\nUser Profiles:")
                
                for i, entry in enumerate(generation_history, 1):
                    profile = db.get_user_profile(entry["user_profile_id"])
                    if profile:
                        print(f"\n{i}. Profile ID: {profile['id']}")
                        print(f"   Name: {profile['name']}")
                        print(f"   Email: {profile['email']}")
                        print(f"   Date: {profile['birth_date']}")
                        print(f"   Created: {profile['created_at']}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '2':
        try:
            limit = input(Fore.YELLOW + "\nEnter number of records to view (default: 10): " + Style.RESET_ALL)
            limit = int(limit) if limit and limit.isdigit() else 10
            
            print(Fore.CYAN + f"\nRetrieving password analysis history (limit: {limit})...")
            
            # Get analysis history
            analysis_history = db.get_password_analysis_history(limit)
            
            if not analysis_history:
                print(Fore.YELLOW + "\nNo password analysis history found.")
            else:
                print(Fore.GREEN + "\nPassword Analysis History:")
                
                for i, entry in enumerate(analysis_history, 1):
                    print(f"\n{i}. Password: {entry['password']}")
                    print(f"   Entropy: {entry['entropy']:.2f} bits")
                    print(f"   Strength: {entry['strength']}")
                    print(f"   Score: {entry['score']}/5")
                    print(f"   Length: {entry['length']}")
                    print(f"   Created: {entry['created_at']}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '3':
        try:
            limit = input(Fore.YELLOW + "\nEnter number of records to view (default: 10): " + Style.RESET_ALL)
            limit = int(limit) if limit and limit.isdigit() else 10
            
            print(Fore.CYAN + f"\nRetrieving attack simulation history (limit: {limit})...")
            
            # Get simulation history
            simulation_history = db.get_attack_simulation_history(limit)
            
            if not simulation_history:
                print(Fore.YELLOW + "\nNo attack simulation history found.")
            else:
                print(Fore.GREEN + "\nAttack Simulation History:")
                
                for i, entry in enumerate(simulation_history, 1):
                    print(f"\n{i}. Password: {entry['password']}")
                    print(f"   Attack Type: {entry['attack_type']}")
                    print(f"   Attempts: {entry['attempts']:,}")
                    print(f"   Duration: {entry['duration']:.2f} seconds")
                    print(f"   Attempts/sec: {entry['attempts_per_second']:.2f}")
                    print(f"   Found: {'Yes' if entry['found'] else 'No'}")
                    print(f"   Created: {entry['created_at']}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '4':
        try:
            limit = input(Fore.YELLOW + "\nEnter number of records to view (default: 10): " + Style.RESET_ALL)
            limit = int(limit) if limit and limit.isdigit() else 10
            
            print(Fore.CYAN + f"\nRetrieving password generation history (limit: {limit})...")
            
            # Get generation history
            generation_history = db.get_password_generation_history(limit)
            
            if not generation_history:
                print(Fore.YELLOW + "\nNo password generation history found.")
            else:
                print(Fore.GREEN + "\nPassword Generation History:")
                
                for i, entry in enumerate(generation_history, 1):
                    print(f"\n{i}. User Profile: {entry['user_name'] or entry['user_profile_id']}")
                    print(f"   Total Passwords: {entry['total_passwords']}")
                    print(f"   Output File: {entry['output_file']}")
                    print(f"   Created: {entry['created_at']}")
            
        except Exception as e:
            print(Fore.RED + f"\nError: {e}")
        
        input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)
    
    elif choice == '0':
        return
    else:
        print(Fore.RED + "\nInvalid choice. Please try again.")
        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
        history_menu()

def help_menu():
    """Display the help submenu."""
    clear_screen()
    print(Fore.YELLOW + "\nHELP")
    
    print(Fore.CYAN + "╔" + "═" * 58 + "╗")
    print(Fore.CYAN + "║" + Fore.YELLOW + " HELP MENU:".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╠" + "═" * 58 + "╣")
    print(Fore.CYAN + "║" + Fore.WHITE + " 1. Getting started".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 2. Command reference".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 3. Examples".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.WHITE + " 4. Troubleshooting".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "║" + Fore.RED + " 0. Back to main menu".ljust(57) + Fore.CYAN + "║")
    print(Fore.CYAN + "╚" + "═" * 58 + "╝")
    
    choice = input(Fore.YELLOW + "\nEnter your choice (0-4): " + Style.RESET_ALL)
    
    if choice == '1':
        clear_screen()
        
        # Calculate number of patterns and transformations
        num_patterns = len(ALGORITHM_TEMPLATE)
        num_transforms = len(TRANSFORMATIONS)
        total_potential = num_patterns * num_transforms
        
        print(Fore.CYAN + "╔" + "═" * 58 + "╗")
        print(Fore.CYAN + "║" + Fore.WHITE + f" Password Generation Capacity:".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.YELLOW + f" • Base Patterns: {num_patterns}".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.YELLOW + f" • Transformations: {num_transforms}".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "║" + Fore.YELLOW + f" • Potential Combinations: {total_potential:,}".ljust(57) + Fore.CYAN + "║")
        print(Fore.CYAN + "╚" + "═" * 58 + "╝")
        
        print(Fore.CYAN + "\n1. Generate Passwords")
        print(Fore.WHITE + "   Start by generating passwords based on your personal information.")
        print(Fore.WHITE + "   You can enter data interactively or use a pre-saved profile.")
        print(Fore.WHITE + "   Generated passwords will be saved to a file of your choice.")
        
        print(Fore.CYAN + "\n2. Analyze Passwords")
        print(Fore.WHITE + "   Analyze your generated passwords to assess their strength.")
        print(Fore.WHITE + "   Check individual passwords or analyze entire files.")
        print(Fore.WHITE + "   Get detailed reports on password patterns and weaknesses.")
        
        print(Fore.CYAN + "\n3. Export Formats")
        print(Fore.WHITE + "   Export your passwords in various formats.")
        print(Fore.WHITE + "   Supports plain text, Hashcat, and John the Ripper formats.")
        print(Fore.WHITE + "   Automatically organizes files in the appropriate output folders.")
        
        print(Fore.CYAN + "\n4. Templates")
        print(Fore.WHITE + "   Templates are available in the templates/ directory.")
        print(Fore.WHITE + "   Edit the templates and use them for generating passwords.")
        
        print(Fore.CYAN + "\n5. Output Files")
        print(Fore.WHITE + "   Generated passwords are saved to the output/ directory.")
        print(Fore.WHITE + "   Different formats are saved in their respective subdirectories.")
        
    elif choice == '2':
        clear_screen()
        print(Fore.GREEN + "\nCOMMAND REFERENCE")
        print(Fore.CYAN + "\nGenerate Menu")
        print(Fore.WHITE + "1. Generate from interactive input - Collect personal data and generate passwords")
        print(Fore.WHITE + "2. Generate from saved profile - Use a pre-saved JSON profile")
        print(Fore.WHITE + "3. Save user profile - Save collected data for later use")
        
        print(Fore.CYAN + "\nAnalyze Menu")
        print(Fore.WHITE + "1. Analyze password file - Check strength of all passwords in a file")
        print(Fore.WHITE + "2. Check single password - Analyze a single password's strength")
        print(Fore.WHITE + "3. Pattern analysis only - Check patterns without strength assessment")
        
        print(Fore.CYAN + "\nAttack Menu")
        print(Fore.WHITE + "1. Export passwords - Export to various formats for cracking tools")
        print(Fore.WHITE + "2. Simulate brute force - Test how long a brute force attack would take")
        print(Fore.WHITE + "3. Simulate dictionary - Test password against a wordlist")
        
        print(Fore.CYAN + "\nHistory Menu")
        print(Fore.WHITE + "1. View user profiles - See saved user profiles")
        print(Fore.WHITE + "2. View password analysis - See previous password analyses")
        print(Fore.WHITE + "3. View attack simulation - See previous attack simulations")
        print(Fore.WHITE + "4. View password generation - See password generation history")
        
    elif choice == '3':
        clear_screen()
        print(Fore.GREEN + "\nEXAMPLES")
        print(Fore.CYAN + "\n1. Complete Password Workflow")
        print(Fore.WHITE + "   a. Generate passwords from personal information")
        print(Fore.WHITE + "   b. Save generated passwords to output/txt/my_passwords.txt")
        print(Fore.WHITE + "   c. Analyze the password file to assess strength")
        print(Fore.WHITE + "   d. Export passwords to hashcat format for testing")
        print(Fore.WHITE + "   e. Simulate a brute force attack on selected passwords")
        
        print(Fore.CYAN + "\n2. Using Templates")
        print(Fore.WHITE + "   a. Copy templates/user_profile_template.json to my_profile.json")
        print(Fore.WHITE + "   b. Edit my_profile.json with your personal information")
        print(Fore.WHITE + "   c. Generate passwords using the saved profile")
        print(Fore.WHITE + "   d. Analyze and export as needed")
        
        print(Fore.CYAN + "\n3. Pattern Analysis")
        print(Fore.WHITE + "   a. Generate or import a large password list")
        print(Fore.WHITE + "   b. Use pattern analysis to find common weaknesses")
        print(Fore.WHITE + "   c. Adjust your password generation strategy accordingly")
        
    elif choice == '4':
        clear_screen()
        print(Fore.GREEN + "\nTROUBLESHOOTING")
        print(Fore.CYAN + "\n1. File Not Found Errors")
        print(Fore.WHITE + "   Ensure you're using absolute paths or correct relative paths.")
        print(Fore.WHITE + "   Check that directories exist before trying to save files.")
        
        print(Fore.CYAN + "\n2. Permissions Issues")
        print(Fore.WHITE + "   Make sure you have write permissions in the output directory.")
        print(Fore.WHITE + "   Run the program with appropriate permissions if needed.")
        
        print(Fore.CYAN + "\n3. Database Errors")
        print(Fore.WHITE + "   The database file (darkforge.db) should be writable.")
        print(Fore.WHITE + "   If database is corrupted, delete it and restart the program.")
        
        print(Fore.CYAN + "\n4. Import Errors")
        print(Fore.WHITE + "   Ensure all dependencies are installed: pip install -r requirements.txt")
        print(Fore.WHITE + "   Python 3.6+ is required for this program.")
        
        print(Fore.CYAN + "\n5. Getting Help")
        print(Fore.WHITE + "   For more help, see the README.md file or user_manual directory.")
        print(Fore.WHITE + "   Report issues at the project's GitHub repository.")
        
    elif choice == '0':
        return
    else:
        print(Fore.RED + "\nInvalid choice. Please try again.")
        input(Fore.YELLOW + "Press Enter to continue..." + Style.RESET_ALL)
        help_menu()
    
    input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)

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