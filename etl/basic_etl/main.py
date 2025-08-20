import os,requests
from prefect import serve,flow,task
import pandas as pd

@task
def fetch_api_data():
    try:
        response = requests.get("https://fakestoreapi.in/api/products")
        if response.status_code != 200:
            return None
        return response.json()
    except Exception as e:
        print(f"Error fetching API data: {e}")
        return None
@task
def process_data(data):
    if data is None:
        return None
    return data.get("products", [])


@task
def save_data_in_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False)

@flow(name="basic_etl_flow",log_prints=True)
def basic_etl_flow():
    data = fetch_api_data()
    processed_data = process_data(data)
    save_data_in_csv(processed_data)


# Run the flow with a local executor
if __name__ == "__main__":
    basic_etl_flow_deploy=basic_etl_flow.to_deployment(
        name="Basic ETL Flow",
        cron=os.environ['CRON_SCHEDULE']
    )
    serve(basic_etl_flow_deploy)