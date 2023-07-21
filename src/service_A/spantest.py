from tracer import tracer, trace
from env import SERVICE_LETTER
from logger import setup_logging
from loguru import logger


setup_logging()


def main():

    with tracer.start_as_current_span("TEST-SPAN") as span:
        logger.info(
            "Test msg",
            span=span,
            extra={
                "SERVICE_LETTER": SERVICE_LETTER,
                # "span_id": span.get_span_context().span_id,
                # "trace_id": span.get_span_context().trace_id
            }
        )

main()

