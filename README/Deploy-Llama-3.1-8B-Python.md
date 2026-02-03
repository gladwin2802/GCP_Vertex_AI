# 🚀 Deploying LLaMA 3.1 8B Instruct on Vertex AI (Python SDK)

Deploy **LLaMA 3.1 8B Instruct** using pure **Python** with the Vertex AI SDK.

## 📑 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Setup Authentication](#setup-authentication)
4. [Configuration](#configuration)
5. [Deploy Model from Model Garden](#deploy-model-from-model-garden)
6. [Test the Endpoint](#test-the-endpoint)
7. [Manage Deployment](#manage-deployment)
8. [Complete Deployment Script](#complete-deployment-script)

---

## Prerequisites

- Python 3.8+
- Service account JSON key with `roles/aiplatform.admin`
- Google Cloud project with billing enabled

---

## Installation

```bash
pip install google-cloud-aiplatform python-dotenv vertexai
```

---

## Setup Authentication

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Credentials will be loaded automatically from GOOGLE_APPLICATION_CREDENTIALS in .env
```

Create a `.env` file in your project root:

```bash
# .env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
PROJECT_ID=your-project-id
REGION=us-central1
ENDPOINT_NAME=llama-31-8b-endpoint
MODEL_NAME=llama-31-8b-instruct
```

---

## Configuration

```python
from google.cloud import aiplatform
from vertexai import model_garden

# Get configuration from environment variables
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION", "us-central1")
ENDPOINT_NAME = os.getenv("ENDPOINT_NAME", "llama-31-8b-endpoint")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3-1-8b-instruct")

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=REGION)
```

---

## Deploy Model from Model Garden

### Deploy Model (One-Step Process)

Using Model Garden, you can deploy LLaMA 3.1 8B Instruct in a single step. The `model.deploy()` method automatically creates the endpoint and deploys the model.

```python
def deploy_model(
    open_model_id: str = "meta/llama3_1@llama-3.1-8b-instruct",
    accept_eula: bool = True,
    machine_type: str = "g2-standard-12",
    accelerator_type: str = "NVIDIA_L4",
    accelerator_count: int = 1,
    serving_container_image_uri: str = "us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20241016_0916_RC00_maas",
    endpoint_display_name: str = ENDPOINT_NAME,
    model_display_name: str = MODEL_NAME,
    fast_tryout_enabled: bool = True,
):
    """Deploy model from Model Garden to Vertex AI endpoint."""
    model = model_garden.OpenModel(open_model_id)
    endpoint = model.deploy(
        accept_eula=accept_eula,
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        serving_container_image_uri=serving_container_image_uri,
        endpoint_display_name=endpoint_display_name,
        model_display_name=model_display_name,
        fast_tryout_enabled=fast_tryout_enabled,
    )
    return endpoint

# Deploy
endpoint = deploy_model()
print(f"✅ Deployment complete! Endpoint: {endpoint.resource_name}")
```

**Key Parameters:**
- `open_model_id`: Model identifier from Model Garden (e.g., `"meta/llama3_1@llama-3.1-8b-instruct"`)
- `accept_eula`: Accept the model's End User License Agreement (required)
- `machine_type`: Machine type for deployment (e.g., `"g2-standard-12"`)
- `accelerator_type`: GPU accelerator type (use `"NVIDIA_L4"`, not `"NVIDIA_TESLA_L4"`)
- `accelerator_count`: Number of accelerators
- `serving_container_image_uri`: Container image for serving the model
- `endpoint_display_name`: Name for the endpoint
- `model_display_name`: Name for the deployed model
- `fast_tryout_enabled`: Enable fast tryout feature

---

## Test the Endpoint

### Get Endpoint by Display Name

```python
def get_endpoint(endpoint_display_name: str = ENDPOINT_DISPLAY_NAME):
    """Get endpoint by display name."""
    try:
        endpoints = aiplatform.Endpoint.list(
            filter=f'display_name="{endpoint_display_name}"'
        )
        
        if not endpoints:
            print(f"✗ Endpoint '{endpoint_display_name}' not found")
            return None
        
        print(f"✓ Found endpoint: {endpoints[0].resource_name}")
        return endpoints[0]
        
    except Exception as e:
        print(f"✗ Error retrieving endpoint: {e}")
        raise
```

### Simple Text Prediction

```python
def predict_text(
    prompt: str,
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    max_tokens: int = 200,
    temperature: float = 0.2,
    top_p: float = 0.9
):
    """Make a text prediction request using chatCompletions format."""
    try:
        endpoint = get_endpoint(endpoint_display_name)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_display_name}' not found")
        
        instances = [
            {
                "@requestFormat": "chatCompletions",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p
            }
        ]
        
        print(f"\n📝 Sending inference request...")
        print(f"Prompt: {prompt}")
        
        response = endpoint.predict(instances=instances)
        print(f"✓ Inference completed")
        
        if hasattr(response, 'predictions') and response.predictions:
            predictions = response.predictions
            
            if isinstance(predictions, list) and len(predictions) > 0:
                result = predictions[0]
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]
                
                if isinstance(result, dict) and 'message' in result:
                    content = result['message'].get('content', '')
                    return content
            
            return str(predictions)
        
        return None
        
    except Exception as e:
        print(f"✗ Error during inference: {e}")
        raise

# Usage
prompt = "What is machine learning?"
response = predict_text(prompt)
if response:
    print(f"\n🤖 Model Response:")
    print(f"{'='*60}")
    print(response)
```

### Chat Completion

```python
def chat_completion(
    messages: list,
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    max_tokens: int = 512,
    temperature: float = 0.2,
    top_p: float = 0.9
):
    """Make a chat completion request with multiple messages."""
    try:
        endpoint = get_endpoint(endpoint_display_name)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_display_name}' not found")
        
        print(f"\n💬 Sending chat completion request...")
        print(f"Messages: {len(messages)}")
        
        instances = [
            {
                "@requestFormat": "chatCompletions",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p
            }
        ]
        
        response = endpoint.predict(instances=instances)
        print(f"✓ Chat inference completed")
        
        if hasattr(response, 'predictions') and response.predictions:
            predictions = response.predictions
            
            if isinstance(predictions, list) and len(predictions) > 0:
                result = predictions[0]
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]
                
                if isinstance(result, dict) and 'message' in result:
                    content = result['message'].get('content', '')
                    return content
            
            return str(predictions)
        
        return None
        
    except Exception as e:
        print(f"✗ Error during chat inference: {e}")
        return None

