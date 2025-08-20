import os 
from data_load_etl import minio_to_mongo_etl
from prefect import serve

if __name__ == "__main__":
    minio_to_mongo_etl_deploy = minio_to_mongo_etl.to_deployment(
        name="MinIO to MongoDB ETL",
        cron=os.environ['CRON_SCHEDULE']
    )
    serve(minio_to_mongo_etl_deploy) 


# in case of multiple deployment
# import os
# # We import the flow not the task
# from deployment import deployment1,deployment2,deployment3, deployment4
# if __name__=="__main__":
#     deployment_1 = deployment1.to_deployment(
#         name="Deployment 1",
#         cron=os.environ['CRON_SCHEDULE_1']
#     )
#     deployment_2 = deployment2.to_deployment(
#         name="Deployment 2",
#         cron=os.environ['CRON_SCHEDULE_1']
#     )
#     deployment_3 = deployment3.to_deployment(
#         name="Deployment 3",
#         cron=os.environ['CRON_SCHEDULE_1']
#     )
#     deployment_4 = deployment4.to_deployment(
#         name="Deployment 4",
#         cron=os.environ['CRON_SCHEDULE_1']
#     )
#     serve(
#         deployment_1,
#         deployment_2,
#         deployment_3,
#         deployment_4
#     )
