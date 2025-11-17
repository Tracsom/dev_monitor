# src/app.py
"""
Defines the app, bringing together all the packages into a cohesive whole.
"""
import logging
from src.bus import Scheduler
from src.controllers import MainController
from src.ui import Interface
from src.services.scheduler_service import SchedulerService
from src.config import Config

logger = logging.getLogger(__name__)

class App:

    def __init__(self, debug: bool = False):
        """
        Initialize the individual parts of the app and combine them.

        Args:
            debug: Enable debug mode
        """
        self.debug = debug
        logger.info("Initializing application components")
        self.scheduler = Scheduler()
        self.controller = MainController(self.scheduler)
        # background scheduler service (manages repeating tasks)
        self.scheduler_service = SchedulerService()
        self.ui = Interface(self.scheduler, shutdown_callback=self.scheduler_service.stop)
        logger.info("Application initialized successfully")

    def run(self):
        """
        Launch UI with optional debug mode.

        Args:
            debug: Enable debug logging and mode.
        """
        if self.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")

        try:
            # start background scheduler and schedule auto-check if enabled
            self.scheduler_service.start()
            if Config.AUTO_CHECK_ENABLED:
                # schedule a repeating "check_all_devices" trigger
                self.scheduler_service.schedule_repeating(
                    "auto_check",
                    lambda: self.scheduler.publish("check_all_devices"),
                    Config.DEFAULT_CHECK_INTERVAL
                )
            
            # UI mainloop (blocks until window closed)
            self.ui.launch(debug=self.debug)
        except Exception as e:
            logger.error(f"Application error: {e}", exc_info=True)
            raise
        finally:
            # ensure scheduler stops on exit
            try:
                self.scheduler_service.stop()
            except Exception:
                logger.exception("Error stopping scheduler service")