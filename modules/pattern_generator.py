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
    # Basic Name Combinations
    "{first_name}{last_name}",
    "{first_name_lower}{last_name_lower}",
    "{first_name_upper}{last_name_upper}",
    "{first_name_cap}{last_name_cap}",
    "{first_name}_{last_name}",
    "{first_name}.{last_name}",
    "{first_name}-{last_name}",
    "{last_name}{first_name}",
    "{last_name}_{first_name}",
    "{last_name}.{first_name}",
    "{last_name}-{first_name}",
    
    # With Birth Year
    "{first_name}{birth_year}",
    "{last_name}{birth_year}",
    "{first_name}{birth_year_short}",
    "{last_name}{birth_year_short}",
    "{nickname}{birth_year}",
    "{nickname}{birth_year_short}",
    "{first_name}{last_name}{birth_year}",
    "{first_name}{last_name}{birth_year_short}",
    "{last_name}{first_name}{birth_year}",
    "{last_name}{first_name}{birth_year_short}",
    "{first_name}_{birth_year}",
    "{last_name}_{birth_year}",
    "{birth_year}_{first_name}",
    "{birth_year}_{last_name}",
    "{first_name}{birth_year_first}{birth_year_middle}{birth_year_last}",
    "{last_name}{birth_year_first}{birth_year_middle}{birth_year_last}",
    
    # With Birth Month and Day
    "{first_name}{birth_month:02d}{birth_year}",
    "{last_name}{birth_month:02d}{birth_year}",
    "{first_name}{birth_month:02d}{birth_year_short}",
    "{last_name}{birth_month:02d}{birth_year_short}",
    "{first_name}{birthdate:02d}{birth_year}",
    "{last_name}{birthdate:02d}{birth_year}",
    "{first_name}{birthdate:02d}{birth_month:02d}",
    "{last_name}{birthdate:02d}{birth_month:02d}",
    "{first_name}{birthdate:02d}{birth_month:02d}{birth_year}",
    "{last_name}{birthdate:02d}{birth_month:02d}{birth_year}",
    "{first_name}{birthdate:02d}{birth_month:02d}{birth_year_short}",
    "{last_name}{birthdate:02d}{birth_month:02d}{birth_year_short}",
    
    # With Pet Name
    "{first_name}{pet_name}",
    "{last_name}{pet_name}",
    "{pet_name}{first_name}",
    "{pet_name}{last_name}",
    "{pet_name}{birthdate:02d}{birth_month:02d}",
    "{pet_name}{birth_year}",
    "{pet_name}{birth_year_short}",
    "{pet_name}_{first_name}",
    "{pet_name}_{last_name}",
    "{first_name}_{pet_name}",
    "{last_name}_{pet_name}",
    
    # Favorite Items
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
    "{first_name}{favorite_number}",
    "{last_name}{favorite_number}",
    "{first_name}{gamer_tag}",
    "{last_name}{gamer_tag}",
    "{gamer_tag}{first_name}",
    "{gamer_tag}{last_name}",
    "{gamer_tag}{birth_year}",
    "{gamer_tag}{birth_year_short}",
    
    # With names and date formats
    "{first_name}{birthdate_str}{birth_month_str}",
    "{last_name}{birthdate_str}{birth_month_str}",
    "{first_name}{last_name}{birthdate_str}{birth_month_str}",
    "{last_name}{first_name}{birthdate_str}{birth_month_str}",
    
    # Shortened name variants
    "{first_name_short_3}{last_name_short_3}{birth_year}",
    "{first_name_short_3}{last_name_short_3}{birth_year_short}",
    "{first_name_short_2}{last_name_short_2}{birth_year}",
    "{first_name_short_2}{last_name_short_2}{birth_year_short}",
    "{first_name_short_4}{last_name_short_4}{birth_year}",
    "{first_name_short_4}{last_name_short_4}{birth_year_short}",
    "{first_name_short_3}_{last_name_short_3}",
    "{first_name_short_2}_{last_name_short_2}",
    "{first_name_short_4}_{last_name_short_4}",
    
    # Initial variants
    "{first_name_initial}{last_name_initial}{birth_year}",
    "{first_name_initial}{last_name_initial}{birth_year_short}",
    "{first_name_initial}{last_name}",
    "{first_name}{last_name_initial}",
    "{first_name_initial}{last_name}{birthdate_str}{birth_month_str}",
    "{last_name_initial}{first_name}{birthdate_str}{birth_month_str}",
    "{first_name}{last_name_initial}{birthdate_str}{birth_month_str}",
    "{last_name}{first_name_initial}{birthdate_str}{birth_month_str}",
    "{first_name_initial}{last_name_initial}_{birth_year}",
    "{first_name_initial}{last_name_initial}_{birth_year_short}",
    "{first_name_initial}{last_name_initial}{birthdate:02d}{birth_month:02d}",
    
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
    "{first_name}#{last_name}",
    "{last_name}#{first_name}",
    "{first_name}#{birth_year}",
    "{last_name}#{birth_year}",
    "{first_name}*{last_name}",
    "{last_name}*{first_name}",
    "{first_name}*{birth_year}",
    "{last_name}*{birth_year}",
    "{first_name}${last_name}",
    "{last_name}${first_name}",
    "{first_name}${birth_year}",
    "{last_name}${birth_year}",
    "{first_name}&{last_name}",
    "{last_name}&{first_name}",
    "{first_name}&{birth_year}",
    "{last_name}&{birth_year}",
    
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
    "{father_name}_{birth_year}",
    "{mother_name}_{birth_year}",
    "{spouse_name}_{birth_year}",
    "{child_name}_{birth_year}",
    "{father_name}{birth_year_short}",
    "{mother_name}{birth_year_short}",
    "{spouse_name}{birth_year_short}",
    "{child_name}{birth_year_short}",
    
    # With Family Member Initials
    "{father_name_initial}{mother_name_initial}{spouse_name_initial}",
    "{father_name_initial}{mother_name_initial}{child_name_initial}",
    "{father_name_initial}{mother_name_initial}{pet_name_initial}",
    "{father_name_initial}{mother_name_initial}{first_name_initial}",
    "{father_name_initial}{mother_name_initial}{last_name_initial}",
    "{father_name_initial}{mother_name_initial}{birth_year}",
    "{father_name_initial}{mother_name_initial}{birth_year_short}",
    "{father_name_initial}{mother_name_initial}{birthdate:02d}{birth_month:02d}",
    
    # Creative Combinations
    "{first_name}{mother_name}{pet_name}",
    "{last_name}{father_name}{spouse_name}",
    "{first_name}{mother_name}{birth_year}",
    "{last_name}{father_name}{birth_year}",
    "{pet_name}{first_name}{birthdate_str}{birth_month_str}",
    "{spouse_name}{last_name}{birth_year}",
    "{child_name}{first_name}{birth_year}",
    "{first_name}{last_name}{pet_name}{birth_year}",
    "{first_name}{mother_name}{birth_year_short}",
    "{last_name}{father_name}{birth_year_short}",
    "{pet_name}_{first_name}_{birth_year}",
    "{spouse_name}_{last_name}_{birth_year}",
    "{first_name}_{pet_name}_{birth_year}",
    "{last_name}_{spouse_name}_{birth_year}",
    
    # With Phone Number Parts
    "{first_name}{phone_last4}",
    "{last_name}{phone_last4}",
    "{first_name}_{phone_last4}",
    "{last_name}_{phone_last4}",
    "{phone_last4}_{first_name}",
    "{phone_last4}_{last_name}",
    "{first_name}{phone_first3}{phone_last4}",
    "{last_name}{phone_first3}{phone_last4}",
    "{phone_first3}{first_name}{phone_last4}",
    "{phone_first3}{last_name}{phone_last4}",
    "{first_name_initial}{last_name_initial}{phone_last4}",
    "{first_name}{phone_middle}{birth_year_short}",
    "{last_name}{phone_middle}{birth_year_short}",
    
    # With Location Information
    "{first_name}{residence_short}",
    "{last_name}{residence_short}",
    "{first_name}_{residence_short}",
    "{last_name}_{residence_short}",
    "{residence_short}_{first_name}",
    "{residence_short}_{last_name}",
    "{first_name}{birthplace_short}",
    "{last_name}{birthplace_short}",
    "{first_name}_{birthplace_short}",
    "{last_name}_{birthplace_short}",
    "{birthplace_short}_{first_name}",
    "{birthplace_short}_{last_name}",
    "{residence_short}{birth_year}",
    "{residence_short}{birth_year_short}",
    "{birthplace_short}{birth_year}",
    "{birthplace_short}{birth_year_short}",
    
    # With Social Media IDs
    "{first_name}{social_id}",
    "{last_name}{social_id}",
    "{social_id}{first_name}",
    "{social_id}{last_name}",
    "{social_id}{birth_year}",
    "{social_id}{birth_year_short}",
    "{social_id}_{first_name}",
    "{social_id}_{last_name}",
    "{first_name}_{social_id}",
    "{last_name}_{social_id}",
    
    # With Device Names
    "{first_name}{device_name}",
    "{last_name}{device_name}",
    "{device_name}{first_name}",
    "{device_name}{last_name}",
    "{device_name}{birth_year}",
    "{device_name}{birth_year_short}",
    "{device_name}_{first_name}",
    "{device_name}_{last_name}",
    "{first_name}_{device_name}",
    "{last_name}_{device_name}",
    
    # With Simple Sequences
    "{first_name}123456",
    "{last_name}123456",
    "123456{first_name}",
    "123456{last_name}",
    "{first_name}123",
    "{last_name}123",
    "123{first_name}",
    "123{last_name}",
    "{first_name}12345",
    "{last_name}12345",
    "12345{first_name}",
    "12345{last_name}",
    "{first_name}1234",
    "{last_name}1234",
    "1234{first_name}",
    "1234{last_name}",
    "{birth_year}abcdef",
    "abcdef{birth_year}",
    "{first_name}password",
    "password{first_name}",
    "{last_name}password",
    "password{last_name}",
    "{first_name}qwerty",
    "{last_name}qwerty",
    "qwerty{first_name}",
    "qwerty{last_name}",
    "{first_name}abc123",
    "{last_name}abc123",
    "abc123{first_name}",
    "abc123{last_name}",
    
    # Common Words and Combinations
    "{first_name}welcome",
    "{last_name}welcome",
    "welcome{first_name}",
    "welcome{last_name}",
    "{first_name}dragon",
    "{last_name}dragon",
    "dragon{first_name}",
    "dragon{last_name}",
    "{first_name}monkey",
    "{last_name}monkey",
    "monkey{first_name}",
    "monkey{last_name}",
    "{first_name}football",
    "{last_name}football",
    "football{first_name}",
    "football{last_name}",
    "{first_name}baseball",
    "{last_name}baseball",
    "baseball{first_name}",
    "baseball{last_name}",
    "{first_name}superman",
    "{last_name}superman",
    "superman{first_name}",
    "superman{last_name}",
    "{first_name}batman",
    "{last_name}batman",
    "batman{first_name}",
    "batman{last_name}",
    
    # Birthdate Variations
    "{birth_month_str}/{birthdate_str}/{birth_year}",
    "{birthdate_str}-{birth_month_str}-{birth_year}",
    "{birth_year}-{birth_month_str}-{birthdate_str}",
    "{first_name}{birth_month_str}/{birthdate_str}",
    "{last_name}{birth_year}-{birth_month_str}",
    "{birth_year}{first_name}{last_name}",
    "{birth_month_str}{birthdate_str}{birth_year}",
    "{birth_year}{birth_month_str}{birthdate_str}",
    "{birthdate_str}{birth_month_str}-{birth_year}",
    "{birth_month_str}-{birthdate_str}-{birth_year}",
    "{birth_year}{birth_month_str}-{birthdate_str}",
    "{first_name}{birth_month_str}{birthdate_str}{birth_year_short}",
    "{last_name}{birth_month_str}{birthdate_str}{birth_year_short}",
    
    # Reversed Strings
    "{first_name_rev}{birth_year}",
    "{last_name_rev}{birth_year}",
    "{first_name}{last_name_rev}{birth_year}",
    "{first_name_rev}{last_name}{birth_year}",
    "{birth_year_rev}{first_name}",
    "{birth_year_rev}{last_name}",
    "{first_name}{birth_year_rev}{last_name}",
    "{first_name_rev}{birth_year_short}",
    "{last_name_rev}{birth_year_short}",
    "{first_name}{last_name_rev}{birth_year_short}",
    "{first_name_rev}{last_name}{birth_year_short}",
    "{birth_year_rev}{first_name_rev}",
    "{birth_year_rev}{last_name_rev}",
    "{first_name_rev}_{last_name_rev}",
    "{first_name_rev}_{last_name}",
    "{first_name}_{last_name_rev}",
    
    # With Special Characters (Middle)
    "{first_name}!{last_name}{birth_year}",
    "{last_name}@{first_name}{birth_year}",
    "{birth_year}#{first_name}{last_name}",
    "{first_name}{last_name}${birthdate_str}{birth_month_str}",
    "{birthdate_str}{birth_month_str}%{first_name}{last_name}",
    "{first_name}!{last_name}",
    "{last_name}@{first_name}",
    "{first_name}#{birth_year}",
    "{last_name}${birth_year}",
    "{birth_year}%{first_name}",
    "{birth_year}^{last_name}",
    "{first_name}&{last_name}{birth_year}",
    "{last_name}*{first_name}{birth_year}",
    "{birth_year}({first_name}{last_name}",
    "{first_name}{last_name}){birthdate_str}{birth_month_str}",
    "{birthdate_str}{birth_month_str}-{first_name}{last_name}",
    "{first_name}+{last_name}",
    "{last_name}={first_name}",
    "{first_name}//{birth_year}",
    "{last_name}\\{birth_year}",
    "{birth_year}|{first_name}",
    "{birth_year}~{last_name}",
    
    # Extended Number Variations
    "{first_name}00",
    "{last_name}00",
    "{first_name}01",
    "{last_name}01",
    "{first_name}02",
    "{last_name}02",
    "{first_name}69",
    "{last_name}69",
    "{first_name}007",
    "{last_name}007",
    "{first_name}777",
    "{last_name}777",
    "{first_name}111",
    "{last_name}111",
    "{first_name}222",
    "{last_name}222",
    "{first_name}333",
    "{last_name}333",
    "{first_name}666",
    "{last_name}666",
    "{first_name}999",
    "{last_name}999",
    "{first_name}1234567",
    "{last_name}1234567",
    "{first_name}7654321",
    "{last_name}7654321",
    "{first_name}11111",
    "{last_name}11111",
    "{first_name}22222",
    "{last_name}22222",
    "{first_name}55555",
    "{last_name}55555",
    "{first_name}0000",
    "{last_name}0000",
    "{first_name}0123",
    "{last_name}0123",
    "{first_name}6789",
    "{last_name}6789",
    
    # Special Combinations
    "{first_name_initial}{last_name}{phone_last4}",
    "{last_name_initial}{first_name}{phone_last4}",
    "{first_name}{last_name_initial}{birth_year}",
    "{last_name}{first_name_initial}{birth_year}",
    "{first_name_initial}{last_name_initial}{birth_year}{phone_last4}",
    "{father_name_initial}{mother_name_initial}{first_name_initial}{last_name_initial}",
    "{first_name_short_2}{last_name_short_2}{birth_month_str}{birthdate_str}",
    "{birthplace_short}{residence_short}{birth_year_short}",
    "{device_name}{birth_year}{phone_last4}",
    "{social_id}{birth_year}{phone_last4}",
    "{pet_name_initial}{first_name_initial}{last_name_initial}{birth_year_short}",
    "{father_name_short_3}{mother_name_initial}{birth_year_short}",
    "{first_name}_{last_name}_{birth_year}",
    "{first_name}.{last_name}.{birth_year}",
    "{first_name}-{last_name}-{birth_year}",
    "{favorite_band}{birth_year}",
    "{favorite_song}{birth_year}",
    "{favorite_movie}{birth_year}",
    "{favorite_number}{first_name}{birth_year}",
    "{gamer_tag}{phone_last4}",
    "{social_id}{phone_last4}",
    "{pet_name}_{birth_year}_{phone_last4}",
    
    # Very Common Patterns (Based on Real Leaks)
    "password123",
    "admin123",
    "welcome123",
    "letmein123",
    "123456789",
    "12345678",
    "qwerty123",
    "abc123xyz",
    "1q2w3e4r",
    "qazwsx123",
    "password1!",
    "P@ssw0rd",
    "passw0rd",
    "Football123",
    "Baseball123",
    "Princess123",
    "Superman123",
    "Batman123",
    "Trustno1",
    "iloveyou123",
    "sunshine123",
    "monkey123",
    "dragon123",
    "master123",
    "login123",
    "solo123",
    "access123",
    "flower123",
    "forever123",
    "hunter123",
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
    data["birth_year_short"] = str(data["birth_year"])[-2:]
    data["birth_year_last"] = str(data["birth_year"])[-1]
    data["birth_year_first"] = str(data["birth_year"])[0]
    data["birth_year_middle"] = str(data["birth_year"])[1:3]
    # Substring fields
    data["first_name_short_3"] = data["first_name"][:3] if data["first_name"] else ""
    data["last_name_short_3"] = data["last_name"][:3] if data["last_name"] else ""
    data["first_name_short_2"] = data["first_name"][:2] if data["first_name"] else ""
    data["last_name_short_2"] = data["last_name"][:2] if data["last_name"] else ""
    data["first_name_short_4"] = data["first_name"][:4] if data["first_name"] and len(data["first_name"]) >= 4 else data["first_name"]
    data["last_name_short_4"] = data["last_name"][:4] if data["last_name"] and len(data["last_name"]) >= 4 else data["last_name"]
    data["first_name_middle"] = data["first_name"][1:-1] if data["first_name"] and len(data["first_name"]) >= 3 else ""
    data["last_name_middle"] = data["last_name"][1:-1] if data["last_name"] and len(data["last_name"]) >= 3 else ""
    # Initials
    data["first_name_initial"] = data["first_name"][0].upper() if data["first_name"] else ""
    data["last_name_initial"] = data["last_name"][0].upper() if data["last_name"] else ""
    data["father_name_initial"] = data["father_name"][0].upper() if data.get("father_name") else ""
    data["mother_name_initial"] = data["mother_name"][0].upper() if data.get("mother_name") else ""
    data["spouse_name_initial"] = data["spouse_name"][0].upper() if data.get("spouse_name") else ""
    data["child_name_initial"] = data["child_name"][0].upper() if data.get("child_name") else ""
    data["pet_name_initial"] = data["pet_name"][0].upper() if data.get("pet_name") else ""
    # Device names and social media
    data["device_name"] = data["device_names"][0] if data["device_names"] else ""
    data["social_id"] = data.get("instagram_id", "") or data.get("facebook_id", "") or data.get("twitter_id", "")
    # Location derived
    data["residence_short"] = data["residence"][:4] if data["residence"] else ""
    data["birthplace_short"] = data["birthplace"][:4] if data["birthplace"] else ""
    # Phone parts
    if data["phone_number"]:
        if len(data["phone_number"]) >= 10:
            data["phone_last4"] = data["phone_number"][-4:]
            data["phone_first3"] = data["phone_number"][:3]
            data["phone_middle"] = data["phone_number"][3:6]
        else:
            data["phone_last4"] = data["phone_number"]
            data["phone_first3"] = data["phone_number"]
            data["phone_middle"] = data["phone_number"]
    else:
        data["phone_last4"] = ""
        data["phone_first3"] = ""
        data["phone_middle"] = ""
    # Reversed strings
    data["first_name_rev"] = data["first_name"][::-1] if data["first_name"] else ""
    data["last_name_rev"] = data["last_name"][::-1] if data["last_name"] else ""
    data["birth_year_rev"] = str(data["birth_year"])[::-1]
    # If a nickname field exists, ensure it is in the data dictionary.
    if "nickname" not in data or data["nickname"] is None:
        data["nickname"] = ""
    # Favorite fields (ensure not None)
    data["favorite_movie"] = data.get("favorite_movie", "") or ""
    data["favorite_book"] = data.get("favorite_book", "") or ""
    data["favorite_song"] = data.get("favorite_song", "") or ""
    data["favorite_band"] = data.get("favorite_band", "") or ""
    data["favorite_sport"] = data.get("favorite_sport", "") or ""
    data["favorite_number"] = data.get("favorite_number", "") or ""
    data["favorite_celebrity"] = data.get("favorite_celebrity", "") or ""
    # lowercase variants
    data["first_name_lower"] = data["first_name"].lower() if data["first_name"] else ""
    data["last_name_lower"] = data["last_name"].lower() if data["last_name"] else ""
    # uppercase variants
    data["first_name_upper"] = data["first_name"].upper() if data["first_name"] else ""
    data["last_name_upper"] = data["last_name"].upper() if data["last_name"] else ""
    # Capitalize first letter
    data["first_name_cap"] = data["first_name"].capitalize() if data["first_name"] else ""
    data["last_name_cap"] = data["last_name"].capitalize() if data["last_name"] else ""
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

