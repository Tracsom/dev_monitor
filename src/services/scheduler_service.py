# src/services/scheduler_service.py
"""
Background scheduler for periodic tasks.
"""
import logging
import threading
import time
from typing import Callable, Optional
from src.config import Config

logger = logging.getLogger(__name__)

class SchedulerService:
    """Manages background scheduled tasks."""

    def __init__(self):
        """Initialize scheduler service."""
        self._tasks: dict = {}
        self._running = False
        self._lock = threading.Lock()
        # event used to request worker threads stop promptly
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start the scheduler."""
        while self._lock:
            if self._running:
                logger.warning("Scheduler already running")
                return
            self._running = True
            self._stop_event.clear()
        logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop the scheduler."""
        with self._lock:
            if not self._running:
                return
            self._running = False
            self._stop_event.set()
        # join selected threads to ensure clean shutdown
        for name, thread in list(self._tasks.items()):
            if thread.is_alive():
                thread.join(timeout=2)
        self._tasks.clear()
        logger.info("Scheduler stopped")

    def schedule_repeating(self, task_name: str, callback: Callable, interval: int) -> None:
        """
        Schedule repeating task.

        Args:
            task_name: Unique task name
            callback: Function to call
            interval: Interval in seconds
        """
        if task_name in self._tasks:
            logger.warning(f"Task already scheduled: {task_name}")
            return
        
        def worker():
            logger.debug("Scheudled task %s started (interval=%s)", task_name, interval)
            # run immediately then wait interval using stop_event.wait for responsiveness
            while not self._stop_event.is_set() and self._running:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error in scheduled task {task_name}: {e}", exc_info=True)
                # wait returns True if stop_event set (break early)
                if self._stop_event.wait(timeout=interval):
                    break
            logger.debug("Scheduled task %s exiting", task_name)

        thread = threading.Thread(target=worker, daemon=True, name=f"task-{task_name}")
        self._tasks[task_name] = thread
        thread.start()
        logger.info(f"Scheduled task: {task_name} (interval: {interval}s)")

    def unschedule(self, task_name: str) -> None:
        """
        Remove a scheduled task.

        Args:
            task_name: Task identifier
        """
        if task_name in self._tasks:
            del self._tasks[task_name]
            logger.info(f"Unscheduled task: {task_name}")