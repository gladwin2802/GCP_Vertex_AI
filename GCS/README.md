# Google Cloud Storage (GCS) Tools

This folder contains tools for working with Google Cloud Storage. These scripts help you upload, download, and manage files and model directories in GCS buckets.

## What's Inside

### 1. **gcs.py**
This file handles bucket management and uploading model directories to Google Cloud Storage buckets.

**What it does:**
- Creates GCS buckets (with existence check)
- Uploads an entire model directory to a GCS bucket
- Preserves folder structure when uploading
- Deletes buckets and all their contents

### 2. **gcs_operations.py**
This file provides various operations for managing files and buckets in GCS.

**What it does:**
- Creates GCS buckets (with existence check)
- Lists all files in a bucket
- Downloads individual files from the bucket
- Downloads entire model directories from the bucket
- Uploads individual files to the bucket
- Gets the GCS URL (gs://) for files in the bucket
- Deletes buckets and all their contents

## Environment Variables (.env file)

Create a `.env` file in your project root with the following variables:

### Required Variables

```bash
# Path to your Google Cloud service account JSON key file
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json

# Your Google Cloud project ID
PROJECT_ID=your-project-id

# Name of your GCS bucket
BUCKET_NAME=your-bucket-name
```

### Optional Variables

```bash
# Google Cloud region (for bucket creation)
LOCATION=us-central1

# Local model directory path to upload
MODEL_DIR=path/to/your/model/directory

# Local directory path for downloads
DOWNLOAD_DIR=downloaded_model
```

### Example .env file

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/user/gcloud/service-account-key.json
PROJECT_ID=my-gcp-project
BUCKET=my-models-bucket
LOCATION=us-central1
MODEL_DIR=qwen2.5-3b-instruct
```

## How to Use

### Creating a Bucket

Before uploading files, you need to create a bucket:

```python
from gcs import create_bucket
from gcs_operations import create_bucket

# Create bucket (uses BUCKET_NAME and LOCATION from .env)
create_bucket()
```

Or run directly:
```bash
python -c "from gcs import create_bucket; create_bucket()"
```

### Uploading a Model Directory

1. Place your model files in a local directory
2. Set `MODEL_DIR` in your `.env` file (or use default)
3. Make sure the bucket exists (create it first if needed)
4. Run the script:
   ```bash
   python gcs.py
   ```

### Managing Files in GCS

Run the script to see available operations:
```bash
python gcs_operations.py
```

This will list all files in the bucket (if it exists).

### Using Functions Programmatically

You can import and use functions from both files in your own code:

```python
from gcs import create_bucket, upload_model_directory, delete_bucket
from gcs_operations import list_bucket_files, download_file, upload_file, download_model

# Create a bucket
create_bucket()

# Upload entire model directory
upload_model_directory("path/to/model")

# List all files in bucket
files = list_bucket_files()

# Download a specific file
download_file("model/config.json", "local_config.json")

# Download entire model
download_model("my_local_model_dir")

# Upload a single file
upload_file("local_file.txt", "remote_file.txt")

# Delete bucket (removes all files and bucket)
delete_bucket()
```

## Typical Workflow

1. **Create a bucket** using `create_bucket()` from either file
2. **Upload your model** to GCS using `upload_model_directory()` from `gcs.py`
3. **Verify upload** by listing files with `list_bucket_files()` from `gcs_operations.py`
4. **Use the GCS path** (gs://bucket-name/path) when registering models in Vertex AI
5. **Download models** when needed using `download_model()` from `gcs_operations.py`
6. **Clean up** by deleting the bucket with `delete_bucket()` when done

## Requirements

- Google Cloud account with Storage access
- Python packages: `google-cloud-storage`, `python-dotenv`
- Valid Google Cloud service account credentials (JSON key file)
- `.env` file configured with required environment variables (see above)
- Appropriate IAM permissions for bucket and object operations (see Notes section)

## Common Operations

### Create Bucket
```python
from gcs import create_bucket
from gcs_operations import create_bucket

# Create bucket (uses env vars)
create_bucket()

# Create bucket with custom name and location
create_bucket("my-custom-bucket", "us-east1")
```

### Upload Model Directory
```python
from gcs import upload_model_directory

# Upload model (uses MODEL_DIR from env)
upload_model_directory()

# Upload with custom path
upload_model_directory("path/to/my/model")
```

### List Files in Bucket
```python
from gcs_operations import list_bucket_files
files = list_bucket_files()
```

### Download Entire Model
```python
from gcs_operations import download_model

# Download to default directory (DOWNLOAD_DIR from env)
download_model()

# Download to custom directory
download_model("my_local_model_dir")
```

### Get Model GCS URL
```python
from gcs_operations import get_model_url
url = get_model_url("qwen2.5-3b-instruct/config.json")
# Returns: gs://bucket-name/qwen2.5-3b-instruct/config.json
```

### Delete Bucket
```python
from gcs import delete_bucket
from gcs_operations import delete_bucket

# Delete bucket and all contents (uses BUCKET_NAME from env)
delete_bucket()

# Delete specific bucket
delete_bucket("my-bucket-name")
```

## Notes

- Make sure your service account has the necessary permissions:
  - `storage.buckets.create` (for creating buckets)
  - `storage.buckets.delete` (for deleting buckets)
  - `storage.objects.create` (for uploads)
  - `storage.objects.get` (for downloads)
  - `storage.objects.list` (for listing)
  - `storage.objects.delete` (for deleting files)
  - `storage.buckets.get` (for bucket access)
- GCS paths use forward slashes (`/`) even on Windows
- Large model uploads may take time depending on your internet connection
- Bucket names must be globally unique across all GCS buckets
- Bucket deletion is permanent and cannot be undone - all files will be deleted
- The `create_bucket()` function checks if the bucket exists before creating it

