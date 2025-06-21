import boto3
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

# Werte auslesen
bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
region = os.getenv("AWS_S3_REGION_NAME")

print("👉 Bucket from .env:", bucket_name)
print("👉 Region:", region)

# Verbindung testen
try:
    s3 = boto3.resource('s3')
    buckets = list(s3.buckets.all())
    print("✅ S3 connection successful. Available buckets:")
    for b in buckets:
        print(" -", b.name)

    # Existiert Bucket?
    if any(b.name == bucket_name for b in buckets):
        print(f"✅ Bucket '{bucket_name}' exists.")
    else:
        print(f"❌ Bucket '{bucket_name}' NOT found in this AWS account.")
except Exception as e:
    print("❌ Error connecting to S3:", e)
