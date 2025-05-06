# SmartStock - Inventory Management System

A professional inventory management system with a modern GUI interface, designed for easy use without any technical knowledge.

## Features
- Product management
- Invoice generation
- PDF export functionality
- Analytics and reporting
- User authentication

## Quick Start Guide

### For End Users (No Installation Required)
1. Download the `SmartStock_Portable.zip` file
2. Extract the ZIP file to any folder on your computer
3. Double-click `SmartStock.exe` to start the application

### System Requirements
- Windows 10/11
- 4GB RAM minimum
- 500MB free disk space
- No Python or other software required

## Default Login Credentials
- Username: admin
- Password: admin

## First Time Setup
1. Extract the ZIP file to a permanent location
2. Create a shortcut on your desktop if desired
3. Run the application
4. Change the default password after first login

## Data Storage
- All data is stored locally on your computer
- No internet connection required
- Regular backups recommended

## Support
For technical support or questions, please contact:
- Email: [Your Email]
- GitHub: [Your GitHub Profile]

## License
[Your License Here]

## Author
Mouhssine Jaiba

---

## For Developers
If you want to modify or build the application from source, follow these steps:

1. Install Python 3.8 or higher
2. Clone the repository:
```bash
git clone https://github.com/mouhssine07/GestionStock_Python.git
cd GestionStock_Python
```

3. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Build the executable:
```bash
pip install pyinstaller
pyinstaller smartstock.spec
```

The executable will be created in the `dist` folder. 