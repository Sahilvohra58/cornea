# # The following code is only for thew purpose of querying the already existing metadata and upload it to firestore.
# # There is no other use for this code, hence it is all commented.
#
# import pandas as pd
# from datetime import datetime
# from google.cloud import firestore
# import json
# from google.cloud import storage
# import gcsfs
#
# fs = gcsfs.GCSFileSystem(project='lt-dia-analytics-exp-ptp')
# env = "prd"
# bucket_name = f"{env}-ptp-dagrun-metadata"
# storage_client = storage.Client()
# bucket = storage_client.bucket(bucket_name)
# blobs_names = [blob.name for blob in storage_client.list_blobs(bucket_name)]
# parsed_data = {}
# df = pd.DataFrame(data=[])
# dags_list = ["archive_hub_mt", "archive_hub_wk", "archive_zone_static_purge"]
#
# for blob_name in blobs_names:
#     # if blob_name.startswith(tuple(dags_list)):
#     metadata_list = blob_name.split("/")
#     if len(metadata_list) == 3:
#         dag_name, run_state, file_name = metadata_list
#         run_datetime = datetime.strptime(file_name.split(".")[0], '%Y%m%dT%H%M%S')
#         run_datetime_date_str = run_datetime.date().strftime("%Y/%m/%d")
#         run_datetime_str = file_name.split(".")[0]
#         if not parsed_data.get(run_datetime_date_str):
#             parsed_data[run_datetime_date_str] = {}
#
#         if not parsed_data[run_datetime_date_str].get(dag_name):
#             parsed_data[run_datetime_date_str][dag_name] = {}
#
#         if not parsed_data[run_datetime_date_str][dag_name].get(run_state):
#             parsed_data[run_datetime_date_str][dag_name][run_state] = []
#
#         #     parsed_data[dag_name]["success"] = {}
#         #     parsed_data[dag_name]["failed"] = {}
#         parsed_data[run_datetime_date_str][dag_name][run_state].append({"start_time": run_datetime_str,
#                                                                         "end_time": None})
#         # parsed_data[run_datetime_date_str][dag_name][run_state]["start_time"] = run_datetime_str
#         # parsed_data[run_datetime_date_str][dag_name][run_state]["end_time"] = None
# print(parsed_data)
#
#
# env = "exp"
# log_bucket = f"{env}-ptp-logging-monitoring"
# bucket = storage.Client().get_bucket(log_bucket)
# db = firestore.Client(project="lt-dia-analytics-exp-ptp", database="cornea")
#
# # #  For Cloud Backup
# # metadata_file_path = f"dag_run_metadata.json"
# # blob = bucket.blob(metadata_file_path)
# # blob.upload_from_string(
# #     data=json.dumps(parsed_data),
# #     content_type='application/json'
# # )
#
# # #  For Local Backup
# # with open(f"dag_run_metadata.json", "w") as outfile:
# #     json.dump(parsed_data, outfile)
#
# for date in parsed_data:
#     for dag in parsed_data[date]:
#         for run_state in parsed_data[date][dag]:
#             db.collection(
#                 "dag_run_metadata"
#             ).document(
#                 "dag_status_and_time"
#             ).collection(
#                 date.replace("/", "-")
#             ).document(
#                 dag
#             ).set(
#                 {run_state: parsed_data[date][dag][run_state]}
#             )
#
