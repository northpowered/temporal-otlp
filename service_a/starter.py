from temporalio import workflow, activity
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
import uuid
from datetime import timedelta
from tracer import tracer, trace

TASK_QUEUE: str = "service_a_queue"


@activity.defn(name='service_a_activity_01')
async def service_a_activity_01() -> str:
    with tracer.start_as_current_span("EXECUTE-A-ACTIVITY") as span:
        return "A"


@workflow.defn(name="Service-A-workflow", sandboxed=False)
class ServiceAWorkflow:
    @workflow.run
    async def run(self):
        with tracer.start_as_current_span("MAIN-A-RUN", kind=trace.SpanKind.SERVER) as span:

            
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
    client = await Client.connect(
        target_host="localhost:7233",
        interceptors=[TracingInterceptor()]
    )

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ServiceAWorkflow],
        activities=[service_a_activity_01],
    ):

        result = await client.execute_workflow(
            workflow=ServiceAWorkflow.run,
            id=str(uuid.uuid4()),
            task_queue=TASK_QUEUE
        )
        return result



if __name__ == "__main__":

    result = asyncio.run(run_service())
    print(result)