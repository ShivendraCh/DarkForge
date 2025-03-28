#!/usr/bin/env python3
"""
database.py

This module handles database operations for DarkForge, storing password analysis results,
user profiles, and attack simulations.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# ASCII Art for Database Module
DB_ART = """
██╗  ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██████╗ ███████╗
██║ ██╔╝██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔════╝
█████╔╝ ██║   ██║██████╔╝█████╔╝ █████╗  ██████╔╝█████╗  
██╔═██╗ ██║   ██║██╔══██╗██╔═██╗ ██╔══╝  ██╔══██╗██╔══╝  
██║  ██╗╚██████╔╝██║  ██║██║  ██║███████╗██║  ██║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
"""

class Database:
    def __init__(self, db_path: str = "darkforge.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self) -> None:
        """Create necessary database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create user profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    birth_date TEXT,
                    phone TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create password analysis results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password TEXT,
                    entropy REAL,
                    strength TEXT,
                    score INTEGER,
                    length INTEGER,
                    patterns TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create attack simulation results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attack_simulations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password TEXT,
                    attack_type TEXT,
                    attempts INTEGER,
                    duration REAL,
                    attempts_per_second REAL,
                    found BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create password generation history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_generation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_profile_id INTEGER,
                    total_passwords INTEGER,
                    output_file TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_profile_id) REFERENCES user_profiles(id)
                )
            """)
            
            conn.commit()
    
    def save_user_profile(self, profile_data: Dict[str, Any]) -> int:
        """Save a user profile and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_profiles (name, email, birth_date, phone, address)
                VALUES (?, ?, ?, ?, ?)
            """, (
                profile_data.get("name"),
                profile_data.get("email"),
                profile_data.get("birth_date"),
                profile_data.get("phone"),
                profile_data.get("address")
            ))
            return cursor.lastrowid
    
    def save_password_analysis(self, analysis_data: Dict[str, Any]) -> None:
        """Save password analysis results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO password_analysis 
                (password, entropy, strength, score, length, patterns)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                analysis_data["password"],
                analysis_data["entropy"],
                analysis_data["strength"],
                analysis_data["score"],
                analysis_data["length"],
                json.dumps(analysis_data["patterns"])
            ))
    
    def save_attack_simulation(self, simulation_data: Dict[str, Any]) -> None:
        """Save attack simulation results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attack_simulations 
                (password, attack_type, attempts, duration, attempts_per_second, found)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                simulation_data["password"],
                simulation_data["attack_type"],
                simulation_data["attempts"],
                simulation_data["duration"],
                simulation_data["attempts_per_second"],
                simulation_data.get("found", False)
            ))
    
    def save_password_generation(self, user_profile_id: int, total_passwords: int, output_file: str) -> None:
        """Save password generation history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO password_generation (user_profile_id, total_passwords, output_file)
                VALUES (?, ?, ?)
            """, (user_profile_id, total_passwords, output_file))
    
    def get_user_profile(self, profile_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a user profile by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (profile_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "birth_date": row[3],
                    "phone": row[4],
                    "address": row[5],
                    "created_at": row[6]
                }
            return None
    
    def get_password_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent password analysis results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM password_analysis 
                ORDER BY created_at DESC LIMIT ?
            """, (limit,))
            return [{
                "id": row[0],
                "password": row[1],
                "entropy": row[2],
                "strength": row[3],
                "score": row[4],
                "length": row[5],
                "patterns": json.loads(row[6]),
                "created_at": row[7]
            } for row in cursor.fetchall()]
    
    def get_attack_simulation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent attack simulation results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM attack_simulations 
                ORDER BY created_at DESC LIMIT ?
            """, (limit,))
            return [{
                "id": row[0],
                "password": row[1],
                "attack_type": row[2],
                "attempts": row[3],
                "duration": row[4],
                "attempts_per_second": row[5],
                "found": row[6],
                "created_at": row[7]
            } for row in cursor.fetchall()]
    
    def get_password_generation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent password generation history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pg.*, up.name as user_name 
                FROM password_generation pg
                JOIN user_profiles up ON pg.user_profile_id = up.id
                ORDER BY pg.created_at DESC LIMIT ?
            """, (limit,))
            return [{
                "id": row[0],
                "user_profile_id": row[1],
                "total_passwords": row[2],
                "output_file": row[3],
                "created_at": row[4],
                "user_name": row[5]
            } for row in cursor.fetchall()]
