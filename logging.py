
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


# ============================================================
# DEFAULT VALUES
# ============================================================

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


# ============================================================
# CUSTOM LOGGER WRAPPER
# ============================================================

class Logger:
    """
    Application logger wrapper.

    Provides:
    - info()
    - warning()
    - error()
    - debug()
    - critical()
    """

    def __init__(
        self,
        name: Optional[str] = None,
    ):
        """
        Create a logger instance.

        Args:
            name:
                Logger name.
        """

        self.logger = logging.getLogger(
            name or "ai_app_generator"
        )

    # ========================================================
    # DEBUG
    # ========================================================

    def debug(
        self,
        message: str,
        **kwargs,
    ):
        """
        Log a debug message.
        """

        self.logger.debug(
            self._format_message(
                message,
                kwargs,
            )
        )

    # ========================================================
    # INFO
    # ========================================================

    def info(
        self,
        message: str,
        **kwargs,
    ):
        """
        Log an informational message.
        """

        self.logger.info(
            self._format_message(
                message,
                kwargs,
            )
        )

    # ========================================================
    # WARNING
    # ========================================================

    def warning(
        self,
        message: str,
        **kwargs,
    ):
        """
        Log a warning message.
        """

        self.logger.warning(
            self._format_message(
                message,
                kwargs,
            )
        )

    # ========================================================
    # ERROR
    # ========================================================

    def error(
        self,
        message: str,
        **kwargs,
    ):
        """
        Log an error message.
        """

        self.logger.error(
            self._format_message(
                message,
                kwargs,
            )
        )

    # ========================================================
    # CRITICAL
    # ========================================================

    def critical(
        self,
        message: str,
        **kwargs,
    ):
        """
        Log a critical message.
        """

        self.logger.critical(
            self._format_message(
                message,
                kwargs,
            )
        )

    # ========================================================
    # FORMAT MESSAGE
    # ========================================================

    @staticmethod
    def _format_message(
        message: str,
        context: dict,
    ) -> str:
        """
        Add contextual key-value data to the log message.
        """

        if not context:
            return message

        context_string = " ".join(
            f"{key}={value}"
            for key, value in context.items()
        )

        return f"{message} | {context_string}"


# ============================================================
# SETUP LOGGING
# ============================================================

def setup_logging(
    log_level: str = DEFAULT_LOG_LEVEL,
    log_format: str = DEFAULT_LOG_FORMAT,
    log_file: Optional[str] = None,
):
    """
    Configure application-wide logging.

    Args:
        log_level:
            Logging level such as DEBUG, INFO, WARNING,
            ERROR, or CRITICAL.

        log_format:
            Format used for log messages.

        log_file:
            Optional path to a log file.
    """

    # --------------------------------------------------------
    # NORMALIZE LOG LEVEL
    # --------------------------------------------------------

    if not log_level:
        log_level = DEFAULT_LOG_LEVEL

    log_level = str(
        log_level
    ).upper()

    numeric_level = getattr(
        logging,
        log_level,
        logging.INFO,
    )

    # --------------------------------------------------------
    # CREATE FORMATTER
    # --------------------------------------------------------

    formatter = logging.Formatter(
        log_format
    )

    # --------------------------------------------------------
    # GET ROOT LOGGER
    # --------------------------------------------------------

    root_logger = logging.getLogger()

    root_logger.setLevel(
        numeric_level
    )

    # --------------------------------------------------------
    # REMOVE EXISTING HANDLERS
    # --------------------------------------------------------

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(
            handler
        )

        try:
            handler.close()

        except Exception:
            pass

    # --------------------------------------------------------
    # CONSOLE HANDLER
    # --------------------------------------------------------

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setLevel(
        numeric_level
    )

    console_handler.setFormatter(
        formatter
    )

    root_logger.addHandler(
        console_handler
    )

    # --------------------------------------------------------
    # FILE HANDLER
    # --------------------------------------------------------

    if log_file:

        log_path = Path(
            log_file
        )

        # Create parent directory
        if log_path.parent:
            log_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(
                log_path
            ),
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setLevel(
            numeric_level
        )

        file_handler.setFormatter(
            formatter
        )

        root_logger.addHandler(
            file_handler
        )

    # --------------------------------------------------------
    # LOG INITIALIZATION
    # --------------------------------------------------------

    root_logger.info(
        "Logging initialized | level=%s | file=%s",
        log_level,
        log_file or "console only",
    )


# ============================================================
# GET LOGGER
# ============================================================

def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Return a standard Python logger.

    Args:
        name:
            Logger name.

    Returns:
        logging.Logger
    """

    return logging.getLogger(
        name or "ai_app_generator"
    )
