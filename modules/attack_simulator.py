#!/usr/bin/env python3
"""
attack_simulator.py

This module provides attack simulation features and password export formats
compatible with various password cracking tools.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import hashlib
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
import click
from datetime import datetime

# -----------------------------------------------------------------------------
# Hash Generation Functions
# -----------------------------------------------------------------------------

def generate_hashes(password: str) -> Dict[str, str]:
    """
    Generate various hash formats for a password.
    
    Args:
        password: The password to hash
        
    Returns:
        Dict: Dictionary of hash formats and their values
    """
    hashes = {
        "md5": hashlib.md5(password.encode()).hexdigest(),
        "sha1": hashlib.sha1(password.encode()).hexdigest(),
        "sha256": hashlib.sha256(password.encode()).hexdigest(),
        "sha512": hashlib.sha512(password.encode()).hexdigest(),
        "ntlm": hashlib.new('md4', password.encode('utf-16le')).hexdigest(),
        "lm": hashlib.new('md4', password.encode('utf-16le')).hexdigest()[:32],
    }
    return hashes

# -----------------------------------------------------------------------------
# Export Format Functions
# -----------------------------------------------------------------------------

def export_hashcat_format(passwords: List[str], output_file: str, hash_type: str = "sha256") -> None:
    """
    Export passwords in Hashcat format.
    
    Args:
        passwords: List of passwords to export
        output_file: Path to save the output file
        hash_type: Type of hash to generate (default: sha256)
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for password in passwords:
            hashes = generate_hashes(password)
            if hash_type in hashes:
                f.write(f"{hashes[hash_type]}:{password}\n")

def export_john_format(passwords: List[str], output_file: str, hash_type: str = "sha256") -> None:
    """
    Export passwords in John the Ripper format.
    
    Args:
        passwords: List of passwords to export
        output_file: Path to save the output file
        hash_type: Type of hash to generate (default: sha256)
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for password in passwords:
            hashes = generate_hashes(password)
            if hash_type in hashes:
                if hash_type == "sha256":
                    f.write(f"$SHA256${hashes[hash_type]}:{password}\n")
                elif hash_type == "ntlm":
                    f.write(f"{hashes[hash_type]}:{password}\n")

def export_plain_wordlist(passwords: List[str], output_file: str) -> None:
    """
    Export passwords as a plain wordlist.
    
    Args:
        passwords: List of passwords to export
        output_file: Path to save the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for password in passwords:
            f.write(f"{password}\n")

# -----------------------------------------------------------------------------
# Attack Simulation Functions
# -----------------------------------------------------------------------------

def simulate_brute_force(password: str, charset: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> Dict[str, Any]:
    """
    Simulate a brute force attack on a password.
    
    Args:
        password: The password to simulate attack on
        charset: Character set to use for simulation
        
    Returns:
        Dict: Simulation results including time and attempts
    """
    start_time = time.time()
    attempts = 0
    max_attempts = 1000000  # Limit for simulation
    
    for length in range(1, len(password) + 1):
        for attempt in range(len(charset) ** length):
            attempts += 1
            if attempts >= max_attempts:
                break
                
    end_time = time.time()
    duration = end_time - start_time
    
    return {
        "password": password,
        "attempts": attempts,
        "duration": duration,
        "attempts_per_second": attempts / duration if duration > 0 else 0
    }

def simulate_dictionary_attack(password: str, wordlist: List[str]) -> Dict[str, Any]:
    """
    Simulate a dictionary attack on a password.
    
    Args:
        password: The password to simulate attack on
        wordlist: List of words to try
        
    Returns:
        Dict: Simulation results including time and attempts
    """
    start_time = time.time()
    attempts = 0
    
    for word in wordlist:
        attempts += 1
        if word == password:
            break
            
    end_time = time.time()
    duration = end_time - start_time
    
    return {
        "password": password,
        "attempts": attempts,
        "duration": duration,
        "attempts_per_second": attempts / duration if duration > 0 else 0,
        "found": attempts <= len(wordlist)
    }

# -----------------------------------------------------------------------------
# CLI Interface
# -----------------------------------------------------------------------------

@click.group()
def cli():
    """DarkForge Attack Simulator and Password Export Tool"""
    pass

@cli.command()
@click.option(
    "--password-file",
    required=True,
    help="File containing passwords to process"
)
@click.option(
    "--output-dir",
    default="./attack_results",
    help="Directory to save results"
)
@click.option(
    "--format",
    type=click.Choice(["hashcat", "john", "plain"]),
    default="plain",
    help="Export format"
)
@click.option(
    "--hash-type",
    type=click.Choice(["md5", "sha1", "sha256", "sha512", "ntlm", "lm"]),
    default="sha256",
    help="Hash type for export"
)
def export(password_file, output_dir, format, hash_type):
    """Export passwords in various formats."""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Read passwords
        with open(password_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export based on format
        if format == "hashcat":
            output_file = output_path / f"hashcat_{timestamp}.txt"
            export_hashcat_format(passwords, output_file, hash_type)
        elif format == "john":
            output_file = output_path / f"john_{timestamp}.txt"
            export_john_format(passwords, output_file, hash_type)
        else:
            output_file = output_path / f"wordlist_{timestamp}.txt"
            export_plain_wordlist(passwords, output_file)
        
        click.echo(f"Exported {len(passwords)} passwords to {output_file}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise

@cli.command()
@click.option(
    "--password",
    required=True,
    help="Password to simulate attack on"
)
@click.option(
    "--attack-type",
    type=click.Choice(["brute", "dictionary"]),
    default="brute",
    help="Type of attack to simulate"
)
@click.option(
    "--wordlist",
    help="Path to wordlist file for dictionary attack"
)
def simulate(password, attack_type, wordlist):
    """Simulate password attacks."""
    try:
        if attack_type == "brute":
            results = simulate_brute_force(password)
            click.echo("\nBrute Force Attack Simulation Results:")
        else:
            if not wordlist:
                raise click.UsageError("Wordlist file required for dictionary attack")
            with open(wordlist, 'r', encoding='utf-8') as f:
                wordlist_data = [line.strip() for line in f if line.strip()]
            results = simulate_dictionary_attack(password, wordlist_data)
            click.echo("\nDictionary Attack Simulation Results:")
        
        click.echo(f"Password: {results['password']}")
        click.echo(f"Attempts: {results['attempts']:,}")
        click.echo(f"Duration: {results['duration']:.2f} seconds")
        click.echo(f"Attempts per second: {results['attempts_per_second']:.2f}")
        if 'found' in results:
            click.echo(f"Password found: {'Yes' if results['found'] else 'No'}")
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise

if __name__ == "__main__":
    cli() 