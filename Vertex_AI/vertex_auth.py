import os
from google.cloud import aiplatform
from dotenv import load_dotenv
load_dotenv()
PROJECT_ID = os.environ.get("PROJECT_ID")
if not PROJECT_ID:
    raise FileNotFoundError("PROJECT_ID environment variable not set")
SA_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
LOCATION = os.environ.get("LOCATION", "us-central1")
MODEL_ID_1 = os.environ.get("MODEL_ID_1")
MODEL_ID_2 = os.environ.get("MODEL_ID_2")
if not SA_FILE:
    raise FileNotFoundError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

def list_models(project: str, location: str = "us-central1"):
    """List all Vertex AI models in a project."""
    aiplatform.init(project=project, location=location)
    models = aiplatform.Model.list()
    for m in models:
        print(m.resource_name)
    return models


def list_endpoints(project: str, location: str = "us-central1"):
    """List all Vertex AI endpoints in a project."""
    aiplatform.init(project=project, location=location)
    endpoints = aiplatform.Endpoint.list()
    for e in endpoints:
        print(e.resource_name)
    return endpoints


def get_model(project: str, model_id: str, location: str = "us-central1"):
    """Get a specific model by ID."""
    aiplatform.init(project=project, location=location)
    model = aiplatform.Model(model_id)
    print(f"Model: {model.resource_name}")
    return model


def get_endpoint(project: str, endpoint_id: str, location: str = "us-central1"):
    """Get a specific endpoint by ID."""
    aiplatform.init(project=project, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    print(f"Endpoint: {endpoint.resource_name}")
    return endpoint


if __name__ == "__main__":

    
    print("Listing models...")
    list_models(PROJECT_ID, LOCATION)
    print("\nListing endpoints...")
    list_endpoints(PROJECT_ID, LOCATION)
    
    if MODEL_ID_1:
        print("\nGetting model...")
        get_model(PROJECT_ID, MODEL_ID_1, LOCATION)
    if MODEL_ID_2:
        print("\nGetting model...")
        get_model(PROJECT_ID, MODEL_ID_2, LOCATION)
