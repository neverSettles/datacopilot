import os
import boto3

from pathlib import Path
from botocore.exceptions import NoCredentialsError


def upload_to_aws(bucket, s3_file, local_file):
    s3 = boto3.client(service_name='s3')

    try:
        s3.upload_file(Filename=local_file, Bucket=bucket, Key=s3_file)
        print("Upload Successful")
        return True

    except FileNotFoundError:
        print("The file was not found")
        return False

    except NoCredentialsError:
        print("Credentials not available")
        return False


def download_files_from_s3_folder(bucket_name, s3_folder, local_folder):
    s3 = boto3.client(service_name='s3')
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
        s3.download_file(Bucket=bucket_name, Key=item['Key'], Filename=local_file_path)
        print(f"Downloaded {item['Key']} from {bucket_name} to {local_file_path}")

    return csv_file_names


def upload_file_to_s3(uuid: str, local_filepath: str):
    return upload_to_aws(bucket='csvlake',  s3_file=uuid + '/' + local_filepath, local_file=local_filepath)


def download_csvs_from_s3(uuid: str, local_directory_path: str):
    bucket_name = 'csvlake'  # your bucket name
    s3_folder = uuid  # your folder in the bucket, ends with '/'
    local_folder = local_directory_path + uuid  # local folder where the files will be downloaded

    Path(local_folder).mkdir(parents=True, exist_ok=True)  # ensure the local folder exists
    return download_files_from_s3_folder(bucket_name=bucket_name, s3_folder=s3_folder, local_folder=local_folder)


if __name__ == '__main__':
    uuid = '4bda6b7c-0b24-48a8-bd94-22fd072f37f2'
    local_directory_path = './downloaded/'

    file_names = download_csvs_from_s3(uuid=uuid, local_directory_path=local_directory_path)
    print('csv file names: ', file_names)

    local_filepath = './output/exp53/most_ordered_products.png'
    uploaded = upload_file_to_s3(uuid=uuid, local_filepath=local_filepath)
    print('Uploaded status: ', uploaded)
