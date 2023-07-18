from temporalio import workflow, activity
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig, LoggingConfig
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from datetime import timedelta
from tracer import tracer, trace
from env import SERVICE_LETTER
from logger import setup_logging
from loguru import logger


setup_logging()


TASK_QUEUE: str = "service_a_queue"


@activity.defn(name='service_a_activity_01')
async def service_a_activity_01() -> str:
    with tracer.start_as_current_span("EXECUTE-A-ACTIVITY") as span:
        logger.info(f"Execute {activity.info().activity_type}")
        return "A"


@workflow.defn(name="Service-A-workflow", sandboxed=False)
class ServiceAWorkflow:
    @workflow.run
    async def run(self):
        with tracer.start_as_current_span("MAIN-A-RUN", kind=trace.SpanKind.SERVER) as span:
            span.set_attribute("x-custom-tag", "foobar")

            with tracer.start_as_current_span("RUN-A-ACTIVITY") as span:
                result_a = await workflow.execute_activity(
                    activity=service_a_activity_01,
                    task_queue=TASK_QUEUE,
                    start_to_close_timeout=timedelta(seconds=5)
                )
            with tracer.start_as_current_span("RUN-B-WORKFLOW") as span:
                result_b = await workflow.execute_child_workflow(
                    "Service-B-workflow",
                    arg=result_a,
                    task_queue="service_B_queue"
                )
            with tracer.start_as_current_span("RUN-C-WORKFLOW") as span:
                result = await workflow.execute_child_workflow(
                    "Service-C-workflow",
                    arg=result_b,
                    task_queue="service_C_queue"
                )
            return result


async def run_service():

    runtime = Runtime(
        telemetry=TelemetryConfig(
            metrics=PrometheusConfig(bind_address="0.0.0.0:5001"),
            
        )
    )

    client = await Client.connect(
        target_host="localhost:7233",
        interceptors=[TracingInterceptor()],
        runtime=runtime
    )
    worker = Worker(
        client=client,
        task_queue=TASK_QUEUE,
        workflows=[ServiceAWorkflow],
        activities=[service_a_activity_01]
    )
    await worker.run()


def run_worker():

    print(f"Start worker {SERVICE_LETTER}")
    asyncio.run(run_service())
    print(f"Close worker {SERVICE_LETTER}")
