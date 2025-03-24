# # The following code is only for thew purpose of querying the already existing metadata and upload it to firestore.
# # There is no other use for this code, hence it is all commented.
#
# import pandas as pd
# from google.cloud import firestore
# import json
# from google.cloud import storage
# import gcsfs
# from datetime import datetime
# import re
#
# reading_env = "prd"
# fs = gcsfs.GCSFileSystem(project=f'lt-dia-analytics-{reading_env}-ptp')
# bucket_name = f"{reading_env}-ptp-logging-monitoring"
# storage_client = storage.Client()
# bucket = storage_client.bucket(bucket_name)
# blobs_names = [blob.name for blob in storage_client.list_blobs(bucket_name)]
# regex_float = "[+-]?[0-9]+\.[0-9]+"
# regex_int = "[+-]?[0-9]+"
#
# parsed_data = {}
# df = pd.DataFrame(data=[])
# for blob_name in blobs_names:
#     if blob_name.startswith(f"validation_metadata_logs/"):
#         print(blob_name)
#         log_date_str = datetime.strptime("-".join(blob_name.split("/")[1:4]), "%Y-%m-%d").strftime("%Y-%m-%d")
#         landing_id = "_".join(blob_name.split("/")[-1].split("_")[:3])
#         validation_df = pd.read_csv(f"gs://{bucket_name}/{blob_name}")
#         null_count_dict_df = validation_df.set_index(validation_df.columns[0])['null_count'].to_dict()
#         min_values_dict_df = validation_df.set_index(validation_df.columns[0])['min_values'].to_dict()
#         max_values_dict_df = validation_df.set_index(validation_df.columns[0])['max_values'].to_dict()
#         row_count = str(validation_df["row_count"][:1][0])
#
#         for column_name in null_count_dict_df.keys():
#             if not column_name.endswith(".KEY"):
#                 split_column_name = column_name.split(".array")[0] if ".array" in column_name else column_name
#                 if landing_id not in parsed_data.keys():
#                     parsed_data[landing_id] = {}
#                 if log_date_str not in parsed_data[landing_id].keys():
#                     parsed_data[landing_id][log_date_str] = {}
#
#                 if split_column_name not in parsed_data[landing_id][log_date_str].keys():
#                     parsed_data[landing_id][log_date_str][split_column_name] = {}
#
#                 if null_count_dict_df[column_name] != 0:
#                     parsed_data[landing_id][log_date_str][split_column_name][
#                         "null_values_count"
#                     ] = null_count_dict_df[column_name]
#
#                 min_value, max_value = str(min_values_dict_df[column_name]), str(max_values_dict_df[column_name])
#                 if (
#                         re.search(regex_float, min_value) or re.search(regex_int, min_value)
#                 ) and (
#                         re.search(regex_float, max_value) or re.search(regex_int, max_value)
#                 ):
#                     parsed_data[landing_id][log_date_str][split_column_name][
#                         "min_values_count"
#                     ] = min_values_dict_df[column_name]
#                     parsed_data[landing_id][log_date_str][split_column_name][
#                         "max_values_count"
#                     ] = max_values_dict_df[column_name]
#
#                 parsed_data[landing_id][log_date_str][split_column_name]["row_count"] = row_count
#
# writing_env = "exp"
# log_bucket = f"{writing_env}-ptp-logging-monitoring"
# bucket = storage.Client().get_bucket(log_bucket)
#
# db = firestore.Client(project="lt-dia-analytics-exp-ptp", database="cornea")
#
# for landing_id in parsed_data.keys():
#     print(f"for landing id = {landing_id}")
#     # For Cloud Backup
#     metadata_file_path = f"metadata_jsons/{landing_id}.json"
#     blob = bucket.blob(metadata_file_path)
#     blob.upload_from_string(
#         data=json.dumps(parsed_data[landing_id]),
#         content_type='application/json'
#     )
#
#     # #  For Local Backup
#     # with open(f"metadata_jsons/{landing_id}.json", "w") as outfile:
#     #     json.dump(parsed_data[landing_id], outfile)
#     #
#     for date_str in parsed_data[landing_id].keys():
#         doc_ref = db.collection(f"landing_zone/{landing_id}/{date_str}")
#         for column_name in parsed_data[landing_id][date_str].keys():
#             doc_ref.document(column_name).set(parsed_data[landing_id][date_str][column_name])
