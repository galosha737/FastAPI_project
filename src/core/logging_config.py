import logging
import sys
import contextvars
from pythonjsonlogger import jsonlogger
from src.core.config import settings

# Контексная переменная для хранения id запроса
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar('request_id', default=None)


class ContextualJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        req_id = request_id_var.get()
        if req_id:
            log_record['request_id'] = req_id


def setup_logging():
    ''' Глобальное логгирование всего приложения'''
    log_level = getattr(logging, settings.LOG_LEVEL)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.handlers:
        root_logger.handlers.clear()

    json_formatter = ContextualJsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        rename_fields={'asctime': '@timestamp', 'name': 'logger', 'levelname': 'level'},
        datefmt='%Y-%m-%dT%H:%M:%S.%fZ'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(json_formatter)

    root_logger.addHandler(handler)

    logging.info(f"Logging with level: {settings.LOG_LEVEL}")