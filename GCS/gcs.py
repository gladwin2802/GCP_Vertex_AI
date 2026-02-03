import os
from google.cloud import storage
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

SA_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not SA_FILE:
    raise FileNotFoundError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

PROJECT_ID = os.environ.get("PROJECT_ID")
if not PROJECT_ID:
    raise FileNotFoundError("PROJECT_ID environment variable not set")

BUCKET_NAME = os.environ.get("BUCKET_NAME")
if not BUCKET_NAME:
    raise FileNotFoundError("BUCKET_NAME environment variable not set")

LOCATION = os.environ.get("LOCATION", "us-central1")
MODEL_DIR = os.environ.get("MODEL_DIR", "qwen2.5-3b-instruct")

client = storage.Client(project=PROJECT_ID)

def create_bucket(bucket_name: str = BUCKET_NAME, location: str = LOCATION):
    """Create a GCS bucket if it doesn't exist."""
    try:
        bucket = client.bucket(bucket_name)
        if bucket.exists():
            print(f"Bucket '{bucket_name}' already exists")
            return bucket
        
        bucket = client.create_bucket(bucket_name, location=location)
        print(f"✓ Created bucket: {bucket.name} in location: {location}")
        return bucket
    except Exception as e:
        print(f"✗ Error creating bucket: {e}")
        raise

def upload_model_directory(model_dir_path: str = MODEL_DIR, bucket_name: str = BUCKET_NAME):
    """Upload a model directory to GCS bucket."""
    bucket = client.bucket(bucket_name)
    
    if not bucket.exists():
        raise FileNotFoundError(f"Bucket '{bucket_name}' does not exist. Create it first using create_bucket()")
    
    model_dir = Path(model_dir_path)
    if model_dir.exists():
        print(f"Uploading model from {model_dir}...")
        
        folder_name = model_dir.name
        print(f"Creating folder '{folder_name}' in bucket...")
        
        for file_path in model_dir.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(model_dir.parent)
                blob_name = str(relative_path).replace("\\", "/")
                blob = bucket.blob(blob_name)
                blob.upload_from_filename(str(file_path))
                print(f"  ✓ Uploaded {blob_name}")
        print("Upload complete!")
    else:
        print(f"Model directory {model_dir} not found")


def delete_bucket(bucket_name: str = BUCKET_NAME):
    """Delete a GCS bucket and all its contents."""
    try:
        bucket = client.bucket(bucket_name)
        
        if not bucket.exists():
            print(f"Bucket '{bucket_name}' does not exist")
            return
        
        # Delete all blobs in the bucket first
        blobs = client.list_blobs(bucket_name)
        blob_count = 0
        for blob in blobs:
            blob.delete()
            blob_count += 1
            print(f"  ✓ Deleted blob: {blob.name}")
        
        if blob_count > 0:
            print(f"Deleted {blob_count} blob(s)")
        
        # Delete the bucket
        bucket.delete()
        print(f"✓ Bucket '{bucket_name}' deleted successfully!")
    except Exception as e:
        print(f"✗ Error deleting bucket: {e}")
        raise

if __name__ == "__main__":
    # Uncomment the line below to create the bucket if it doesn't exist
    # create_bucket(BUCKET_NAME, LOCATION)
    
    # Upload model directory
    upload_model_directory(MODEL_DIR, BUCKET_NAME)
    
    # Uncomment the line below to delete the bucket
    # delete_bucket(BUCKET_NAME)

