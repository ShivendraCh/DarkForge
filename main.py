#!/usr/bin/env python3
"""
main.py

Main entry point for the DarkForge toolkit. Provides a command-line interface for
password generation based on user profile data.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import os
import sys
import json
import click
import logging
from pathlib import Path

# Use relative imports from the darkforge package
from modules.data_input.collector import UserProfile, get_user_profile
from modules.pattern_generator import generate_passwords
from modules.password_analyzer import analyze_password_file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """DarkForge - Password Analysis and Generation Toolkit"""
    pass

@cli.command()
@click.option(
    "--source",
    default="cli",
    type=click.Choice(["cli", "file"]),
    help="Data source: 'cli' for interactive input or 'file' for JSON file input"
)
@click.option(
    "--file",
    "file_path",
    default=None,
    help="Path to the JSON file (required if --source is 'file')."
)
@click.option(
    "--output",
    "output_file",
    default="passwords.txt",
    help="Path to the output file for password candidates."
)
def generate(source, file_path, output_file):
    """Generate password candidates based on user profile data."""
    try:
        # Collect user data
        click.echo("Collecting user profile data...")
        raw_profile_data = get_user_profile(source=source, file_path=file_path)
        profile = UserProfile(**raw_profile_data)
        
        # Generate passwords
        click.echo("Generating password candidates...")
        passwords = generate_passwords(profile)
        
        # Save passwords to file
        output_path = Path(output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            for password in passwords:
                f.write(f"{password}\n")
        
        click.echo(f"Generated {len(passwords)} password candidates.")
        click.echo(f"Saved to: {output_path.absolute()}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option(
    "--file",
    "file_path",
    required=True,
    help="Path to save the user profile JSON file."
)
def collect(file_path):
    """Collect and save user profile data to a JSON file."""
    try:
        # Collect user data
        click.echo("Collecting user profile data...")
        raw_profile_data = get_user_profile(source="cli")
        profile = UserProfile(**raw_profile_data)
        
        # Save to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(raw_profile_data, f, indent=2)
        
        click.echo(f"User profile saved to: {file_path}")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option(
    "--password-file",
    required=True,
    help="File containing passwords to analyze (one per line)"
)
@click.option(
    "--output-dir",
    default="./analysis_results",
    help="Directory to save analysis results"
)
@click.option(
    "--no-visuals",
    is_flag=True,
    help="Disable visualization generation"
)
def analyze(password_file, output_dir, no_visuals):
    """Analyze passwords and generate reports."""
    try:
        click.echo("Analyzing passwords...")
        analysis_results = analyze_password_file(
            password_file=password_file,
            output_dir=output_dir,
            generate_visuals=not no_visuals
        )
        
        click.echo(f"Analysis complete!")
        click.echo(f"Total passwords analyzed: {analysis_results['total_passwords']}")
        click.echo(f"Average password length: {analysis_results['length_stats']['avg']:.2f}")
        click.echo(f"Report saved to: {output_dir}/password_analysis_report.json")
        
        if not no_visuals:
            click.echo(f"Visualizations saved to: {output_dir}/visualizations/")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    cli() 