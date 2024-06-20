Documentation
# Crisp App
Description: 
navigate to https://github.com/savman65/Crisp/actions/workflows/crisp.yml for the github action which:
deploys azure infrastructure, builds and pushes the python docker image, and then deploys it to kubernetes

the python image is a script running on an infinite loop polls the storage account on a specified interval, then uses a simple name comparison to assess if new csv blobs have been added to the storage account's "csv" container, at which point it will convert those new csv blobs to parquet and then push the parquet blobs up to the storage account's "parquet" container


kubectl exec -it crisp-6989776775-bmj6m -- /bin/sh

