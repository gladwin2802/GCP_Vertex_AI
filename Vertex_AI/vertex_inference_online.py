import os
from google.cloud import aiplatform
from dotenv import load_dotenv
import json

load_dotenv()

SA_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not SA_FILE:
    raise FileNotFoundError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")

PROJECT_ID = os.environ.get("PROJECT_ID")
if not PROJECT_ID:
    raise FileNotFoundError("PROJECT_ID environment variable not set")

LOCATION = os.environ.get("LOCATION", "us-central1")
ENDPOINT_DISPLAY_NAME = os.environ.get("ENDPOINT_DISPLAY_NAME", "llama-3-1-8b-instruct-mg-one-click-deploy")

aiplatform.init(project=PROJECT_ID, location=LOCATION)

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

def predict_text(
    prompt: str,
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    max_tokens: int = 200,
    temperature: float = 0.2,
    top_p: float = 0.9
):
    try:
        endpoint = get_endpoint(endpoint_display_name)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_display_name}' not found")
        
        # Prepare input using chatCompletions format
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
        
        print(f"\nSending inference request...")
        print(f"Prompt: {prompt}")
        
        # Make prediction
        response = endpoint.predict(instances=instances)
        
        print(f"✓ Inference completed")
        
        # Extract predictions
        if hasattr(response, 'predictions') and response.predictions:
            predictions = response.predictions
            print(f"\n🤖 Model Response:")
            print(f"{'='*60}")
            
            # Handle nested list structure: predictions[0][0]
            if isinstance(predictions, list) and len(predictions) > 0:
                result = predictions[0]
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]
                
                # Extract message content
                if isinstance(result, dict) and 'message' in result:
                    content = result['message'].get('content', '')
                    return content
            
            return str(predictions)
        
        return None
        
    except Exception as e:
        print(f"✗ Error during inference: {e}")
        raise

def chat_completion(
    messages: list,
    endpoint_display_name: str = ENDPOINT_DISPLAY_NAME,
    max_tokens: int = 512,
    temperature: float = 0.2,
    top_p: float = 0.9
):
    try:
        endpoint = get_endpoint(endpoint_display_name)
        if not endpoint:
            raise ValueError(f"Endpoint '{endpoint_display_name}' not found")
        
        print(f"\n💬 Sending chat completion request...")
        print(f"Messages: {len(messages)}")
        
        # Prepare input using chatCompletions format
        instances = [
            {
                "@requestFormat": "chatCompletions",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p
            }
        ]
        
        # Make prediction
        response = endpoint.predict(instances=instances)
        
        print(f"✓ Chat inference completed")
        
        # Extract predictions
        if hasattr(response, 'predictions') and response.predictions:
            predictions = response.predictions
            
            # Handle nested list structure: predictions[0][0]
            if isinstance(predictions, list) and len(predictions) > 0:
                result = predictions[0]
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]
                
                # Extract message content
                if isinstance(result, dict) and 'message' in result:
                    content = result['message'].get('content', '')
                    return content
            
            return str(predictions)
        
        return None
        
    except Exception as e:
        print(f"✗ Error during chat inference: {e}")
        return None

if __name__ == "__main__":
    # Example 1: Simple text prediction
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Text Prediction")
    print("="*60)
    
    prompt = "What is machine learning?"
    response = predict_text(prompt)
    if response:
        print(response)
    
    # Example 2: Chat completion with chatCompletions format
    print("\n" + "="*60)
    print("EXAMPLE 2: Chat Completion")
    print("="*60)
    
    messages = [
        {"role": "user", "content": "What is machine learning? Please, answer in pirate-speak."}
    ]
    
    response = chat_completion(messages, max_tokens=100)
    if response:
        print(response)
