from temporalio import workflow, activity
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from datetime import timedelta
from tracer import tracer, trace
from env import SERVICE_LETTER, PROMETHEUS_PORT, TEMPORAL_ENDPOINT
from logger import setup_logging
from loguru import logger


setup_logging()


TASK_QUEUE: str = f"service_{SERVICE_LETTER}_queue"


@activity.defn(name=f'service_{SERVICE_LETTER}_activity_01')
async def activity_01(payload: str) -> str:
    with tracer.start_as_current_span(f"EXECUTE-{SERVICE_LETTER}-ACTIVITY", kind=trace.SpanKind.SERVER) as span:
        logger.info(
            f"Execute {activity.info().activity_type}",
            x_request_id=payload,
            service_letter=SERVICE_LETTER
        )
        return payload


@workflow.defn(name=f"Service-{SERVICE_LETTER}-workflow", sandboxed=False)
class ServiceWorkflow:
    @workflow.run
    async def run(self, payload: str):
        with tracer.start_as_current_span(f"MAIN-{SERVICE_LETTER}-RUN", kind=trace.SpanKind.SERVER) as span:

            span.set_attribute("x_request_id", payload)
            span.set_attribute("service_letter", SERVICE_LETTER)

            with tracer.start_as_current_span(f"RUN-{SERVICE_LETTER}-ACTIVITY", kind=trace.SpanKind.CLIENT) as span:

                span.set_attribute("x_request_id", payload)
                span.set_attribute("service_letter", SERVICE_LETTER)

                result = await workflow.execute_activity(
                    activity=activity_01,
                    arg=payload,
                    task_queue=TASK_QUEUE,
                    start_to_close_timeout=timedelta(seconds=5)
                )
            
            with tracer.start_as_current_span(f"RUN-D-WORKFLOW", kind=trace.SpanKind.CLIENT) as span:

                span.set_attribute("x_request_id", payload)
                span.set_attribute("service_letter", SERVICE_LETTER)

                result = await workflow.execute_child_workflow(
                    workflow="Service-D-workflow",
                    arg=payload,
                    task_queue="service_D_queue",
                )
                return result


async def run_service():
    runtime = Runtime(
        telemetry=TelemetryConfig(
            metrics=PrometheusConfig(bind_address=f"0.0.0.0:{PROMETHEUS_PORT}")
        )
    )

    client = await Client.connect(
        target_host=TEMPORAL_ENDPOINT,
        interceptors=[TracingInterceptor(tracer=tracer)],
        runtime=runtime
    )
    worker = Worker(
        client=client,
        task_queue=TASK_QUEUE,
        workflows=[ServiceWorkflow],
        activities=[activity_01]
    )
    await worker.run()


def run_worker():
    logger.info(f"Starting worker {SERVICE_LETTER}")
    asyncio.run(run_service())
