import requests
import boto3
import pytz
import os
from datetime import datetime
import uuid
from botocore.exceptions import ClientError

# Retrieve API Key and AWS Credentials from environment variables for added security
api_key = os.getenv("COINBASE_API_KEY")  # Set your API key securely in environment variables
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

if not api_key or not aws_access_key or not aws_secret_key:
    raise ValueError("API key or AWS credentials are not set. Please configure your environment.")

region_name = 'us-east-1'
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).isoformat()

table_name = 'bitcoin_price_storer'
api_url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

# Use Boto3 to connect with DynamoDB using credentials from environment variables or IAM role
dynamodb = boto3.client('dynamodb', region_name=region_name, 
                        aws_access_key_id=aws_access_key, 
                        aws_secret_access_key=aws_secret_key)

def put_item_to_dynamodb(item):
    try:
        dynamodb.put_item(TableName=table_name, Item=item)
    except ClientError as e:
        print(f"Error inserting item to DynamoDB: {e}")
        raise

def fetch_bitcoin_price():
    try:
        response = requests.get(api_url, headers={'Authorization': f'Bearer {api_key}'})
        response.raise_for_status()  # Raise exception for bad status codes (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        raise

def main():
    try:
        data = fetch_bitcoin_price()
        data_to_ingest = {
            "amount": {"S": data["data"]["amount"]},
            "base": {"S": data["data"]["base"]},
            "currency": {"S": data["data"]["currency"]},
            "timestamp": {"S": current_time},
            "uuid": {"S": str(uuid.uuid4())}
        }
        put_item_to_dynamodb(data_to_ingest)
        print(f'Item {data_to_ingest} added to DynamoDB table {table_name}.')
        print('Data transfer complete.')
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
