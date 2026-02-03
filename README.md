# Google Cloud AI Model Deployment and Usage

This project helps you download AI models, store them in the cloud, and use them to make predictions. Everything is organized into simple folders that work together.

## What Each Folder Does

### **HF** - Download Models
Downloads AI models from HuggingFace (a popular model library) to your computer.

**What it does:**
- Downloads a pre-trained AI model
- Saves it to a folder on your computer so you can use it later

### **GCS** - Store Models in Cloud Storage
Uploads your downloaded models to Google Cloud Storage so they're safely stored in the cloud.

**What it does:**
- Creates a storage bucket (like a folder in the cloud)
- Uploads your model files to the cloud
- Lets you download models back when needed

### **Vertex_AI** - Deploy and Use Models
Registers your model with Google Cloud's AI platform and makes it available for predictions.

**What it does:**
- Registers your model with Google Cloud
- Deploys it so it's ready to use
- Lets you send questions and get answers from the AI model

## How Everything Works Together

Here's the simple step-by-step process:

### Step 1: Download a Model
1. Go to the **HF** folder
2. Run the script to download a model from HuggingFace
3. The model files are saved to your computer

### Step 2: Upload to Cloud Storage
1. Go to the **GCS** folder
2. Create a storage bucket (if you don't have one)
3. Upload your downloaded model to the cloud
4. Your model is now safely stored online

### Step 3: Register the Model
1. Go to the **Vertex_AI** folder
2. Register your model with Google Cloud
3. Tell Google Cloud where your model files are stored

### Step 4: Deploy the Model
1. Deploy your registered model to an endpoint
2. This makes your model ready to answer questions
3. It may take a few minutes to set up

### Step 5: Use the Model
1. Send questions or prompts to your deployed model
2. Get AI-generated responses
3. Use it for chat conversations or text generation

## Getting Started

### What You Need First

1. **Google Cloud Account** - Sign up at cloud.google.com
2. **Service Account Key** - A special file that lets the scripts access your Google Cloud account
3. **Python** - Install Python on your computer
4. **Setup File** - Create a `.env` file with your account information

### Setup Steps

1. **Install Required Tools**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Your Setup File**
   Create a file named `.env` in this folder with:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
   PROJECT_ID=your-google-cloud-project-id
   BUCKET_NAME=your-storage-bucket-name
   LOCATION=us-central1
   ```

3. **Follow the Workflow**
   - Start with the HF folder to download a model
   - Then use GCS to upload it
   - Finally use Vertex_AI to deploy and use it

## Quick Reference

- **Download Model**: Run `python HF/hf.py`
- **Upload to Cloud**: Run `python GCS/gcs.py`
- **Deploy Model**: Run `python Vertex_AI/vertex_deployment.py`
- **Ask Questions**: Run `python Vertex_AI/vertex_inference_online.py`

## Need More Details?

Each folder has its own README file with more specific instructions:
- `HF/README.md` - How to download models
- `GCS/README.md` - How to manage cloud storage
- `Vertex_AI/README.md` - How to deploy and use models

## Important Notes

- Make sure your Google Cloud account has billing enabled
- Keep your service account key file safe and private
- Model deployment can take 5-15 minutes
- You'll be charged for using Google Cloud services based on usage

## Deployment Method Observation

**Important Finding:**

The workflow of downloading OSS models from HuggingFace, uploading to GCS, and then deploying to Vertex AI has been found to fail in practice.

**What Works:**
- Using Vertex AI Model Garden directly to deploy models works successfully
- The Model Garden approach (deploying models directly from Vertex AI's model library) is the recommended method

**What Doesn't Work:**
- Downloading models from HuggingFace → Uploading to GCS → Registering and deploying to Vertex AI

**Recommendation:**
For deploying models, use the Model Garden approach available in the `vertex_deployment.py` file, which deploys models directly from Vertex AI's Model Garden. This method is more reliable and easier to use than the manual upload workflow.

