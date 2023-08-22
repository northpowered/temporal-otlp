from tracer import tracer, trace
from env import SERVICE_LETTER
from logger import setup_logging
from loguru import logger


setup_logging()


def main():

    with tracer.start_as_current_span("TEST-SPAN") as span:
        span.set_attribute("foo", "bar")
        logger.info(
            "Test msg",
            span=span,
            service_letter=SERVICE_LETTER,
        )

main()

