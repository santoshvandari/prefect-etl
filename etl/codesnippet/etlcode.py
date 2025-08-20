import asyncio
from prefect import task, flow
from prefect.task_runners import ThreadPoolTaskRunner


@task
async def process_data(data):
    # Simulate data processing
    await asyncio.sleep(1)
    print(f"Processed data: {data}")
    return {"status": "success", "data": data}


@task(retries=2, retry_delay_seconds=3)
async def task_retries_snippit(data):
    try:
        result = await process_data(data)
        return result
    except Exception as e:
        print(f"Error processing {data}: {e}")
        raise


@flow(log_prints=True, task_runner=ThreadPoolTaskRunner(max_workers=3))
async def some_etl(data1=None, data2=None):
    """ETL flow to process a data"""
    if data1:
        await process_data(data1)
    if data2:
        await process_data(data2)

