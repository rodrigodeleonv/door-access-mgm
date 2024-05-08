"""Setup logging

Logging
Default: django.utils.log.DEFAULT_LOGGING
https://github.com/django/django/blob/main/django/utils/log.py
"""
from pathlib import Path


def logger_setup(log_dir: str, log_level: str) -> dict:
    """Configure Django logging.

    Args:
        log_dir: Path string where log is saved
        log_level: Log level

    Returns:
        Django logging config for settings module
    """
    LOG_DIR = Path(log_dir).resolve()
    LOG_DIR.mkdir(exist_ok=True, parents=True)

    # Filter for DEBUG
    # filter_for_file_handler = ['require_debug_true']
    # filter_for_file_handler = ['require_debug_false']
    #
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            # https://docs.python.org/3/library/logging.html#logrecord-attributes
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[{server_time}] {message}',
                'style': '{',
            },
            'verbose': {
                # 'format': '[{levelname} {asctime} {module} {process:d} {thread:d} {lineno}]> {message}',
                'format': '{levelname} {asctime} {module} {lineno}> {message}',
                # 'format': '{asctime} {levelname} [{name}:{lineno}] -> {message}',
                'style': '{',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'filters': ['require_debug_true']
            },
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                # 'formatter': 'django.server',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_DIR / 'app.log',
                'formatter': 'verbose',
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 10,
                # 'filters': filter_for_file_handler
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': log_level,
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'django.server', 'mail_admins'],
                'level': 'INFO'
            },
            'django.server': {
                'handlers': ['django.server', 'file'],
                'level': 'INFO',
                'propagate': False,
            },
            #
            # Other loggers
            #
            'asyncio': {
                'level': 'WARNING',  # avoid "Using selector: EpollSelector"
            },
            'urllib3': {
                'level': 'WARNING',
                'propagate': False
            },
        }
    }
    return LOGGING
