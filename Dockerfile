FROM python:3.9-slim

RUN pip3 install pandas pyarrow fastparquet
RUN pip3 install azure-storage-blob

WORKDIR /app

COPY . /app

RUN chmod u+x ./ConvertCSVToPasquet.py

CMD ["python", "./ConvertCSVToPasquet.py"]