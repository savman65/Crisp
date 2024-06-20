import pandas as pd

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import os

import time


storage_account_name = os.getenv('crispsa')
storage_account_key = os.getenv('crispsakey')
source_container_name = "csv"
destination_container_name = "parquet"
local_target_directory = "./blob_files/"
saPollingIntervalSeconds = 5
connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

#for local testing
#storage_account_key = ""
#storage_account_name = "crispsadsavitz"

blobRecord = []
blobsToProcessNow = []

#Download all blobs in the container
def download_blobs(storage_account_name, storage_account_key, container_name, local_target_directory):
    # Construct the BlobServiceClient using the account key
    global blobRecord
    global blobsToProcessNow
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=storage_account_key
    )

    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs()

    #for each blob in the container, if we haven't converted the blob to parquet yet, download the blob and add it to blobsToProcessNow
    for blob in blob_list:
        if blob.name not in blobRecord:
            blobsToProcessNow.append(blob.name)
            blobRecord.append(blob.name)

            blob_client = container_client.get_blob_client(blob)
            download_file_path = local_target_directory + blob.name

            print(f"Downloading blob to {download_file_path}")

            with open(download_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

            print(f"Downloaded {blob.name} to {download_file_path}")
        print(f"all blobs recorded so far: {blobRecord}")
        print(f"converting the following blobs to parquet now: {blobsToProcessNow}")

def upload_blob_to_azure(connection_string, container_name, blob_name, parquet_file_path):
    global blobRecord
    global blobsToProcessNow
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    
    with open(parquet_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

if __name__ == "__main__":
    while True:
        download_blobs(storage_account_name, storage_account_key, source_container_name, local_target_directory)

        #for every blob in blobsToProcessNow, convert the blob to parquet and upload it to the storage account
        for blob in blobsToProcessNow:
            # Read CSV file into pandas DataFrame
            blobNoExt = blob.replace(".csv", "")
            df = pd.read_csv(f"{local_target_directory}/{blobNoExt}.csv")

            df.to_parquet(f"{local_target_directory}/{blobNoExt}.parquet", engine='pyarrow')

            print(f"CSV file '{blobNoExt}.csv' converted to Parquet file '{blobNoExt}.parquet' successfully.")

            upload_blob_to_azure(connection_string, destination_container_name, f"{blobNoExt}.parquet", f"./{local_target_directory}/{blobNoExt}.parquet")

        blobsToProcessNow = []
        
        time.sleep(saPollingIntervalSeconds)














