"""
One-off script: uploads the local mediafiles/ folder to the Cloudflare R2
bucket, under the media/ prefix (matching MediaStorage.location in
storage_backends.py). Run once after loaddata, to get the actual image/video
files into R2 (loaddata only restores the database rows, not the files).

Usage (from the project root, with the venv activated):
    python upload_media_to_r2.py

Needs R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, R2_ENDPOINT_URL
set as environment variables in the current shell (same values as on Railway).
Safe to run more than once — it just re-uploads/overwrites.
"""
import os
import sys
import mimetypes

import boto3
from botocore.exceptions import ClientError

REQUIRED = ["R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET_NAME", "R2_ENDPOINT_URL"]
missing = [name for name in REQUIRED if not os.environ.get(name)]
if missing:
    print(f"Missing environment variables: {', '.join(missing)}")
    print("Set them in this PowerShell session first, e.g.:")
    print('  $env:R2_ACCESS_KEY_ID = "..."')
    sys.exit(1)

LOCAL_DIR = "mediafiles"
PREFIX = "media"

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["R2_ENDPOINT_URL"],
    aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
)
bucket = os.environ["R2_BUCKET_NAME"]

if not os.path.isdir(LOCAL_DIR):
    print(f"Folder '{LOCAL_DIR}' not found — run this from the project root.")
    sys.exit(1)

count = 0
failed = []

for root, _dirs, files in os.walk(LOCAL_DIR):
    for name in files:
        local_path = os.path.join(root, name)
        rel_path = os.path.relpath(local_path, LOCAL_DIR).replace(os.sep, "/")
        key = f"{PREFIX}/{rel_path}"

        content_type, _ = mimetypes.guess_type(local_path)
        extra_args = {"ContentType": content_type} if content_type else {}

        try:
            s3.upload_file(local_path, bucket, key, ExtraArgs=extra_args)
            count += 1
            print(f"[{count}] {key}")
        except ClientError as e:
            failed.append((key, str(e)))
            print(f"FAILED: {key} -> {e}")

print(f"\nDone. {count} files uploaded.")
if failed:
    print(f"{len(failed)} failed:")
    for key, err in failed:
        print(f"  {key}: {err}")
