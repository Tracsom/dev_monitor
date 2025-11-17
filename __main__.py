# __main__.py
"""
Entry point for application.

Launches the app defined in src.
"""
import logging
import sys
from src import App
from src.utils.logger import setup_logging

if __name__ == "__main__":
    debug = "--debug" in sys.argv
    setup_logging(debug=debug)
    
    try:
        app = App(debug=debug)
        app.run()
    except Exception as e:
        logging.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)