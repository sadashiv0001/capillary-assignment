# Data Ingestion Script

## Overview

The Data Ingestion Script is a Python script designed to facilitate the migration of data from a CSV file to Capillary's CRM platform using their REST APIs. It reads data from a CSV file, batches it, and sends it to the Capillary APIs for ingestion. The script handles API rate limiting, retries on failures, and provides detailed logging for monitoring and troubleshooting.

## Features

- Reads data from a CSV file.
- Batches data for API calls to Capillary CRM.
- Handles API rate limiting to stay within the specified rate limit.
- Retries failed API calls based on specified error conditions.
- Provides detailed logging for monitoring and troubleshooting.

## Requirements

- Python 3.x
- `requests` library
- CSV file with data to be ingested
- Access to Capillary's CRM platform and API endpoints

## Usage

1. Install Python 3.x on your system if not already installed.
2. Install the `requests` library using `pip install requests`.
3. Prepare a CSV file with the data to be ingested. Ensure that the CSV file has the required fields and formatting as per the Capillary API documentation.
4. Update the script with the correct file path (`FILE_PATH`) and API endpoints (`CUSTOMER_API_URL`, `TRANSACTION_API_URL`) if necessary.
5. Run the script using `python data_ingestion.py`.

## Configuration

- `FILE_PATH`: Path to the CSV file containing the data to be ingested.
- `BATCH_SIZE`: Batch size for API calls. Adjust this value based on the API rate limit and the size of the data.
- `CUSTOMER_API_URL`: API endpoint for adding customer data to Capillary CRM.
- `TRANSACTION_API_URL`: API endpoint for adding transaction data to Capillary CRM.
- `API_RATE_LIMIT`: Maximum number of API calls allowed per minute.

## Logging

The script uses logging to provide information, warnings, and errors during execution. Logs are output to the console, allowing users to monitor the progress of data ingestion and identify any issues that may arise.

## Error Handling

The script includes error handling mechanisms to deal with various scenarios such as file not found, API rate limiting, and API call failures. Error messages are logged, and the script attempts retries as appropriate to minimize data loss and ensure successful ingestion.

## Conclusion

The Data Ingestion Script simplifies the process of migrating data to Capillary's CRM platform by automating the ingestion process and handling common issues that may arise during data transfer. With its configurable options and robust error handling, the script provides a reliable solution for efficiently managing data migration tasks.
