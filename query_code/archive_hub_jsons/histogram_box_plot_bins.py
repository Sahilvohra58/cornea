# The following code is only for thew purpose of querying the already existing metadata and upload it to firestore.
# There is no other use for this code, hence it is all commented.

from datetime import datetime
from google.cloud import firestore
from google.cloud import bigquery

client = bigquery.Client()

firestore_client = firestore.Client(project="lt-dia-analytics-exp-ptp", database="cornea")

tables_list = ["CID_WK_CAT", "CID_MT_ATR", "CID_MT_BEH", "CID_MT_CAT", "CID_WK_BEH", "CID_MT_INT", "CID_MT_OFF",
               "CID_WK_INT", "CID_WK_OFF"]

for table_id in tables_list:
    query_all_pwk = client.query(
        f"""
        SELECT distinct(PWK_START_DATE)
        FROM `lt-dia-analytics-prd-ptp.archive_zone.{table_id}`
        """
    )
    results = query_all_pwk.result()
    results = results.to_dataframe()
    results = results.dropna()
    pwk_date_list = [
        datetime.strftime(x, "%Y-%m-%d") for x in results.sort_values(by="PWK_START_DATE")["PWK_START_DATE"]
    ]
    print(f"Got dates {pwk_date_list}")
    for pwk_date in pwk_date_list:
        # if isinstance(pwk_date, str):
        query_job = client.query(
            f"""
            SELECT FEATURE.key as feature_key, APPROX_QUANTILES(FEATURE.value, 20) as percentile_bins
            FROM `lt-dia-analytics-prd-ptp.archive_zone.{table_id}`,
            UNNEST (FEATURES.key_value) as FEATURE
            WHERE PWK_START_DATE = "{pwk_date}" GROUP BY feature_key
            """
        )
        results = query_job.result()
        results = results.to_dataframe()
        table_collection = firestore_client.collection(f"archive_zone/{table_id}/{pwk_date}")

        for idx, row in results.iterrows():
            doc = table_collection.document(row["feature_key"])
            doc_dict = doc.get().to_dict()
            updated_dict = {} if not doc_dict else doc_dict
            updated_dict["percentile_bins"] = list(row["percentile_bins"])
            doc.set(updated_dict)
        print(f"{table_id}/{pwk_date}")
        break
