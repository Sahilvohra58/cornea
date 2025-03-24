# # The following code is only for thew purpose of querying the already existing metadata and upload it to firestore.
# # There is no other use for this code, hence it is all commented.
#
# # pip install - -upgrade google - cloud - bigquery
# # pip install --upgrade db-dtypes
#
# # Query all PWK
# from google.cloud import bigquery
# import pandas as pd
#
# client = bigquery.Client()
#
# tables_list = ["CID_MT_ATR", "CID_MT_BEH", "CID_MT_CAT", "CID_MT_INT", "CID_MT_OFF", "CID_WK_BEH", "CID_WK_CAT",
#                "CID_WK_INT", "CID_WK_OFF"]
#
# all_tables_df = pd.DataFrame([])
# for table in tables_list:
#     print(f"for table {table}")
#     query_job = client.query(
#         f"""
#             SELECT distinct(PWK_START_DATE) FROM `lt-dia-analytics-prd-ptp.archive_zone.{table}`
#             """
#     )
#     results = query_job.result()
#     results = results.to_dataframe()
#     results = results.sort_values(by="PWK_START_DATE")
#     print(results)
#     all_tables_df[table] = results
#
# all_tables_df.to_csv("all_tables_pwk.csv", index=False)
