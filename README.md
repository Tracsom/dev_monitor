# Dev Monitor

A simple application to monitor the status of remote IP devices.

## Intallation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m dev_monitor
python -m dev_monitor --debug # Enable debug logging
```

## Configuration

Configuration is handled via `src/config.py`. Key settings:

 - `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
 - `DEFAULT_CHECK_INTERVAL`: Auto-check interval in seconds
 - `LOG_FILE`: Location of application log

## Features

 - Add/remove/monitor remove devices
 - TCP connection-based status checking
 - Persistent device storage (JSON)
 - Tkinter GUI
 - Event-driven architechture
 - Comprehensive logging

## Project Structure

```
src/
|- models/          # Data models
|- services/        # Business Logic
|- controllers/     # Event handlers
|- ui/              # User interface
|- bus/             # Event bus
|- config.py        # Configuration
|- exceptions.py    # Custom Exceptions
|- utils/           # Utilities (validators, logging)
```

## Testing

```bash
pytest tests/
```

## Logging

Logs are written to `~/.dev_monitor/app.log` with automatic rotation.