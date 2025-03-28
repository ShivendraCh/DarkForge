# DarkForge Password Toolkit

DarkForge is a comprehensive password analysis and generation toolkit designed for security research and penetration testing. It enables security professionals to test password security by generating potential passwords based on personal information patterns.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Usage Guide](#usage-guide)
  - [Interactive Menu](#interactive-menu)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [Working with User Profiles](#working-with-user-profiles)
- [Password Generation](#password-generation)
- [Password Analysis](#password-analysis)
- [Export Formats](#export-formats)
- [Technical Details](#technical-details)
- [Legal and Ethical Considerations](#legal-and-ethical-considerations)
- [Troubleshooting](#troubleshooting)
- [Future Development](#future-development)
- [Contributing](#contributing)
- [License](#license)

## Overview

DarkForge leverages OSINT (Open Source Intelligence) data to create targeted password candidates based on predictable human patterns. The tool models the ways people often create passwords using personal information like names, dates, pet names, and other personal details.

**Security Research Purpose**: This tool is designed for legitimate security testing, helping organizations identify vulnerable passwords before malicious actors can exploit them.

## Key Features

- **User Profile Collection**: Gather comprehensive profiles either interactively or from templates
- **Advanced Pattern Generation**: Over 700+ password patterns based on real-world password creation habits
- **Password Transformation**: Apply common character substitutions and variations
- **Strength Analysis**: Assess password strength and identify pattern weaknesses
- **Format Export**: Export passwords in formats compatible with Hashcat and John the Ripper
- **Intuitive Interface**: Clean menu-driven interface with color-coded sections
- **History Tracking**: Maintain history of analyses and generations for reference

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/darkforge.git
   cd darkforge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python main.py
   ```

## Directory Structure

```
darkforge/
├── main.py                  # Main entry point with interactive menu
├── requirements.txt         # Python dependencies
├── config/                  # Configuration files
│   └── settings.json        # Application settings
├── modules/                 # Core functionality
│   ├── data_input/          # User data collection
│   │   └── collector.py     # Profile collection functionality
│   ├── pattern_generator.py # Password generation algorithms
│   ├── password_analyzer.py # Strength assessment tools
│   ├── attack_simulator.py  # Export and simulation functionality
│   └── database.py          # Database operations
├── output/                  # Generated output storage
│   ├── txt/                 # Plain text password lists
│   ├── hashcat/             # Hashcat formatted exports
│   ├── john/                # John the Ripper formatted exports
│   └── analysis/            # Analysis reports
└── templates/               # User profile templates
    └── example_profile.json # Example profile for testing
```

## Usage Guide

### Interactive Menu

DarkForge features a user-friendly menu system that can be accessed by running:

```bash
python main.py
```

The main menu provides five primary options:

1. **Generate Passwords**: Create passwords based on user profiles
2. **Analyze Passwords**: Assess strength and patterns in passwords
3. **Export Formats**: Convert passwords to various formats
4. **View History**: Access past operations and results
5. **Help**: Get assistance and documentation

### Command Line Interface

For automation and scripting, DarkForge supports command-line operations:

```bash
# Generate passwords from a profile file
python main.py generate --profile templates/example_profile.json --output my_passwords.txt

# Analyze a password file
python main.py analyze --file passwords.txt --output analysis_report.json

# Export passwords to Hashcat format
python main.py export --file passwords.txt --format hashcat --hash-type md5
```

### Python API

DarkForge can be integrated into other Python applications:

```python
from modules.data_input.collector import UserProfile, get_user_profile
from modules.pattern_generator import generate_passwords
from modules.password_analyzer import rate_password_strength

# Create a user profile
profile_data = {
    "first_name": "John",
    "last_name": "Smith",
    "birthdate": 15,
    "birth_month": 6,
    "birth_year": 1985,
    # Add other profile data as needed
}
profile = UserProfile(**profile_data)

# Generate passwords
passwords = generate_passwords(profile)

# Analyze a password
analysis = rate_password_strength("MyPassword123!")
print(f"Password strength: {analysis['strength']}")
```

## Working with User Profiles

### Profile Structure

A user profile contains personal information that might be used in password creation:

- Basic information (name, birthdate, phone)
- Family details (spouse, children, pets)
- Personal preferences (favorite movie, sports team)
- Social media identifiers
- And more

### Creating Profiles

Profiles can be created in three ways:

1. **Interactive Input**: Follow prompts to enter information
2. **JSON Template**: Edit and use a JSON profile template
3. **Programmatic Creation**: Create via the Python API

Example template (abbreviated):
```json
{
    "first_name": "John",
    "last_name": "Smith",
    "birthdate": 15,
    "birth_month": 6,
    "birth_year": 1985,
    "pet_name": "Buddy"
}
```

## Password Generation

DarkForge uses templates and algorithms to generate potential passwords:

### Generation Methods

1. From the **Generate Passwords** menu:
   - Select "Generate from interactive input" to enter data directly
   - Select "Generate from saved profile" to use a template file
   - Select "Save user profile" to store a profile for later use

2. From command line:
   ```bash
   python main.py generate --profile templates/my_profile.json
   ```

### Pattern Examples

DarkForge implements common password creation patterns, including:

- `{first_name}{birth_year}` (e.g., "John1985")
- `{pet_name}{birth_year}` (e.g., "Buddy1985")
- `{first_name}{last_name}{birth_year}` (e.g., "JohnSmith1985")
- `{spouse_name}{anniversary}` (e.g., "Jane1005")

Plus hundreds more combinations and variations with character substitutions.

## Password Analysis

### Analysis Features

DarkForge provides several password analysis capabilities:

1. **Password File Analysis**: Assess all passwords in a file
2. **Single Password Check**: Detailed analysis of individual passwords
3. **Pattern Detection**: Identify specific patterns used in passwords

### Assessment Metrics

- **Entropy**: Measure of password randomness/unpredictability
- **Strength Categories**: Very Weak, Weak, Moderate, Strong, Very Strong
- **Score**: Numeric rating from 1-5
- **Pattern Detection**: Identification of common patterns

### Using Analysis

From the **Analyze Passwords** menu:
- Select "Analyze password file" to process multiple passwords
- Select "Check single password" for individual assessment
- Select "Pattern analysis only" to focus on pattern identification

## Export Formats

DarkForge supports exporting passwords in formats compatible with popular cracking tools:

### Available Formats

1. **Plain Text**: Simple list of passwords
2. **Hashcat**: Compatible with the hashcat password recovery tool
3. **John the Ripper**: Compatible with John the Ripper cracking tool

### Hash Types

For Hashcat and John exports, the following hash types are supported:
- MD5
- SHA1
- SHA256
- SHA512
- NTLM

### Export Process

From the **Export Formats** menu:
1. Select the desired export format
2. Provide the password file path
3. Select hash type (if applicable)
4. Specify output filename
5. The file will be created in the appropriate output directory

## Technical Details

### Password Generation Algorithm

DarkForge uses a multi-stage approach to password generation:

1. **Template Selection**: Apply various templates to user data
2. **Transformation**: Apply character substitutions (e.g., 'a' → '4')
3. **Variation**: Create common variations (capitalization, suffix/prefix)

### Password Analysis Methodology

Passwords are analyzed using multiple criteria:

1. **Entropy Calculation**: Based on character set and length
2. **Pattern Matching**: Regular expressions identify common patterns
3. **Compositional Analysis**: Character types and distribution
4. **Dictionary Checking**: Compare against common password lists

### Database Structure

DarkForge maintains a SQLite database with the following tables:

- `user_profiles`: Stores user profile information
- `password_analysis`: Records of password analysis results
- `password_generation`: History of password generation operations
- `attack_simulation`: Results of simulated attack attempts

## Legal and Ethical Considerations

### Authorized Use Only

DarkForge is designed for:
- Security professionals conducting authorized testing
- Penetration testers with client permission
- Security awareness training and education

### Prohibited Uses

DarkForge should NOT be used for:
- Unauthorized access to systems
- Testing systems without explicit permission
- Illegal activities of any kind

### Data Privacy

When collecting and storing profile information:
- Ensure you have permission to use any personal data
- Consider anonymizing data when possible
- Follow applicable data protection regulations

## Troubleshooting

### Common Issues

1. **File Path Problems**
   - Use absolute paths when files can't be found
   - Ensure directories exist before saving files

2. **Permission Issues**
   - Verify write permissions in output directories
   - Run with appropriate permissions if needed

3. **Database Errors**
   - If database becomes corrupted, delete `darkforge.db` and restart
   - Ensure the database directory is writable

4. **Import Errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Ensure you're using Python 3.6 or higher

## Future Development

### Planned Features

1. **Phase 2: Analysis & Visualization** (April 2025)
   - Enhanced password strength assessment
   - Visual representations of pattern distributions
   - Machine learning pattern recognition

2. **Phase 3: Advanced Cracking Integration** (May 2025)
   - Direct integration with Hashcat and John the Ripper
   - GPU acceleration support
   - Extended wordlist and rule management

3. **Phase 4: Enterprise Features** (June 2025)
   - Active Directory integration
   - Team collaboration capabilities
   - Comprehensive reporting system

## Contributing

Contributions to DarkForge are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin new-feature`
5. Submit a pull request

## License

DarkForge is licensed under the MIT License. See the LICENSE file for details.

## Author

Shivendra Chauhan - Security Researcher
