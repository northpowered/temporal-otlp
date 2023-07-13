from temporalio import workflow, activity
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.client import Client
from temporalio.worker import Worker
from threading import Lock
import asyncio
import uuid
from datetime import timedelta
from tracer import tracer
from env import SERVICE_LETTER


TASK_QUEUE: str = f"service_{SERVICE_LETTER}_queue"


@activity.defn(name=f'service_{SERVICE_LETTER}_activity_01')
async def activity_01(payload: str) -> str:
    with tracer.start_as_current_span(f"EXECUTE-{SERVICE_LETTER}-ACTIVITY") as span:
        return f"{payload}->{SERVICE_LETTER}"


@workflow.defn(name=f"Service-{SERVICE_LETTER}-workflow", sandboxed=False)
class ServiceWorkflow:
    @workflow.run
    async def run(self, payload: str):
        with tracer.start_as_current_span(f"MAIN-{SERVICE_LETTER}-RUN") as span:
            with tracer.start_as_current_span(f"RUN-{SERVICE_LETTER}-ACTIVITY") as span:
                result = await workflow.execute_activity(
                    activity=activity_01,
                    arg=payload,
                    task_queue=TASK_QUEUE,
                    start_to_close_timeout=timedelta(seconds=5)
                )
            with tracer.start_as_current_span(f"RUN-D-WORKFLOW") as span:
                result = await workflow.execute_child_workflow(
                    workflow="Service-D-workflow",
                    arg=payload,
                    task_queue="service_D_queue",
                )
                return result


async def run_service():
    client = await Client.connect(
        target_host="localhost:7233",
        interceptors=[TracingInterceptor()]
    )
    worker = Worker(
        client=client,
        task_queue=TASK_QUEUE,
        workflows=[ServiceWorkflow],
        activities=[activity_01]
    )
    await worker.run()


def run_worker():
   
    print(f"Start worker {SERVICE_LETTER}")
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    asyncio.run(run_service())
    print(f"Close worker {SERVICE_LETTER}")
    