# Usage
messages = [
    {"role": "user", "content": "What is machine learning? Please, answer in pirate-speak."}
]

response = chat_completion(messages, max_tokens=100)
if response:
    print(response)
```

---

## Manage Deployment

### List Deployments

```python
def list_deployments(endpoint_display_name):
    """List all models deployed on an endpoint."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if not endpoints:
        print(f"✗ Endpoint '{endpoint_display_name}' not found")
        return
    
    endpoint = endpoints[0]
    deployments = endpoint.list_models()
    
    print(f"Deployments on endpoint '{endpoint_display_name}':")
    for deployed_model in deployments:
        print(f"  • {deployed_model.display_name} (ID: {deployed_model.id})")
    return deployments
```

### Undeploy Model

```python
def undeploy_model(endpoint_display_name, deployed_model_id):
    """Undeploy a specific model from endpoint."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if not endpoints:
        print(f"✗ Endpoint '{endpoint_display_name}' not found")
        return
    
    endpoint = endpoints[0]
    endpoint.undeploy(deployed_model_id=deployed_model_id)
    print(f"✓ Model undeployed successfully!")
```

### Delete Endpoint

```python
def delete_endpoint(endpoint_display_name):
    """Delete endpoint (must undeploy models first)."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if not endpoints:
        print(f"✗ Endpoint '{endpoint_display_name}' not found")
        return
    
    endpoint = endpoints[0]
    endpoint.delete()
    print(f"✓ Endpoint deleted successfully!")
```

---

## Complete Deployment Script

```python
import os
from dotenv import load_dotenv
from google.cloud import aiplatform
from vertexai import model_garden

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("REGION", "us-central1")
ENDPOINT_DISPLAY_NAME = os.getenv("ENDPOINT_NAME", "llama-3-1-8b-instruct-mg-one-click-deploy")
MODEL_DISPLAY_NAME = os.getenv("MODEL_NAME", "llama-3-1-8b-instruct")

aiplatform.init(project=PROJECT_ID, location=LOCATION)

def deploy_model(
    open_model_id: str = "meta/llama3_1@llama-3.1-8b-instruct",
    accept_eula: bool = True,
    machine_type: str = "g2-standard-12",
    accelerator_type: str = "NVIDIA_L4",
    accelerator_count: int = 1,
    serving_container_image_uri: str = "us-docker.pkg.dev/vertex-ai/vertex-vision-model-garden-dockers/pytorch-vllm-serve:20241016_0916_RC00_maas",
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    model_display_name: str = MODEL_DISPLAY_NAME,
    fast_tryout_enabled: bool = True,
):
    """Deploy model from Model Garden to Vertex AI endpoint."""
    model = model_garden.OpenModel(open_model_id)
    endpoint = model.deploy(
        accept_eula=accept_eula,
        machine_type=machine_type,
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        serving_container_image_uri=serving_container_image_uri,
        endpoint_display_name=endpoint_display_name,
        model_display_name=model_display_name,
        fast_tryout_enabled=fast_tryout_enabled,
    )
    return endpoint

def get_endpoint(endpoint_display_name: str = ENDPOINT_DISPLAY_NAME):
    """Get endpoint by display name."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if not endpoints:
        print(f"✗ Endpoint '{endpoint_display_name}' not found")
        return None
    print(f"✓ Found endpoint: {endpoints[0].resource_name}")
    return endpoints[0]

