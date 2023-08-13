import pandas as pd
import os
import boto3
from multiprocessing import Pool


def process_file(file):
    # AWS Setup
    s3 = boto3.client('s3')
    bucket = os.environ.get('BUCKET_NAME')  # Replace with your bucket name

    # Read the gzipped CSV into a DataFrame
    df = pd.read_csv(
        os.path.join(os.environ.get('NYSE_DATA_DIR'), file),
        compression='gzip',
        header=None,
        names=['ticker', 'trade_date', 'open', 'high', 'low', 'close', 'volume']
    )

    # Assuming trade_date is in the format YYYY-MM-DD
    # Extract unique dates in that file
    unique_dates = df['trade_date'].unique()

    # Save to separate files based on the unique date
    for trade_date in unique_dates:
        date_df = df[df['trade_date'] == trade_date]

        # Convert the DataFrame to CSV content
        csv_content = date_df.to_csv(index=False)

        # Define the key (path) in the S3 bucket
        key = f'nyse_all/nyse_data/NYSE_{trade_date}.csv'

        # Upload the CSV content to S3
        s3.put_object(Body=csv_content, Bucket=bucket, Key=key, ContentType='text/csv')


if __name__ == '__main__':
    # Assuming you have a list of files in the format 'NYSE_YYYY.txt.gz'
    files = os.listdir(os.environ.get('NYSE_DATA_DIR'))
    files = [f for f in files if f.startswith('NYSE_') and f.endswith('.txt.gz')]

    # Process files concurrently
    # Adjust the number of processes based on your CPU and tasks
    with Pool(processes=4) as pool:
        pool.map(process_file, files)
