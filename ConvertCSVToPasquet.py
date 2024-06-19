import pandas as pd

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import os

def download_blob_container(storage_account_name, storage_account_key, container_name, local_target_directory):
    # Construct the BlobServiceClient using the account key
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=storage_account_key
    )

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # List all blobs in the container
    blob_list = container_client.list_blobs()

    # Download each blob to local directory
    for blob in blob_list:
        blob_client = container_client.get_blob_client(blob)
        download_file_path = local_target_directory + blob.name

        print(f"Downloading blob to {download_file_path}")

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print(f"Downloaded {blob.name} to {download_file_path}")

if __name__ == "__main__":
    # Replace with your own Azure Storage Account details
    storage_account_name = "crispsadsavitz"
    storage_account_key = os.getenv('sakey')
    container_name = "crisp"
    local_target_directory = "./downloaded_files/"

    # Call the function to download the container
    download_blob_container(storage_account_name, storage_account_key, container_name, local_target_directory)




# Read CSV file into pandas DataFrame
csv_file = './downloaded_files/crisp.csv'
df = pd.read_csv(csv_file)

# Specify the output Parquet file
parquet_file = 'crisp.parquet'

# Option 1: Using pyarrow for Parquet writing
# Ensure to have pyarrow installed: pip install pyarrow
df.to_parquet(parquet_file, engine='pyarrow')

# Option 2: Using fastparquet for Parquet writing
# Ensure to have fastparquet installed: pip install fastparquet
# df.to_parquet(parquet_file, engine='fastparquet')

print(f"CSV file '{csv_file}' converted to Parquet file '{parquet_file}' successfully.")

def upload_parquet_to_azure(connection_string, container_name, parquet_blob_name, parquet_file_path):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(parquet_blob_name)
    
    with open(parquet_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

connection_string = f"DefaultEndpointsProtocol=https;AccountName=crispsadsavitz;AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
parquet_blob_name = "crisp.parquet"

upload_parquet_to_azure(connection_string, container_name, parquet_blob_name, "./crisp.parquet")