def predict_text(
    prompt: str,
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    max_tokens: int = 200,
    temperature: float = 0.2,
    top_p: float = 0.9
):
    """Make a text prediction request using chatCompletions format."""
    endpoint = get_endpoint(endpoint_display_name)
    if not endpoint:
        raise ValueError(f"Endpoint '{endpoint_display_name}' not found")
    
    instances = [
        {
            "@requestFormat": "chatCompletions",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    ]
    
    print(f"\n📝 Sending inference request...")
    print(f"Prompt: {prompt}")
    
    response = endpoint.predict(instances=instances)
    print(f"✓ Inference completed")
    
    if hasattr(response, 'predictions') and response.predictions:
        predictions = response.predictions
        if isinstance(predictions, list) and len(predictions) > 0:
            result = predictions[0]
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            if isinstance(result, dict) and 'message' in result:
                content = result['message'].get('content', '')
                return content
        return str(predictions)
    return None

def cleanup(endpoint_display_name):
    """Clean up resources."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if endpoints:
        endpoint = endpoints[0]
        for deployed_model in endpoint.list_models():
            endpoint.undeploy(deployed_model_id=deployed_model.id)
        endpoint.delete()
        print(f"✅ Deleted endpoint: {endpoint_display_name}")

if __name__ == "__main__":
    endpoint = deploy_model()
    print(f"✅ Deployment complete! Endpoint: {endpoint.resource_name}")
    
    result = predict_text("Explain transformers in one sentence")
    if result:
        print(f"\n🤖 Model Response:")
        print(f"{'='*60}")
        print(result)
    
    # cleanup(ENDPOINT_DISPLAY_NAME)
```

---

## Autoscaling Deployment

Note: Model Garden's `deploy()` method handles endpoint creation automatically. For autoscaling, you would need to update the deployment after creation or use the standard deployment approach with manual endpoint management.

---

## Monitoring

```python
def get_endpoint_info(endpoint):
    """Get endpoint details and deployed models."""
    print(f"Endpoint: {endpoint.display_name}")
    print(f"Resource name: {endpoint.resource_name}")
    print(f"Create time: {endpoint.create_time}")
    
    for deployed_model in endpoint.gca_resource.deployed_models:
        print(f"\nDeployed Model:")
        print(f"  ID: {deployed_model.id}")
        print(f"  Display name: {deployed_model.display_name}")
        print(f"  Machine type: {deployed_model.dedicated_resources.machine_spec.machine_type}")
        print(f"  Min replicas: {deployed_model.dedicated_resources.min_replica_count}")
        print(f"  Max replicas: {deployed_model.dedicated_resources.max_replica_count}")
```

---

## Error Handling

```python
from google.api_core import exceptions

def safe_deploy():
    """Deploy with error handling."""
    try:
        endpoint = deploy_model()
        return endpoint
    except exceptions.GoogleAPIError as e:
        print(f"❌ Deployment failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
```

---

## Cost Optimization

```python
def undeploy_model(endpoint_display_name, deployed_model_id):
    """Undeploy a specific model from endpoint."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if endpoints:
        endpoint = endpoints[0]
        endpoint.undeploy(deployed_model_id=deployed_model_id)
        print(f"✅ Model {deployed_model_id} undeployed successfully")

def delete_endpoint(endpoint_display_name):
    """Delete endpoint (must undeploy models first)."""
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{endpoint_display_name}"'
    )
    if endpoints:
        endpoint = endpoints[0]
        endpoint.delete()
        print(f"✅ Endpoint {endpoint_display_name} deleted successfully")
```
