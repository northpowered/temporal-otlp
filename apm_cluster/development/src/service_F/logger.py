import logging
from loguru import logger
import sys
import traceback
from env import LOG_JSON, LOG_LEVEL


class InterceptHandler(logging.Handler):

    def emit(self, record):
        extra_data: dict = dict()
        try:
            # Trying to catch `trace_id` and exclude None, if cought
            
            assert record.trace_id
            extra_data['trace_id'] = record.trace_id
        except (AttributeError, AssertionError):
            pass
        if record.exc_info:
            extra_data['exc_info'] = record.exc_info
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        # Inject `extra` payload to `message` dict
        log = logger.bind(**extra_data)

        log.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage())


def setup_logging():

    logging.root.handlers = [InterceptHandler()]

    def formatter(record):
        
        base_fmt = ""
        extra: dict = record.get('extra', dict())

        exception = record.get('exception')

        if exception:
            extra["traceback"] = "\n" + \
                "".join(traceback.format_exception(extra['exc_info'][1]))
            return base_fmt + f"{extra['traceback']}"
        return base_fmt + "{message}"

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "serialize": LOG_JSON,
                "level": LOG_LEVEL,
                "format": formatter,
                "colorize": False
            }
        ]
    )