# Additional transformation functions
def append_year(pwd: str) -> str:
    return f"{pwd}2023"

def append_year_short(pwd: str) -> str:
    return f"{pwd}23"

def append_at(pwd: str) -> str:
    return f"{pwd}@"

def append_hash(pwd: str) -> str:
    return f"{pwd}#"

def append_dollar(pwd: str) -> str:
    return f"{pwd}$"

def append_1(pwd: str) -> str:
    return f"{pwd}1"

def append_12(pwd: str) -> str:
    return f"{pwd}12"

def append_1234(pwd: str) -> str:
    return f"{pwd}1234"

def append_12345(pwd: str) -> str:
    return f"{pwd}12345"

def append_321(pwd: str) -> str:
    return f"{pwd}321"

def append_0(pwd: str) -> str:
    return f"{pwd}0"

def append_00(pwd: str) -> str:
    return f"{pwd}00"

def append_question(pwd: str) -> str:
    return f"{pwd}?"

def prepend_at(pwd: str) -> str:
    return f"@{pwd}"

def capitalize_first(pwd: str) -> str:
    if not pwd:
        return pwd
    return pwd[0].upper() + pwd[1:] if len(pwd) > 1 else pwd.upper()

def capitalize_all(pwd: str) -> str:
    return pwd.upper()

