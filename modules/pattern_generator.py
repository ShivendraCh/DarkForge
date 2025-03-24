#!/usr/bin/env python3
"""
pattern_generator.py

This module generates password candidates for DarkForge using various algorithms
derived from the user profile data. It leverages a set of string templates,
then applies multiple transformations (e.g., appending numbers, reversing, leetspeak)
to generate a comprehensive password list, aiming for 4000–8000 variants.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import json
from typing import List, Dict
from .data_input.collector import UserProfile

# -----------------------------------------------------------------------------
# ALGORITHM_TEMPLATE: List of String Templates for Password Generation
# -----------------------------------------------------------------------------
ALGORITHM_TEMPLATE = [
    "{first_name}{last_name}",
    "{first_name}{birth_year}",
    "{last_name}{birth_year}",
    "{nickname}{birth_year}",  # Assumes a 'nickname' field exists in UserProfile.
    "{first_name}{last_name}{birth_year}",
    "{last_name}{first_name}{birth_year}",
    "{first_name}{birth_month:02d}{birth_year}",
    "{last_name}{birth_month:02d}{birth_year}",
    "{first_name}{birthdate:02d}{birth_year}",
    "{last_name}{birthdate:02d}{birth_year}",
    "{first_name}{pet_name}",
    "{last_name}{pet_name}",
    "{first_name}{favorite_movie}",
    "{last_name}{favorite_movie}",
    "{first_name}{favorite_song}",
    "{last_name}{favorite_song}",
    "{first_name}{favorite_band}",
    "{last_name}{favorite_band}",
    "{first_name}{favorite_sport}",
    "{last_name}{favorite_sport}",
    "{first_name}{favorite_book}",
    "{last_name}{favorite_book}",
    "{first_name}{favorite_celebrity}",
    "{last_name}{favorite_celebrity}",
    "{first_name}{gamer_tag}",
    "{last_name}{gamer_tag}",
    # Additional Templates (Name and Birthdate)
    "{first_name}{birthdate_str}{birth_month_str}",
    "{last_name}{birthdate_str}{birth_month_str}",
    "{first_name}{last_name}{birthdate_str}{birth_month_str}",
    "{last_name}{first_name}{birthdate_str}{birth_month_str}",
    "{first_name_short_3}{last_name_short_3}{birth_year}",
    "{first_name_short_2}{last_name_short_2}{birth_year}",
    "{first_name_initial}{last_name_initial}{birth_year}",
    "{first_name_initial}{last_name}{birthdate_str}{birth_month_str}",
    "{last_name_initial}{first_name}{birthdate_str}{birth_month_str}",
    "{first_name}{last_name_initial}{birthdate_str}{birth_month_str}",
    "{last_name}{first_name_initial}{birthdate_str}{birth_month_str}",
    # Name and Birthdate with Special Characters
    "{last_name}@{birth_year}",
    "{first_name}@{birth_year}",
    "{first_name}{last_name}@{birth_year}",
    "{birth_year}@{first_name}",
    "{first_name}{last_name_initial}@{birth_year}",
    "{last_name}{first_name_initial}@{birth_year}",
    "{first_name_initial}{last_name}@{birth_year}",
    "{last_name_initial}{first_name}@{birth_year}",
    "{first_name}{birth_year}!",
    "{last_name}{birth_year}?",
    "{first_name}{last_name}#",
    "{birthdate_str}{birth_month_str}{birth_year}@",
    "{pet_name}{birth_year}$",
    # Personal Relationships
    "{father_name}{birth_year}",
    "{mother_name}{birth_year}",
    "{pet_name}{birth_year}",
    "{first_name}{father_name}{birth_year}",
    "{last_name}{mother_name}{birth_year}",
    "{pet_name}{first_name}{birth_year}",
    "{spouse_name}{birth_year}",
    "{first_name}{spouse_name}{birth_year}",
    "{last_name}{spouse_name}{birth_year}",
    "{child_name}{birth_year}",
    "{first_name}{child_name}{birth_year}",
    "{last_name}{child_name}{birth_year}",
    "{father_name_initial}{mother_name_initial}{birth_year}",
    "{pet_name}{first_name_initial}{last_name_initial}{birth_year}",
    "{spouse_name}{child_name}{birth_year}",
    # Creative Combinations
    "{first_name}{mother_name}{pet_name}",
    "{last_name}{father_name}{spouse_name}",
    "{first_name}{mother_name}{birth_year}",
    "{last_name}{father_name}{birth_year}",
    "{pet_name}{first_name}{birthdate_str}{birth_month_str}",
    "{spouse_name}{last_name}{birth_year}",
    "{child_name}{first_name}{birth_year}",
    "{first_name}{last_name}{pet_name}{birth_year}",
    # With Simple Sequences
    "{first_name}123456",
    "123456{last_name}",
    "{birth_year}abcdef",
    "abcdef{birth_year}",
    "{first_name}password",
    "password{last_name}",
    # Birthdate Variations
    "{birth_month_str}/{birthdate_str}/{birth_year}",
    "{birthdate_str}-{birth_month_str}-{birth_year}",
    "{first_name}{birth_month_str}/{birthdate_str}",
    "{last_name}{birth_year}-{birth_month_str}",
    "{birth_year}{first_name}{last_name}",
    # Reversed Strings
    "{first_name_rev}{birth_year}",
    "{last_name_rev}{birth_year}",
    "{first_name}{last_name_rev}{birth_year}",
    "{first_name_rev}{last_name}{birth_year}",
    "{birth_year_rev}{first_name}",
    "{birth_year_rev}{last_name}",
    "{first_name}{birth_year_rev}{last_name}",
    # With Special Characters (Middle)
    "{first_name}!{last_name}{birth_year}",
    "{last_name}@{first_name}{birth_year}",
    "{birth_year}#{first_name}{last_name}",
    "{first_name}{last_name}$ {birthdate_str}{birth_month_str}",
    "{birthdate_str}{birth_month_str}%{first_name}{last_name}",
]

# -----------------------------------------------------------------------------
# Precomputation: Compute Additional Fields from the UserProfile
# -----------------------------------------------------------------------------
def compute_extra_fields(profile: UserProfile) -> dict:
    """
    Compute additional fields required by the templates.
    Returns a dictionary containing the original profile data plus derived fields.
    """
    data = profile.dict()
    # Create padded versions of numeric fields (ensure the key names match the template)
    data["birthdate_str"] = f"{data['birthdate']:02d}"
    data["birth_month_str"] = f"{data['birth_month']:02d}"
    # Substring fields
    data["first_name_short_3"] = data["first_name"][:3] if data["first_name"] else ""
    data["last_name_short_3"] = data["last_name"][:3] if data["last_name"] else ""
    data["first_name_short_2"] = data["first_name"][:2] if data["first_name"] else ""
    data["last_name_short_2"] = data["last_name"][:2] if data["last_name"] else ""
    # Initials
    data["first_name_initial"] = data["first_name"][0] if data["first_name"] else ""
    data["last_name_initial"] = data["last_name"][0] if data["last_name"] else ""
    data["father_name_initial"] = data["father_name"][0] if data.get("father_name") else ""
    data["mother_name_initial"] = data["mother_name"][0] if data.get("mother_name") else ""
    # Reversed strings
    data["first_name_rev"] = data["first_name"][::-1] if data["first_name"] else ""
    data["last_name_rev"] = data["last_name"][::-1] if data["last_name"] else ""
    data["birth_year_rev"] = str(data["birth_year"])[::-1]
    # If a nickname field exists, ensure it is in the data dictionary.
    if "nickname" not in data or data["nickname"] is None:
        data["nickname"] = ""
    return data

# -----------------------------------------------------------------------------
# Base Password Generation Function
# -----------------------------------------------------------------------------
def generate_base_passwords(profile: UserProfile) -> List[str]:
    """
    Generate base passwords using the ALGORITHM_TEMPLATE.
    Substitutes computed fields from the profile into each template.
    Templates that fail (due to missing data) are skipped.
    """
    base_passwords = []
    computed_data: Dict = compute_extra_fields(profile)
    for template in ALGORITHM_TEMPLATE:
        try:
            formatted = template.format(**computed_data)
            if formatted and formatted not in base_passwords:
                base_passwords.append(formatted)
        except (KeyError, ValueError):
            continue
    return base_passwords

# -----------------------------------------------------------------------------
# Transformation Functions
# -----------------------------------------------------------------------------
def append_123(pwd: str) -> str:
    return f"{pwd}123"

def prepend_123(pwd: str) -> str:
    return f"123{pwd}"

def append_exclamation(pwd: str) -> str:
    return f"{pwd}!"

def prepend_exclamation(pwd: str) -> str:
    return f"!{pwd}"

def reverse_string(pwd: str) -> str:
    return pwd[::-1]

def leetspeak(pwd: str) -> str:
    mapping = str.maketrans("aAeEiIoOsStT", "4433110055")
    return pwd.translate(mapping)

def alternating_case(pwd: str) -> str:
    return "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(pwd))

# List of transformation functions.
TRANSFORMATIONS = [
    lambda pwd: pwd,  # Identity transformation.
    append_123,
    prepend_123,
    append_exclamation,
    prepend_exclamation,
    reverse_string,
    leetspeak,
    alternating_case,
]

# -----------------------------------------------------------------------------
# Apply Transformations Function
# -----------------------------------------------------------------------------
def apply_transformations(password: str) -> List[str]:
    """
    Apply all transformation functions to the given password.
    Returns a list of unique transformed variants.
    """
    transformed = []
    for transformation in TRANSFORMATIONS:
        try:
            new_pwd = transformation(password)
            if new_pwd and new_pwd not in transformed:
                transformed.append(new_pwd)
        except Exception:
            continue
    return transformed

# -----------------------------------------------------------------------------
# Main Password Generation Function
# -----------------------------------------------------------------------------
def generate_passwords(profile: UserProfile) -> List[str]:
    """
    Generate a comprehensive list of candidate passwords by combining base templates
    with transformation functions.
    
    Returns:
        List[str]: A list of candidate passwords.
    """
    passwords = []
    base_passwords = generate_base_passwords(profile)
    for base in base_passwords:
        variants = apply_transformations(base)
        for variant in variants:
            if variant not in passwords:
                passwords.append(variant)
    return passwords

# -----------------------------------------------------------------------------
# CLI for Testing (using Click)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import click

    @click.command()
    @click.option("--file", "file_path", default=None, help="Path to JSON file with user profile data.")
    def main(file_path):
        """
        Main command to generate password candidates.
        Loads a UserProfile from a JSON file if provided, otherwise uses a sample profile.
        """
        try:
            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    profile_data = json.load(f)
                profile = UserProfile(**profile_data)
            else:
                # Sample profile for demonstration
                profile = UserProfile(
                    first_name="Shivendra",
                    last_name="Chauhan",
                    birthdate=3,
                    birth_month=9,
                    birth_year=2005,
                    birthplace="Delhi",
                    residence="Mumbai",
                    phone_number="1234567890",
                    email="shivendra@example.com",
                    father_name="Rajendra",
                    mother_name="Anjali",
                    # Optional fields:
                    nickname="Shivi",
                    gamer_tag="Ninja",
                    device_names=["iPhone", "DellLaptop"],
                    favorite_number=7,
                    facebook_id="shivendraFB",
                    twitter_id="@shivendra",
                    instagram_id="shivendra_ig",
                    linkedin_id="shivendra_linkedin",
                    github_id="shivendra_github",
                    reddit_id="u_shivendra",
                    tiktok_id="shivendra_tiktok",
                    snapchat_id="shivendra_snap",
                    pinterest_id="shivendra_pin",
                    youtube_id="shivendra_yt"
                )
            base_pwds = generate_base_passwords(profile)
            click.echo("Base Passwords:")
            for pwd in base_pwds:
                click.echo(pwd)
            all_pwds = generate_passwords(profile)
            click.echo("\nGenerated Password Candidates:")
            for pwd in all_pwds:
                click.echo(pwd)
            click.echo(f"\nTotal Passwords Generated: {len(all_pwds)}")
        except Exception as e:
            click.echo(f"An error occurred: {e}", err=True)
            raise

    main()