from temporalio.client import Client
import asyncio
import uuid


async def run_service():

    client = await Client.connect(
        target_host="localhost:7233",
        namespace="dev"
    )

    result = await client.execute_workflow(
        workflow="Service-A-workflow",
        id=str(uuid.uuid4()),
        task_queue="service_A_queue"
    )
    return result



if __name__ == "__main__":

    print("Start Service-A-workflow runner")
    result = asyncio.run(run_service())
    print(result)
    print("Close Service-A-workflow runner")


