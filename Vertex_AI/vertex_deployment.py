import os
from google.cloud import aiplatform
from dotenv import load_dotenv
from vertexai import model_garden
load_dotenv()

SA_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not SA_FILE:
    raise FileNotFoundError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

PROJECT_ID = os.environ.get("PROJECT_ID")
if not PROJECT_ID:
    raise FileNotFoundError("PROJECT_ID environment variable not set")

LOCATION = os.environ.get("LOCATION", "us-central1")
ENDPOINT_DISPLAY_NAME = os.environ.get("ENDPOINT_DISPLAY_NAME", "llama-3-1-8b-instruct-mg-one-click-deploy")
MODEL_DISPLAY_NAME = os.environ.get("MODEL_DISPLAY_NAME", "llama-3-1-8b-instruct")
MODEL_ID = os.environ.get("MODEL_ID")

aiplatform.init(project=PROJECT_ID, location=LOCATION)

def list_deployments(endpoint_display_name: str = ENDPOINT_DISPLAY_NAME):
    try:
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
        
    except Exception as e:
        print(f"✗ Error listing deployments: {e}")
        raise

def undeploy_model(
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    deployed_model_id: str = None
):
    try:
        endpoints = aiplatform.Endpoint.list(
            filter=f'display_name="{endpoint_display_name}"'
        )
        
        if not endpoints:
            print(f"✗ Endpoint '{endpoint_display_name}' not found")
            return
        
        endpoint = endpoints[0]
        
        if deployed_model_id:
            print(f"Undeploying model {deployed_model_id}...")
            endpoint.undeploy(deployed_model_id=deployed_model_id)
            print(f"✓ Model undeployed successfully!")
        else:
            print("Please provide a deployed_model_id")
            
    except Exception as e:
        print(f"✗ Error undeploying model: {e}")
        raise

def delete_endpoint(endpoint_display_name: str = ENDPOINT_DISPLAY_NAME):
    try:
        endpoints = aiplatform.Endpoint.list(
            filter=f'display_name="{endpoint_display_name}"'
        )
        
        if not endpoints:
            print(f"✗ Endpoint '{endpoint_display_name}' not found")
            return
        
        endpoint = endpoints[0]
        print(f"Deleting endpoint '{endpoint_display_name}'...")
        endpoint.delete()
        print(f"✓ Endpoint deleted successfully!")
        
    except Exception as e:
        print(f"✗ Error deleting endpoint: {e}")
        raise

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

if __name__ == "__main__":

    endpoint = deploy_model()
    # undeploy_model(deployed_model_id=MODEL_ID)
    # delete_endpoint()