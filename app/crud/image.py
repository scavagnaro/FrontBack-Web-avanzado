import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import io

import os
from dotenv import load_dotenv

from fastapi import UploadFile

load_dotenv()


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")


async def upload_image(
    file: UploadFile,
    bucket_name="xtremely-cool-bucket-rahub96d6mcm43pa7pwgjffj3g586use1a-s3alias",
):
    try:
        s3 = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
        file_content = await file.read()
        file_obj = io.BytesIO(file_content)
        s3.upload_fileobj(file_obj, bucket_name, file.filename)
        return f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"
    except FileNotFoundError:
        return "The file was not found."
    except NoCredentialsError:
        return "Credentials not available."
    except PartialCredentialsError:
        return "Incomplete credentials provided."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    with open("app/crud/test.png", "rb") as file:
        print(upload_image(file))
