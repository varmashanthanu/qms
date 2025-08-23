# Define the base logging level based on the environment.
from qms.env import ENVIRONMENT

# In development, we want all messages (DEBUG, INFO, WARNING, ERROR, CRITICAL).
# In production, we only want INFO and above.

if ENVIRONMENT == "development":
    LOG_LEVEL = "INFO"
else:
    LOG_LEVEL = "INFO"

# The complete logging configuration dictionary.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": LOG_LEVEL,  # Use the dynamically set log level
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,  # Use the dynamically set log level
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}