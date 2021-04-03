import boto3
import cv2



SRC_FILE_PATH = r'C:\Users\Raghav Gupta\Downloads\vimal_sir.jfif'
DEST_FILE_PATH = 'vimal_sir.jpeg'

REGION_NAME = 'ap-south-1'

S3_BUCKET_NAME = 'ai-on-aws-02'
S3_KEY_NAME = 'file1.jpeg'

from utils.aws_helper import get_aws_service_client,aws_rek_detect_labels
    
CREDENTIAL_FILE_PATH = r'D:\c_data\ARTH\TASKS\AI_ON_AWS\ai_aws_user.csv'


rek = get_aws_service_client('rekognition',credential_file_path=CREDENTIAL_FILE_PATH)['client']

s3 = get_aws_service_client('s3',credential_file_path=CREDENTIAL_FILE_PATH)['client']

print(aws_rek_detect_labels(rek,S3_BUCKET_NAME,S3_KEY_NAME,s3_client=s3,upload_file_path=DEST_FILE_PATH ))




# # get the image


# image = cv2.imread(SRC_FILE_PATH)

# # saving the image

# cv2.imwrite(DEST_FILE_PATH, image)



