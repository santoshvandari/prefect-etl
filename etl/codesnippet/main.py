import os

from prefect import serve

from etlcode import some_etl


# Run the flow with a local executor
if __name__ == "__main__":
    parameters = {
        "data1": os.environ["data1"],
        "data2": os.environ["data2"],
    }
    some_etl_deploy = some_etl.to_deployment(
        name="Some ETL",
        parameters=parameters,
    )
    serve(some_etl_deploy)
