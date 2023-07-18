from temporalio import workflow, activity
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.runtime import PrometheusConfig, Runtime, TelemetryConfig
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
import uuid
from datetime import timedelta


async def run_service():

    client = await Client.connect(
        target_host="localhost:7233",
    )

    result = await client.execute_workflow(
        workflow="Service-A-workflow",
        id=str(uuid.uuid4()),
        task_queue="service_a_queue"
    )
    return result



if __name__ == "__main__":

    print("Start Service-A-workflow runner")
    result = asyncio.run(run_service())
    print(result)
    print("Close Service-A-workflow runner")


