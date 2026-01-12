# Scripts

This folder contains script files used to start and set up the application.

## Files

- **start.bat** - Windows startup script
- **setup_linux.sh** - Linux automatic setup script

## Usage

### Windows

Double-click the `start.bat` file to start the application. The script automatically:
1. Navigates to the project root directory
2. Activates the virtual environment
3. Starts the application

### Linux

Run the setup script:

```bash
chmod +x scripts/setup_linux.sh
./scripts/setup_linux.sh
```

The script automatically:
1. Checks Python installation
2. Creates virtual environment
3. Installs dependencies
4. Prepares systemd service file
5. Shows installation instructions

For detailed information:
- [Windows Installation Guide](../docs/INSTALLATION.md)
- [Linux Installation Guide](../docs/LINUX_INSTALLATION.md)

---

**[View Turkish Version](README_TR.md)**