def lowercase_all(pwd: str) -> str:
    return pwd.lower()

def double_last_char(pwd: str) -> str:
    if not pwd:
        return pwd
    return pwd + pwd[-1]

def between_dots(pwd: str) -> str:
    return f".{pwd}."

def between_underscores(pwd: str) -> str:
    return f"_{pwd}_"

def between_asterisks(pwd: str) -> str:
    return f"*{pwd}*"

def substitute_a_with_4(pwd: str) -> str:
    return pwd.replace('a', '4').replace('A', '4')

def substitute_e_with_3(pwd: str) -> str:
    return pwd.replace('e', '3').replace('E', '3')

def substitute_i_with_1(pwd: str) -> str:
    return pwd.replace('i', '1').replace('I', '1')

def substitute_o_with_0(pwd: str) -> str:
    return pwd.replace('o', '0').replace('O', '0')

def substitute_s_with_5(pwd: str) -> str:
    return pwd.replace('s', '5').replace('S', '5')

def advanced_leetspeak(pwd: str) -> str:
    mapping = str.maketrans("aAeEiIoOsStTbBlL", "443311005577881")
    return pwd.translate(mapping)

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
    append_year,
    append_year_short,
    append_at,
    append_hash,
    append_dollar,
    append_1,
    append_12,
    append_1234,
    append_12345,
    append_321,
    append_0,
    append_00,
    append_question,
    prepend_at,
    capitalize_first,
    capitalize_all,
    lowercase_all,
    double_last_char,
    between_dots,
    between_underscores,
    between_asterisks,
    substitute_a_with_4,
    substitute_e_with_3,
    substitute_i_with_1,
    substitute_o_with_0,
    substitute_s_with_5,
    advanced_leetspeak,
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