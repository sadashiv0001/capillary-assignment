import time
import random
import requests
import csv
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File Configuration
FILE_PATH = "data.csv"  # Path to the CSV file (I have considered root directory only for now)
BATCH_SIZE = 100  # Batch size for API calls, it can be changed to any number, as per requirements  

# Capillary API endpoints
CUSTOMER_API_URL = "https://pac.intouch.capillarytech.com/add_customer"
TRANSACTION_API_URL = "https://pac.intouch.capillarytech.com/addreturn-transaction-bulk"

# Capillary API rate limit
API_RATE_LIMIT = 1000  # Maximum calls per minute, as per the Document, I have considered 1000 only

def read_csv(file_path):
    # Reads data from CSV file.
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        logger.error("File not found.")
        return []

def batch_data(data, batch_size):
    # Batch data for API calls.
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]

def ingest_data(api_url, data):
    # Ingests data using Capillary API
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=data, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

def handle_api_errors(response):
    # Handles API errors
    if response is None:
        return True  # Retry in case of request failure

    if response.status_code == 429:
        # if Rate limit exceeded, it will wait and will retry
        wait_time = random.randint(1, 5)  # Random wait time between 1 to 5 seconds
        logger.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds and retrying...")
        time.sleep(wait_time)
        return True
    elif response.status_code >= 500:
        # Server error, retry
        logger.warning("Server error. Retrying...")
        return True
    else:
        # Other errors, log and ignore
        logger.error(f"Error: {response.status_code} - {response.text}")
        return False

def main():
    # Read data from CSV file
    data = read_csv(FILE_PATH)
    total_records = len(data)
    logger.info(f"Total records to ingest: {total_records}")

    # Batch and ingest data
    successful_records = 0
    failed_records = 0

    for batch in batch_data(data, BATCH_SIZE):
        # Ingestion data in batches
        response = ingest_data(CUSTOMER_API_URL, batch)  # For customers
        if handle_api_errors(response):
            continue

        response_json = response.json()
        successful_records += response_json.get('success_count', 0)
        failed_records += response_json.get('failed_count', 0)

        # Throttle the API calls to stay within rate limit
        time.sleep(60 / API_RATE_LIMIT)  # Sleep for 1 minute / API_RATE_LIMIT

    logger.info("Ingestion process completed.")
    logger.info(f"Successful records: {successful_records}")
    logger.info(f"Failed records: {failed_records}")

if __name__ == "__main__":
    main()
