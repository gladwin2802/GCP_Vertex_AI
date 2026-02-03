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

client = storage.Client(project=PROJECT_ID)
bucket = client.bucket(BUCKET_NAME)


def create_bucket(bucket_name: str = BUCKET_NAME, location: str = None):
    """Create a GCS bucket if it doesn't exist."""
    if location is None:
        location = os.environ.get("LOCATION", "us-central1")
    
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


def list_bucket_files():
    """List all files in the bucket."""
    print(f"Files in bucket: {bucket.name}")
    blobs = list(bucket.list_blobs())
    for blob in blobs:
        print(f"  - {blob.name} ({blob.size} bytes)")
    return blobs


def download_file(blob_name: str, local_path: str = None):
    """Download a file from the bucket."""
    if local_path is None:
        local_path = blob_name.split("/")[-1]
    
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_path)
    print(f"✓ Downloaded {blob_name} to {local_path}")
    return local_path


def download_model(local_dir: str = None):
    """Download entire model from bucket."""
    if local_dir is None:
        local_dir = os.environ.get("DOWNLOAD_DIR", "downloaded_model")
    Path(local_dir).mkdir(exist_ok=True)
    print(f"Downloading model to {local_dir}...")
    
    blobs = bucket.list_blobs()
    for blob in blobs:
        local_file = Path(local_dir) / blob.name
        local_file.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(local_file))
        print(f"  ✓ Downloaded {blob.name}")
    
    print("✓ Model download complete!")
    return local_dir


def upload_file(local_path: str, blob_name: str = None):
    """Upload a file to the bucket."""
    if blob_name is None:
        blob_name = Path(local_path).name
    
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    print(f"✓ Uploaded {local_path} to {blob_name}")


def get_model_url(blob_name: str):
    """Get public URL for a file in bucket."""
    blob = bucket.blob(blob_name)
    url = f"gs://{bucket.name}/{blob_name}"
    print(f"Model URL: {url}")
    return url


if __name__ == "__main__":
    # Uncomment to create bucket if it doesn't exist
    # create_bucket(BUCKET_NAME)
    
    if bucket.exists():
        print(f"Bucket: {bucket.name}\n")
        # List files
        print(list_bucket_files())
    else:
        print(f"Bucket '{BUCKET_NAME}' does not exist. Use create_bucket() to create it.")
    
    # Uncomment to delete bucket
    # delete_bucket(BUCKET_NAME)