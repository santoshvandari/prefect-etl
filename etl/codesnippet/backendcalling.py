import aiohttp
import os
async def create_flow_run_some_etl(
    data1,data2
):
    if not data1 and not data2:
        print("At least one of data1 or data2 must be provided.")
        return

    deployment_id = os.environ.get('ETL_DEPLOYMENT_ID')
    prefect_api_url = os.environ.get('PREFECT_API_URL')
    api_url = f"{prefect_api_url}/deployments/{deployment_id}/create_flow_run"

    payload = {
        "parameters": {
            "data1": data1,
            "data2": data2
        },
        "state": {
            "type": "SCHEDULED",
            "state_details": {}
        }
    }

    # Use aiohttp for non-blocking HTTP call
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload) as response:
            if response.status != 201:
                text = await response.text()
                print(f"Failed to create flow run: {response.status} - {text}")
            else:
                print(f"Flow run created successfully.")


if __name__ == "__main__":
    import asyncio
    data1 = "example_data_1"  # Replace with actual data or logic to fetch data
    data2 = "example_data_2"  # Replace with actual data or logic to fetch data
    asyncio.run(create_flow_run_some_etl(data1, data2))

