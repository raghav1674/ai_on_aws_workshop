
from utils.load_credentials import load_aws_credentials


def get_aws_service_client(service_name, region='ap-south-1', credential_file_path=None, access_key=None, secret_key=None):

    try:
        from boto3 import client
        from os import getenv

        aws_access_key_id = None
        aws_secret_access_key = None

        if credential_file_path:

            credentials_data = load_aws_credentials(credential_file_path)
            if credentials_data['success']:
                aws_access_key_id = credentials_data['access_key']
                aws_secret_access_key = credentials_data['secret_key']

        client = client(
            service_name,
            region,
            aws_access_key_id=aws_access_key_id or access_key or getenv(
                'ACCESS_KEY'),
            aws_secret_access_key=aws_secret_access_key or secret_key or getenv(
                'SECRET_KEY')
        )
        return {'success': 1, 'service': service_name, 'client': client}

    except ImportError as err:
        return {'sucess': 0, 'error': err, 'client': None}
    except Exception as err:
        return {'success': 0, 'service': service_name, 'error': err, 'client': None}


def create_s3_bucket(client, bucket_name, region):

    try:
        response = client.create_bucket(

            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region,
            },
        )

        return {'success': 1, 'response': f'Bucket {bucket_name} created in {region} successfully.'}
    except Exception as e:
        return {'success': 0, 'error': e}


def aws_rek_detect_labels(client, bucket_name, key, s3_client=None, create_new=False, upload_file_path=None, region='ap-south-1', min_confidence=70, max_labels=6):

    try:
        if create_new:
            res = create_s3_bucket(s3_client, bucket_name,
                                   region)
            if not res['success']:
                raise Exception(res['error'])
        if upload_file_path:
            s3_client.upload_file(upload_file_path, bucket_name, key)
        else:
            raise Exception(
                'Path of the file which is to be uploaded is not provided')

        response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': key,
                }
            },
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
        return {'success': 1, 'response': response}
    except Exception as e:
        return {'success': 0, 'response': e}

