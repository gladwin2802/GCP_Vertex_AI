import os
from google.cloud import aiplatform
from dotenv import load_dotenv
load_dotenv()

SA_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not SA_FILE:
    raise FileNotFoundError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

PROJECT_ID = os.environ.get("PROJECT_ID")
if not PROJECT_ID:
    raise FileNotFoundError("PROJECT_ID environment variable not set")

LOCATION = os.environ.get("LOCATION", "us-central1")
DELETE_MODEL_ID = os.environ.get("DELETE_MODEL_ID", "meta-llama3_1-llama-3-1-8b-instruct-1770181322")

def model_register(display_name, artifact_uri, serving_container_image_uri, description):

    aiplatform.init(
        project=PROJECT_ID,
        location=LOCATION
    )

    model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=artifact_uri,
        serving_container_image_uri=serving_container_image_uri,
        # serving_container_ports=[7080],
        # serving_container_predict_route="/predict",
        # serving_container_health_route="/health",
        description=description
    )

    print("Model registered:", model.resource_name)
    print("Model ID:", model.name.split("/")[-1])

def model_delete(model_id):

    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    try:
        print(f"Deleting model with ID: {model_id}...")
        model = aiplatform.Model(model_id)
        
        model.delete()
        
        print(f"✓ Model {model_id} deleted successfully!")
        
    except Exception as e:
        print(f"✗ Error deleting model: {e}")
        raise

if __name__ == "__main__":
    # model_register(
    #     display_name="qwen-2.5-3b-instruct",
    #     artifact_uri="gs://qwen-models-incgcp/qwen2.5-3b-instruct",
    #     serving_container_image_uri="us-docker.pkg.dev/deeplearning-platform-release/gcr.io/huggingface-text-generation-inference-cu124.2-4.ubuntu2204.py311",
    #     description="Qwen 2.5 3B Instruct model"
    # )

    model_delete(model_id=DELETE_MODEL_ID)