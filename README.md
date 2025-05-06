# SmartStock - Inventory Management System

A Python-based inventory management system with a modern GUI interface.

## Features
- Product management
- Invoice generation
- PDF export functionality
- Analytics and reporting
- User authentication

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mouhssine07/GestionStock_Python.git
cd GestionStock_Python
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Building the Executable

To create an executable for your system:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller smartstock.spec
```

The executable will be created in the `dist` folder.

## Running the Application

### Option 1: Run from source
```bash
python smartstock_login.py
```

### Option 2: Run the executable
Navigate to the `dist` folder and run `SmartStock.exe`

## System Requirements
- Python 3.8 or higher
- Windows 10/11
- 4GB RAM minimum
- 500MB free disk space

## Dependencies
All required dependencies are listed in `requirements.txt`

## License
[Your License Here]

## Author
[Your Name] 