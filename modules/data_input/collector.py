#!/usr/bin/env python3
"""
collector.py

This module collects comprehensive OSINT data from the user for the DarkForge project.
It gathers 25 crucial fields based on analysis of real password leaks and vulnerable patterns.
Data is collected interactively via the CLI and validated using a Pydantic model.

Author: Shivendra Chauhan
Date: 21st March 2025
"""
import sys
import json
import logging
from typing import List, Dict, Optional
import click

from pydantic import BaseModel, ValidationError, EmailStr
from typing import Optional, List

# ===========================
# Logging Configuration
# ===========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ===========================
# Pydantic Data Model : UserProfile
# ===========================

class UserProfile(BaseModel):
    # Basic Information (Required)
    first_name: str
    last_name: str
    nickname: Optional[str] = None
    birthdate: int         # Day of month (1-31)
    birth_month: int       # Month as an integer (1-12)
    birth_year: int        # Four-digit year, e.g., 2005
    birthplace: str
    residence: str
    phone_number: str
    email: EmailStr        # Automatically validates email format
    
    # Primary Relationships
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    spouse_name: Optional[str] = None
    child_name: Optional[str] = None
    pet_name: Optional[str] = None
    company_name: Optional[str] = None
    ex_partner_name: Optional[str] = None
    
    # Education and Interests
    school_name: Optional[str] = None
    college_name: Optional[str] = None
    favorite_movie: Optional[str] = None
    favorite_song: Optional[str] = None
    favorite_band: Optional[str] = None
    favorite_sport: Optional[str] = None
    favorite_book: Optional[str] = None
    favorite_celebrity: Optional[str] = None
    gamer_tag: Optional[str] = None
    device_names: List[str] = []     # E.g., ["ShivsiPhone", "MyDellLaptop"]
    favorite_number: Optional[int] = None

    # Social Media and Online Accounts
    facebook_id: Optional[str] = None
    twitter_id: Optional[str] = None
    instagram_id: Optional[str] = None
    linkedin_id: Optional[str] = None
    github_id: Optional[str] = None
    reddit_id: Optional[str] = None
    tiktok_id: Optional[str] = None
    snapchat_id: Optional[str] = None
    pinterest_id: Optional[str] = None
    youtube_id: Optional[str] = None

# ===========================
# Helper Functions for Prompting
# ===========================

def prompt_input(prompt: str, required: bool = True) -> str:
     """
    Prompt the user for input.
    If the field is required, the prompt will repeat until a value is entered.
    """
     while True:
        value = input(prompt).strip()
        if required and not value:
            print("This field is required. Please try again.")
        else:
            return value

def prompt_int(prompt:str, required: bool = True) -> Optional[int]:
    """
    Prompt the user for an integer value.
    Repeats until a valid integer is entered if required.
    """    
    while True:
        value = prompt_input(prompt, required)
        if not value and not required:
            return None
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")

def prompt_list(prompt:str, required: bool = False) -> List[str]:
    """
    Prompt the user for a comma-separated list of strings.
    Returns a list after trimming whitespace from each entry.
    """
    value = prompt_input(prompt, required)
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


# ===========================
# Data Collection Functions
# ===========================

