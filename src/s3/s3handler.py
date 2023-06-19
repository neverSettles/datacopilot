import boto3
import os

from pathlib import Path

from botocore.exceptions import NoCredentialsError

def upload_to_aws(bucket, s3_file, local_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def upload_image_to_s3(uuid, image_filename):
    return upload_to_aws('csvlake',  uuid + '/' + image_filename, image_filename)

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
        csv_file_names.append(str(file_name))
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

if __name__ == '__main__':
    file_names = download_csvs_from_s3('4bda6b7c-0b24-48a8-bd94-22fd072f37f2')
    print('csv file names: ' + str(file_names))


    uploaded = upload_image_to_s3('4bda6b7c-0b24-48a8-bd94-22fd072f37f2', './output/exp53/most_ordered_products.png')
    print('uploaded status: ' + str(uploaded))