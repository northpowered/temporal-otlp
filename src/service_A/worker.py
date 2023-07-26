from temporalio import workflow, activity
from temporalopentelemetry import TracingInterceptor
from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from datetime import timedelta
from tracer import tracer, trace
from env import SERVICE_LETTER, PROMETHEUS_PORT, TEMPORAL_ENDPOINT, TEMPO_ENDPOINT
from logger import setup_logging
from loguru import logger
from uuid import uuid4
import os


setup_logging()


TASK_QUEUE: str = f"service_{SERVICE_LETTER}_queue"


@activity.defn(name="service_a_activity_01")
async def service_a_activity_01(x_request_id: str) -> str:
    with tracer.start_as_current_span("EXECUTE-A-ACTIVITY", kind=trace.SpanKind.SERVER) as span:

        span.set_attribute("x_request_id", x_request_id)
        span.set_attribute("service_letter", SERVICE_LETTER)
        
        logger.info(
            f"Execute {activity.info().activity_type}",
            x_request_id=x_request_id,
            service_letter=SERVICE_LETTER,
        )
        return x_request_id


@workflow.defn(name="Service-A-workflow", sandboxed=False)
class ServiceAWorkflow:
    @workflow.run
    async def run(self):
        
        with tracer.start_as_current_span(
            "MAIN-A-RUN", kind=trace.SpanKind.SERVER
        ) as span:
            
            x_request_id: str = str(uuid4())
            span.set_attribute("x_pid", str(os.getpid()))
            span.set_attribute("x_request_id", x_request_id)
            span.set_attribute("service_letter", SERVICE_LETTER)
            

            with tracer.start_as_current_span("RUN-A-ACTIVITY", kind=trace.SpanKind.CLIENT) as span:

                span.set_attribute("x_request_id", x_request_id)
                span.set_attribute("service_letter", SERVICE_LETTER)

                result_a = await workflow.execute_activity(
                    service_a_activity_01,
                    x_request_id,
                    task_queue=TASK_QUEUE,
                    start_to_close_timeout=timedelta(seconds=5),
                )
            with tracer.start_as_current_span("RUN-B-WORKFLOW", kind=trace.SpanKind.CLIENT) as span:

                span.set_attribute("x_request_id", x_request_id)
                span.set_attribute("service_letter", SERVICE_LETTER)

                result_b = await workflow.execute_child_workflow(
                    "Service-B-workflow", arg=result_a, task_queue="service_B_queue", id=str(uuid4())
                )
            with tracer.start_as_current_span("RUN-C-WORKFLOW", kind=trace.SpanKind.CLIENT) as span:

                span.set_attribute("x_request_id", x_request_id)
                span.set_attribute("service_letter", SERVICE_LETTER)

                result = await workflow.execute_child_workflow(
                    "Service-C-workflow", arg=result_b, task_queue="service_C_queue"
                )
        
        return result


async def run_service():
    runtime = Runtime(
        telemetry=TelemetryConfig(
            # metrics=OpenTelemetryConfig(f"http://0.0.0.0:{PROMETHEUS_PORT}")
            metrics=PrometheusConfig(bind_address=f"0.0.0.0:{PROMETHEUS_PORT}"),
        )
    )

    client = await Client.connect(
        target_host=TEMPORAL_ENDPOINT,
        interceptors=[TracingInterceptor(tracer=tracer)],
        runtime=runtime,
    )
    worker = Worker(
        client=client,
        task_queue=TASK_QUEUE,
        workflows=[ServiceAWorkflow],
        activities=[service_a_activity_01],
    )
    await worker.run()


def run_worker():
    logger.info(f"Starting worker {SERVICE_LETTER}")
    logger.info(f"TEMPORAL_ENDPOINT: {TEMPORAL_ENDPOINT}")
    asyncio.run(run_service())
