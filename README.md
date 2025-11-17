# Dev Monitor

A cross-platform Python application to monitor the status of remote IP devices. Built with Tkinter for the UI, featuring event-driven architecture, background task scheduling, and persistent device storage.

## Features

- ✅ Add/remove/monitor remote devices via GUI
- ✅ TCP connection-based status checking (parallel checks)
- ✅ Persistent device storage (JSON format)
- ✅ Background auto-check scheduler
- ✅ Event-driven architecture with pub/sub event bus
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Comprehensive logging with file rotation
- ✅ Full type hints and mypy compatibility

## System Requirements

- Python 3.9 or higher
- Tkinter (included with most Python distributions)

### Platform-Specific Notes

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get install python3-tk
```

**macOS**
- Tkinter is included with Python from python.org
- Homebrew Python may require: `brew install python-tk@3.12`

**Windows**
- Tkinter is included with official Python installers
- Ensure "tcl/tk and IDLE" is selected during Python installation

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Tracsom/dev_monitor.git
cd dev_monitor
```

### 2. Create a Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Run the Application

**Linux/macOS:**
```bash
python __main__.py
python __main__.py --debug  # Enable debug logging
```

**Windows (PowerShell/Command Prompt):**
```cmd
python __main__.py
python __main__.py --debug
```

### UI Guide

1. **Add Device**: Click "Add Device" and enter:
   - Device name (e.g., "router", "server-01")
   - IP address (e.g., "192.168.1.1")
   - Port (default: 80)
   - Timeout in seconds (default: 5)

2. **Check All**: Click "Check All" to run TCP connection checks on all enabled devices

3. **Remove Device**: Select a device and click "Remove Selected"

4. **Refresh**: Click "Refresh" to reload the device list

5. **Close**: Close the window to gracefully shut down the application

### View Logs

**Linux/macOS:**
```bash
cat ~/.dev_monitor/app.log
tail -f ~/.dev_monitor/app.log  # Follow logs in real-time
```

**Windows:**
```cmd
type %USERPROFILE%\.dev_monitor\app.log
Get-Content $env:USERPROFILE\.dev_monitor\app.log -Wait  # PowerShell: follow in real-time
```

## Configuration

Edit `src/config.py` to customize:

```python
DEFAULT_CHECK_INTERVAL = 300  # Auto-check interval in seconds (default: 5 min)
AUTO_CHECK_ENABLED = True      # Enable/disable background auto-checks
LOG_LEVEL = "INFO"             # Logging level: DEBUG, INFO, WARNING, ERROR
```

Or set environment variables:

```bash
export LOG_LEVEL=DEBUG
python __main__.py
```

## Development

### Run Tests

```bash
pytest -v
pytest --cov=src  # With coverage report
```

### Type Checking

```bash
mypy src
```

### Linting

```bash
flake8 src tests
black src tests --check
```

### Format Code

```bash
black src tests
```

## Project Structure

```
dev_monitor/
├── src/
│   ├── app.py                 # Main application entry point
│   ├── config.py              # Configuration management
│   ├── exceptions.py          # Custom exception hierarchy
│   ├── bus/                   # Event bus (pub/sub)
│   ├── models/                # Data models (Device, Repository)
│   ├── services/              # Business logic (DeviceService, SchedulerService)
│   ├── controllers/           # Event handlers (MainController)
│   ├── ui/                    # Tkinter UI components
│   └── utils/                 # Utilities (logging, validators)
├── tests/                     # Unit tests
├── __main__.py               # Entry point
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## API / Event Bus

The application uses an event-driven architecture. Key events:

- `add_device`: Add a new device
- `remove_device`: Remove a device
- `check_all_devices`: Trigger status checks on all devices
- `get_devices`: Retrieve all devices
- `device_added`: Device successfully added
- `device_removed`: Device successfully removed
- `devices_checked`: Status checks completed

## Logging

Logs are stored in:
- **Linux/macOS**: `~/.dev_monitor/app.log`
- **Windows**: `%USERPROFILE%\.dev_monitor\app.log`

Logs rotate automatically at 10MB with 5 backup files kept.

## Troubleshooting

### "No module named 'src'"
Ensure you've run `pip install -e .` in the project root.

### Tkinter not found
Install platform-specific Tkinter (see "Platform-Specific Notes" above).

### Device shows "Offline" but should be online
- Verify the IP address and port are correct
- Check network connectivity: `ping <ip-address>`
- Ensure the service is running on the target port
- Check firewall rules (TCP port may be blocked)

### UI doesn't respond
The app may be checking devices. Wait for checks to complete (default timeout: 5 seconds per device).

## License

MIT License — see LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -m 'Add my feature'`)
4. Push to branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## Future Enhancements

- [ ] HTTP/HTTPS status code checks
- [ ] Ping-based device checks (ICMP)
- [ ] Device groups/categories
- [ ] Alert notifications (email, webhook)
- [ ] Web dashboard
- [ ] REST API
- [ ] Database backend (SQLite, PostgreSQL)
- [ ] Export device lists (CSV, JSON)
- [ ] Batch import devices

## Support

For issues, questions, or suggestions:
- Open a GitHub Issue
- Check existing documentation
- Review logs in `~/.dev_monitor/app.log`

---

**Made with ❤️ using Python and Tkinter**