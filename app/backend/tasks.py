__author__ = "Richard Correro (richard@richardcorrero.com)"

import io
import os
import zipfile
from datetime import datetime, timedelta
from typing import Iterable, List, Optional

from google.cloud import storage


def _backend_task(
    filenames: Iterable[str], gcs_creds_path: str, bucket_name: str, 
    blob_name: str, content_type: Optional[str] = 'application/zip', 
    exp_minutes: Optional[int] = 60
) -> str:
    def get_zip_as_bytes(filenames: Iterable[str]) -> io.BytesIO:
        # Create a BytesIO instance with the .zip file
        zip_file_data = io.BytesIO()
        with zipfile.ZipFile(zip_file_data, 'w') as zipf:
            for filename in filenames:
                zipf.write(filename)
        zip_file_data.seek(0)
        return zip_file_data

    def upload_file_to_gcs(
            zip_file_data: io.BytesIO, gcs_creds_path: str, bucket_name: str, 
            blob_name: str, content_type: Optional[str] = 'application/zip',
            exp_minutes: Optional[int] = 60
    ) -> str:
        # Upload the .zip file to GCS with authentication
        client = storage.Client.from_service_account_json(gcs_creds_path)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_file(zip_file_data, content_type=content_type)

        # Generate a signed URL with expiration time
        expiration_time = datetime.utcnow() + timedelta(minutes=exp_minutes)
        signed_url = blob.generate_signed_url(expiration=expiration_time, method='GET')

        return signed_url
    
    zip_file_data: io.BytesIO = get_zip_as_bytes(filenames=filenames)
    signed_url: str = upload_file_to_gcs(
        zip_file_data=zip_file_data, gcs_creds_path=gcs_creds_path, 
        bucket_name=bucket_name, blob_name=blob_name, content_type=content_type,
        exp_minutes=exp_minutes
    )
    return signed_url


def backend_task(*args, **kwargs) -> dict:
    filenames: List[str] = ["blake.txt"]
    gcs_creds_path = os.environ["GCS_CREDS_PATH"]
    bucket_name = os.environ["GCS_BUCKET_NAME"]
    blob_name: str = "dir_0/dir_1/dir_2/blake.zip"
    content_type: str = "application/zip"
    exp_minutes: int = 60
    signed_url: str = _backend_task(
        filenames=filenames, gcs_creds_path=gcs_creds_path, bucket_name=bucket_name,
        blob_name=blob_name, content_type=content_type, exp_minutes=exp_minutes
    )
    return {"url": signed_url}
