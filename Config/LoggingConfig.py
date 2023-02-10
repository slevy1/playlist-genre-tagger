import logging
import logging.handlers
from Config import AppConfig
from logging.config import dictConfig

logger = logging.getLogger(__name__)

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}


def configure_logging(logfile_path, error_path):
    """
    Initialize logging defaults for Project.

    :param logfile_path: logfile used to the logfile
    :type logfile_path: string

    This function does:

    - Assign INFO and DEBUG level to logger file handler and console handler

    """
    dictConfig(DEFAULT_LOGGING)

    default_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    file_handler = logging.handlers.RotatingFileHandler(logfile_path, maxBytes=2684354, backupCount=300,
                                                        encoding='utf-8')
    error_file_handler = logging.handlers.RotatingFileHandler(error_path, maxBytes=2684354, backupCount=300,
                                                              encoding='utf-8')
    smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.gmail.com', 587),
                                                fromaddr=AppConfig.Logging.USER,
                                                toaddrs=AppConfig.Logging.TO,
                                                subject=AppConfig.Logging.SUBJECT,
                                                credentials=(AppConfig.Logging.USER, AppConfig.Logging.PASSWORD),
                                                secure=())

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(default_formatter)
    file_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(default_formatter)

    error_file_handler.setFormatter(default_formatter)
    error_file_handler.setLevel(logging.WARNING)

    smtp_handler.setFormatter(default_formatter)
    smtp_handler.setLevel(logging.ERROR)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(error_file_handler)
    logging.root.addHandler(console_handler)
    logging.root.addHandler(smtp_handler)
