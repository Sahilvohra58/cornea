import pandas as pd
from datetime import datetime
import json
from google.cloud import storage
import gcsfs

fs = gcsfs.GCSFileSystem(project='lt-dia-analytics-exp-ptp')
bucket_name = "exp-ptp-logging-monitoring"
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blobs_names = [blob.name for blob in storage_client.list_blobs(bucket_name)]

# landing_folder = "grocery_behavior_wk"

parsed_data = {}
df = pd.DataFrame(data=[])
for blob_name in blobs_names:
    if blob_name.startswith(f"validation_metadata_logs/"):
        log_date_str = "/".join(blob_name.split("/")[1:4])
        landing_id = "_".join(blob_name.split("/")[-1].split("_")[:3])
        validation_df = pd.read_csv(f"gs://{bucket_name}/{blob_name}")
        null_count_dict_df = validation_df.set_index(validation_df.columns[0])['null_count'].to_dict()
        min_values_dict_df = validation_df.set_index(validation_df.columns[0])['min_values'].to_dict()
        max_values_dict_df = validation_df.set_index(validation_df.columns[0])['max_values'].to_dict()

        for key in null_count_dict_df:
            if not key.endswith(".KEY"):
                if landing_id not in parsed_data.keys():
                    parsed_data[landing_id] = {}
                if log_date_str not in parsed_data[landing_id].keys():
                    parsed_data[landing_id][log_date_str] = {"null_values_count": {},
                                                             "min_values_count": {},
                                                             "max_values_count": {}}
                parsed_data[landing_id][log_date_str]["null_values_count"][key] = null_count_dict_df[key]
                if isinstance(min_values_dict_df[key], str) and isinstance(max_values_dict_df[key], str):
                    parsed_data[landing_id][log_date_str]["min_values_count"][key] = min_values_dict_df[key]
                    parsed_data[landing_id][log_date_str]["max_values_count"][key] = max_values_dict_df[key]

        parsed_data[landing_id][log_date_str]["row_count"] = str(validation_df["row_count"][:1][0])

for key in parsed_data.keys():
    with open(f"metadata_jsons/{key}.json", "w") as outfile:
        json.dump(parsed_data[key], outfile)
