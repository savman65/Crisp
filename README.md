# Crisp App

## Assumptions:

## Usage: 
Navigate to https://github.com/savman65/Crisp/actions/workflows/crisp.yml for the github action which deploys the required azure infrastructure (storage account, acr, and aks), builds and pushes the python docker image, and then deploys the python app to kubernetes.

For the next part you'll need a sas key to the storage account key (shared in my email)

The following script will copy a csv file to the storage account using azcopy, then it will use azcopy again to retrieve the corresponding parquet file

###MAC instructions:
it is assumed you have brew installed on your mac. 

```
brew install az
brew install azcopy
```

Please replace <your-storage-account-key> with the storage account key that I sent you
Please create a csv file and cd to its directory. Replace <csvFile> with the name of the csv file (ex: test.csv). Then run the following code

```
saskey="<your-storage-account-key>"
csvFile="<csvFile>"

azcopy copy "$csvFile" "https://crispsadsavitz.blob.core.windows.net/csv/$csvFile?$saskey"
echo "the following is the list of csv files"
az storage blob list --account-name crispsadsavitz --container-name csv --output table
echo "sleeping for 10 seconds for parquet processing..."
sleep 10
echo "the following is the list of parquet files"
parquetFile=$(echo $csvFile | sed s/csv/parquet/g)
az storage blob list --account-name crispsadsavitz --container-name parquet --output table
azcopy copy "https://crispsadsavitz.blob.core.windows.net/parquet/$parquetFile?$saskey" .

```


## Python image description:
The python image is a script running on an infinite loop that polls the storage account on a specified interval, then uses a simple name comparison to assess if new csv blobs have been added to the storage account's "csv" container, at which point it will convert those new csv blobs to parquet and then push the parquet blobs up to the storage account's "parquet" container.

Note: the blob_files directory (which is a script dependancy) contains a placeholder file because without it, the folder wouldn't get copied to the container

## Some Todo items I thought of
- an "event-based" trigger for the application to do parquet conversions so we can remove the naiive logic in the python script
- harden the azure resources (locking down networking, least privilege for service accounts, etc)
- better documentation
- clean up git commits
- standardize naming conventions, use better naming convention
- create the blob_files folder dynamically
- persistent storage for a history of blobs that were processed
- ignore non csv blobs
- error handling for graceful termination for ConvertCSVToPasquet
- make external user script more robust


## Notes
The commits in the git repo come from an author named "Matt Savitz". I'm on vacation now so I'm using my father (Matt's) laptop :)