def collect_from_cli() -> Dict:
    """
    Collect user profile data interactively via the CLI.
    Returns a dictionary of the raw inputs that conforms to the UserProfile model.
    """
    logger.info("Welcome to the DarkForge OSINT Data Collector!")
    logger.info("Please provide the following information:")

    # Basic Information
    first_name = prompt_input("Enter First Name: ")
    last_name = prompt_input("Enter Last Name: ")
    nickname = prompt_input("Enter Nickname (optional): ", required=False)
    birthdate = prompt_int("Enter Birthdate (day as number, e.g., 3, 22): ")
    birth_month = prompt_int("Enter Birth Month (number, e.g., 9, 11): ")
    birth_year = prompt_int("Enter Birth Year (e.g., 2005): ")
    birthplace = prompt_input("Enter Birthplace (City/Country): ")
    residence = prompt_input("Enter Current Residence: ")
    phone_number = prompt_input("Enter Phone Number: ")
    email = prompt_input("Enter Email Address: ")

    # Primary Relationships
    father_name = prompt_input("Enter Father's Name (optional): ", required=False)
    mother_name = prompt_input("Enter Mother's Name (optional): ", required=False)
    spouse_name = prompt_input("Enter Spouse Name (optional): ", required=False)
    child_name = prompt_input("Enter Child's Name (optional): ", required=False)
    pet_name = prompt_input("Enter Pet Name (optional): ", required=False)
    company_name = prompt_input("Enter Company Name (optional): ", required=False)
    ex_partner_name = prompt_input("Enter Ex-Partner Name (optional): ", required=False)

    # Education and Interests
    school_name = prompt_input("Enter School Name (optional): ", required=False)
    college_name = prompt_input("Enter College Name (optional): ", required=False)
    favorite_movie = prompt_input("Enter Favorite Movie (optional): ", required=False)
    favorite_song = prompt_input("Enter Favorite Song (optional): ", required=False)
    favorite_band = prompt_input("Enter Favorite Band (optional): ", required=False)
    favorite_sport = prompt_input("Enter Favorite Sport (optional): ", required=False)
    favorite_book = prompt_input("Enter Favorite Book (optional): ", required=False)
    favorite_celebrity = prompt_input("Enter Favorite Celebrity (optional): ", required=False)
    gamer_tag = prompt_input("Enter Gamer Tag (optional): ", required=False)
    device_names = prompt_list("Enter Device Names (comma-separated, optional): ", required=False)
    favorite_number = prompt_int("Enter Favorite Number (optional): ", required=False)

    # Social Media and Online Accounts
    facebook_id = prompt_input("Enter Facebook ID (optional): ", required=False)
    twitter_id = prompt_input("Enter Twitter ID (optional): ", required=False)
    instagram_id = prompt_input("Enter Instagram ID (optional): ", required=False)
    linkedin_id = prompt_input("Enter LinkedIn ID (optional): ", required=False)
    github_id = prompt_input("Enter GitHub ID (optional): ", required=False)
    reddit_id = prompt_input("Enter Reddit ID (optional): ", required=False)
    tiktok_id = prompt_input("Enter TikTok ID (optional): ", required=False)
    snapchat_id = prompt_input("Enter Snapchat ID (optional): ", required=False)
    pinterest_id = prompt_input("Enter Pinterest ID (optional): ", required=False)
    youtube_id = prompt_input("Enter YouTube ID (optional): ", required=False)

    # Build raw data dictionary
    raw_data = {
        "first_name": first_name,
        "last_name": last_name,
        "nickname": nickname if nickname else None,
        "birthdate": birthdate,
        "birth_month": birth_month,
        "birth_year": birth_year,
        "birthplace": birthplace,
        "residence": residence,
        "phone_number": phone_number,
        "email": email,
        "father_name": father_name if father_name else None,
        "mother_name": mother_name if mother_name else None,
        "spouse_name": spouse_name if spouse_name else None,
        "child_name": child_name if child_name else None,
        "pet_name": pet_name if pet_name else None,
        "company_name": company_name if company_name else None,
        "ex_partner_name": ex_partner_name if ex_partner_name else None,
        "school_name": school_name if school_name else None,
        "college_name": college_name if college_name else None,
        "favorite_movie": favorite_movie if favorite_movie else None,
        "favorite_song": favorite_song if favorite_song else None,
        "favorite_band": favorite_band if favorite_band else None,
        "favorite_sport": favorite_sport if favorite_sport else None,
        "favorite_book": favorite_book if favorite_book else None,
        "favorite_celebrity": favorite_celebrity if favorite_celebrity else None,
        "gamer_tag": gamer_tag if gamer_tag else None,
        "device_names": device_names,
        "favorite_number": favorite_number,
        "facebook_id": facebook_id if facebook_id else None,
        "twitter_id": twitter_id if twitter_id else None,
        "instagram_id": instagram_id if instagram_id else None,
        "linkedin_id": linkedin_id if linkedin_id else None,
        "github_id": github_id if github_id else None,
        "reddit_id": reddit_id if reddit_id else None,
        "tiktok_id": tiktok_id if tiktok_id else None,
        "snapchat_id": snapchat_id if snapchat_id else None,
        "pinterest_id": pinterest_id if pinterest_id else None,
        "youtube_id": youtube_id if youtube_id else None
    }

    logger.info("Data collection complete.")
    return raw_data

def collect_from_file(file_path:str) -> Dict:
    """
    Collect user profile data from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        Dict: Parsed JSON data.
    """   
    try:
        logger.info(f"Attempting to read user profile data from file: {file_path}")
        with open(file_path, "r") as file:
            raw_data = json.load(file)
        logger.info("Data read successfully.")
        return raw_data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}, exc_info=True")
        raise
    except json.JSONDecodeError as jde:
        logger.error(f"Invalid JSON in file: {file_path} - {jde}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise

def get_user_profile(source: str = "cli", file_path: Optional[str] = None) -> dict:
    """
    Entry point for collecting user profile data.
    
    Args:
        source (str): 'cli' for interactive input, or 'file' for JSON file input.
        file_path (Optional[str]): Required if source is 'file'.
    
    Returns:
        Dict: Collected user profile data.
    """   
    if source == "cli":
        return collect_from_cli()
    elif source == "file":
        if not file_path:
            error_msg = "File path is required when source is 'file'."
            logger.error(error_msg)
            raise ValueError(error_msg)
        return collect_from_file(file_path)
    else:
        error_msg = f"Unsupported data source specified: {source}"
        logger.error(error_msg)
        raise ValueError(error_msg)

# ===========================
# Main Execution Block for Testing
# ===========================
@click.command()
@click.option("--source", default="cli" , type=click.Choice(["cli","file"]), help="Data source :'cli' for interactive input or 'file' for JSON file input")
@click.option("--file", "file_path", default=None, help="Path to the JSON file (requirment if --source is 'file').")
def main(source:str, file_path: Optional[str]):
    """
    Main command to collect user profile data for DarkForge.
    """
    try:
        raw_profile_data = get_user_profile(source=source, file_path=file_path)
        # Validate the data using the Pydantic model
        profile = UserProfile(**raw_profile_data)
        logger.info("Successfully collected and validated user profile data:")
        click.echo(profile.json(indent=2, sort_keys=True))
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}", exc_info=True)
        click.echo(f"Validation error occurred. Please check the inputs.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        click.echo(f"An unexpected error occurred. Please check the logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()