#!/usr/bin/env python3
"""
test_pattern_generator.py

Tests for the pattern_generator module.

Author: Shivendra Chauhan
Date: 23rd March 2025
"""

import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow imports from the darkforge package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from darkforge.modules.data_input.collector import UserProfile
from darkforge.modules.pattern_generator import generate_passwords, generate_base_passwords


class TestPatternGenerator(unittest.TestCase):
    """Test cases for the pattern_generator module."""

    def setUp(self):
        """Set up a sample UserProfile for testing."""
        self.sample_profile = UserProfile(
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
            nickname="Shivi",
        )

    def test_import_works(self):
        """Test that the UserProfile import works correctly."""
        self.assertIsInstance(self.sample_profile, UserProfile)
        
    def test_generate_base_passwords(self):
        """Test that base passwords can be generated."""
        base_passwords = generate_base_passwords(self.sample_profile)
        self.assertIsInstance(base_passwords, list)
        self.assertGreater(len(base_passwords), 0)
        
    def test_generate_passwords(self):
        """Test that passwords can be generated."""
        passwords = generate_passwords(self.sample_profile)
        self.assertIsInstance(passwords, list)
        self.assertGreater(len(passwords), 0)
        # Check that transformations were applied
        self.assertGreater(len(passwords), len(generate_base_passwords(self.sample_profile)))


if __name__ == "__main__":
    unittest.main()
