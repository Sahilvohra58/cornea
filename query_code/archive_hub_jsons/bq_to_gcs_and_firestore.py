# # The following code is only for thew purpose of querying the already existing metadata and upload it to firestore.
# # There is no other use for this code, hence it is all commented.
#
# import json
# import pandas as pd
# from google.cloud import storage
# from google.cloud import bigquery
#
# client = bigquery.Client()
# df = pd.read_csv("all_tables_pwk.csv")
#
# # "CID_MT_ATR", "CID_MT_BEH", "CID_MT_CAT", "CID_WK_BEH", "CID_WK_CAT",
# # "CID_MT_INT", "CID_MT_OFF", "CID_WK_INT", "CID_WK_OFF" - nan pwk start dates!!!
# tables_list = ["CID_MT_ATR", "CID_MT_BEH", "CID_MT_CAT", "CID_WK_BEH", "CID_WK_CAT", "CID_MT_INT", "CID_MT_OFF",
#                "CID_WK_INT", "CID_WK_OFF"]
# for table in tables_list:
#     table_dict = {}
#     for date in df[table]:
#         if type(date) == str:
#             query = f"""
#             SELECT
#             FEATURE.key as feature_key, min(FEATURE.value) as min_value,
#             max(FEATURE.value) as max_value, avg(FEATURE.value) as avg_value,
#             stddev(FEATURE.value) as std_value
#             FROM `lt-dia-analytics-prd-ptp.archive_zone.{table}`, UNNEST (FEATURES.key_value) as FEATURE
#             WHERE PWK_START_DATE = "{date}" GROUP BY feature_key
#             """
#
#             query_job = client.query(query)
#             results = query_job.result()
#             results = results.to_dataframe()
#             results = results.set_index("feature_key")
#             table_date_dict = {}
#             for index, row in results.iterrows():
#                 table_date_dict[index] = {
#                     "min_value": row["min_value"],
#                     "max_value": row["max_value"],
#                     "avg_value": row["avg_value"],
#                     "std_value": row["std_value"]
#                 }
#
#             table_dict[date] = table_date_dict
#
#     with open(f"archive_hub_jsons/{table}.json", "w") as outfile:
#         json.dump(table_dict, outfile)
#
#     writing_env = "exp"
#     log_bucket = f"{writing_env}-ptp-logging-monitoring"
#     bucket = storage.Client().get_bucket(log_bucket)
#
#     metadata_file_path = f"archive_hub_jsons/{table}.json"
#     blob = bucket.blob(metadata_file_path)
#     blob.upload_from_string(
#         data=json.dumps(table_dict),
#         content_type='application/json'
#     )
############################################################################################################
# from google.cloud import firestore
# from google.cloud import storage
# import json
#
# # Instantiate a Google Cloud Storage client and specify required bucket and file
# storage_client = storage.Client()
# log_bucket = f"exp-ptp-logging-monitoring"
# bucket = storage_client.get_bucket(log_bucket)
# tables_list = ["CID_WK_CAT", "CID_MT_INT", "CID_MT_OFF",
#                "CID_WK_INT", "CID_WK_OFF", "CID_MT_ATR", "CID_WK_BEH", "CID_MT_BEH", "CID_MT_CAT"]
# db = firestore.Client(project="lt-dia-analytics-exp-ptp", database="cornea")
#
# for table in tables_list:
#     print(f"for table = {table}")
#     blob = bucket.blob(f"archive_hub_jsons/{table}.json")
#     data = json.loads(blob.download_as_string(client=None))
#
#     # doc_ref_table = db.collection("archive_zone").document(table)
#     for date in data.keys():
#         print(f"for date = {date}")
#         doc_ref_date = db.collection(f"archive_zone/{table}/{date}")
#         for feature in data[date].keys():
#             print(f"for feature = {feature}")
#             doc_ref_date.document(feature).set(data[date][feature])

############################################################################################################
# from google.cloud import firestore
# from google.cloud import storage
# import json
#
# # Instantiate a Google Cloud Storage client and specify required bucket and file
# storage_client = storage.Client()
# log_bucket = f"exp-ptp-logging-monitoring"
# bucket = storage_client.get_bucket(log_bucket)
# tables_list = ["CID_WK_BEH"]
# db = firestore.Client(project="lt-dia-analytics-exp-ptp", database="cornea")
#
# for table in tables_list:
#     print(f"for table = {table}")
#     blobs = list(bucket.list_blobs(prefix=f"temp_folder/archive_hub_features/{table}"))
#     for blob in blobs:
#         if blob.name.endswith("/insights_dict.json"):
#             split_name = blob.name.split("/")
#             date = split_name[3]
#             feature = split_name[4]
#             insights_data = json.loads(blob.download_as_string(client=None))
#             doc_ref = db.document(f"archive_zone/{table}/{date}/{feature}")
#             dict_doc = doc_ref.get().to_dict()
#             for key in insights_data.keys():
#                 if key == "histogram_bins":
#                     insights_data[key] = {"x_axis": insights_data[key][0],
#                                           "y_axis": insights_data[key][1]}
#                 dict_doc[key] = insights_data[key]
#
#             table_collection = db.collection(f"archive_zone/{table}/{date}")
#             doc_ref = table_collection.document(feature)
#             doc_ref.set(dict_doc)
