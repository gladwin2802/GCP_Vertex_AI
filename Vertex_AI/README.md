# Vertex AI Tools

This folder contains tools for working with Google Cloud's Vertex AI platform. These scripts help you manage AI models and use them to make predictions.

## What's Inside

### 1. **vertex_auth.py**
This file handles connecting to your Google Cloud account and provides basic information about your models and endpoints.

**What it does:**
- Lists all your AI models
- Lists all your endpoints (places where models are deployed)
- Gets details about specific models
- Gets details about specific endpoints

### 2. **vertex_model_register.py**
This file helps you add new AI models to Vertex AI or remove existing ones.

**What it does:**
- Registers a new model to your Vertex AI project
- Deletes models you no longer need

### 3. **vertex_deployment.py**
This file manages how your models are deployed and made available for use.

**What it does:**
- Deploys a model to an endpoint (makes it ready to use)
- Lists all models currently deployed on an endpoint
- Removes a model from an endpoint
- Deletes entire endpoints

### 4. **vertex_inference_online.py**
This file is used to actually use your deployed models to make predictions or have conversations.

**What it does:**
- Sends questions or prompts to your deployed model
- Gets responses from the AI model
- Supports both simple questions and chat-style conversations

## Environment Variables (.env file)

Create a `.env` file in your project root with the following variables:

### Required Variables

```bash
# Path to your Google Cloud service account JSON key file
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json

# Your Google Cloud project ID
PROJECT_ID=your-project-id
```

### Optional Variables (with defaults)

```bash
# Google Cloud region (defaults to "us-central1" if not set)
LOCATION=us-central1

# Endpoint display name (used by vertex_deployment.py and vertex_inference_online.py)
# Default: "llama-3-1-8b-instruct-mg-one-click-deploy"
ENDPOINT_DISPLAY_NAME=your-endpoint-name

# Model display name (used by vertex_deployment.py)
# Default: "llama-3-1-8b-instruct"
MODEL_DISPLAY_NAME=your-model-name

# Model ID for undeploying (used by vertex_deployment.py)
MODEL_ID=your-model-id

# Model ID for deletion (used by vertex_model_register.py)
DELETE_MODEL_ID=your-model-id-to-delete

# Model IDs for testing (used by vertex_auth.py)
MODEL_ID_1=your-first-model-id
MODEL_ID_2=your-second-model-id
```

### Example .env file

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/user/gcloud/service-account-key.json
PROJECT_ID=my-gcp-project
LOCATION=us-central1
ENDPOINT_DISPLAY_NAME=my-llama-endpoint
MODEL_DISPLAY_NAME=my-llama-model
```

## How to Use

1. Create a `.env` file with the required environment variables (see above)
2. Make sure you have your Google Cloud credentials set up
3. Each file can be run directly to see examples of how it works
4. You can also import functions from these files into your own code

## Typical Workflow

1. **Register a model** using `vertex_model_register.py`
2. **Deploy the model** using `vertex_deployment.py`
3. **Use the model** to make predictions with `vertex_inference_online.py`
4. **Manage your resources** using `vertex_auth.py` to see what you have

## Requirements

- Google Cloud account with Vertex AI access
- Python packages: `google-cloud-aiplatform`, `python-dotenv`, `vertexai`
- Valid Google Cloud service account credentials (JSON key file)
- `.env` file configured with required environment variables (see above)

