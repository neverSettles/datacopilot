import boto3
import os

from pathlib import Path

def download_files_from_s3_folder(bucket_name, s3_folder, local_folder):
    s3 = boto3.client('s3')
    result = s3.list_objects(Bucket=bucket_name, Prefix=s3_folder)
    
    if 'Contents' not in result:
        err = f"No objects available in {s3_folder} of {bucket_name}."
        print(err)
        return err
    
    csv_file_names = []

    for item in result['Contents']:
        file_name = os.path.basename(item['Key'])
        csv_file_names.append(file_name)
        local_file_path = os.path.join(local_folder, file_name)
        s3.download_file(bucket_name, item['Key'], local_file_path)
        print(f"Downloaded {item['Key']} from {bucket_name} to {local_file_path}")
    
    return csv_file_names

def download_csvs_from_s3(uuid):
    bucket_name = 'csvlake'  # your bucket name
    s3_folder = uuid  # your folder in the bucket, ends with '/'
    local_folder = './downloaded/' + uuid  # local folder where the files will be downloaded

    Path(local_folder).mkdir(parents=True, exist_ok=True) # ensure the local folder exists
    return download_files_from_s3_folder(bucket_name, s3_folder, local_folder)

