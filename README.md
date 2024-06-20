# Crisp App

## Usage:
Navigate to https://github.com/savman65/Crisp/actions/workflows/crisp.yml to run the github action which:
- Deploys the required azure infrastructure (storage account, acr, and aks)
- Builds and pushes the python docker image
- Deploys the python app to kubernetes
- Runs a test by pushing a sample csv to the storage account and then verifies that it can download the corresponding parquet file

## External User Test
The following is a test that you can perform with your own csv on your local machine. The script below will copy a csv file to the storage account using azcopy, then it will use azcopy again to retrieve the corresponding parquet file (generated by the application)

You'll need a sas key to the storage account key (shared in my email)

### MAC instructions:
it is assumed you have brew installed on your mac. 

```
brew install az
brew install azcopy
```

### Windows Instructions
ToDo
https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10

### Test Script
- Please replace 'your-storage-account-key' below with the storage account key that I sent you.
- Please create a csv file and cd to its directory. Replace 'csvFile' below with the name of the csv file (ex: test.csv). Then run the following code

```
#Variables for you to update
saskey="your-storage-account-key"
csvFile="csvFile"

#The script. Do not edit
crispsa="crispsadsavitz"
azcopy copy "$csvFile" "https://$crispsa.blob.core.windows.net/csv/$csvFile?$saskey"
echo "the following is the list of csv files"
az storage blob list --account-name $crispsa --container-name csv --output table
echo "sleeping for 10 seconds for parquet processing..."
sleep 10
echo "the following is the list of parquet files"
parquetFile=$(echo $csvFile | sed s/csv/parquet/g)
az storage blob list --account-name $crispsa --container-name parquet --output table
azcopy copy "https://$crispsa.blob.core.windows.net/parquet/$parquetFile?$saskey" .

```

## Some Todo Items I Thought Of
- An "event-based" trigger for the application to do parquet conversions to replace the naiive "polling" logic used python script
- Harden azure/github resources (locking down networking, least privilege for service accounts, etc)
- Better documentation
- Clean up git commits
- Standardize naming conventions and use better ones too
- Create the blob_files folder dynamically
- Persistent storage for a history of blobs that were processed
- Ignore non-csv blobs
- Error handling for graceful termination for ConvertCSVToPasquet.py
- Make the external user script above more robust


## Notes
- The commits in this repo come from an author named "Matt Savitz". I'm on vacation now so I'm using my father's (Matt) laptop :)
- The only resource that isn't managed in the github workflow is the service principle used for github to authenticate to azure. This is to avoid a "chicken and egg" problem. The deployment to azure depends on the service principle.
- The blob_files directory (which is a script dependency) contains a placeholder file because without it, the folder wouldn't get copied to the container
