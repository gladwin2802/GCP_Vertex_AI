# 🚀 Deploying LLaMA 3.1 8B Instruct on Vertex AI (GCP)

Deploying **LLaMA 3.1 8B Instruct** from **Model Garden** and exposing it via a **Vertex AI Endpoint**.

## 📑 Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Enable Required APIs](#enable-required-apis)  
3. [Open Vertex AI Model Garden](#open-vertex-ai-model-garden)  
4. [Select LLaMA 3.1 8B Instruct](#select-llama-31-8b-instruct)  
5. [Deploy from Model Garden (UI)](#deploy-from-model-garden-ui)  
6. [Choose Machine & GPU](#choose-machine--gpu)  
7. [Create Endpoint](#create-endpoint)  
8. [Test the Endpoint (UI)](#test-the-endpoint-ui)  
9. [Invoke Endpoint via Python](#invoke-endpoint-via-python)  
10. [Invoke Endpoint via cURL](#invoke-endpoint-via-curl)  
11. [Cost & Quotas](#cost--quotas)

---

## Prerequisites

- Active **Google Cloud Project**
- Billing enabled on the project
- IAM permissions: `roles/aiplatform.admin` (Vertex AI Admin)  
  *(or custom role with sufficient Vertex AI + Compute permissions)*
- Recommended region: `us-central1` (good L4 GPU availability)

---

## Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com compute.googleapis.com
```

---

## Open Vertex AI Model Garden

Go to:  
https://console.cloud.google.com/vertex-ai/model-garden

---

## Select LLaMA 3.1 8B Instruct

In Model Garden:

- Search for: **LLaMA 3.1 8B Instruct**
- Published by: **Meta**
- Click on the model card

---

## Deploy from Model Garden (UI)

1. Click **Deploy**
2. You'll see:
   - Prebuilt container
   - Inference server fully managed by Google

---

## Choose Machine & GPU

Recommended configuration for LLaMA 3.1 8B Instruct (2024–2025):

| Setting          | Recommended Value     |
|------------------|------------------------|
| Machine type     | `g2-standard-12`      |
| Accelerator      | NVIDIA L4             |
| GPU count        | 1                     |
| Boot disk size   | 100 GB                |

*(Other good options: g2-standard-24 + 2×L4 if you want faster inference)*

---

## Create Endpoint

On the deploy screen:

- **Endpoint name**: `llama-31-8b-endpoint` (or your preferred name)
- **Min replicas**: 1
- **Max replicas**: 1 (or enable autoscaling later: e.g. 0–2)
- Click **Deploy**

⏳ Deployment usually takes **5–12 minutes**

---

## Test the Endpoint (UI)

Go to:  
Vertex AI → **Endpoints** → select your endpoint → **Test** tab

Example request body:

```json
{
  "instances": [
    {
      "prompt": "Explain transformers in simple terms"
    }
  ]
}
```

---

## Invoke Endpoint via Python

```python
from google.cloud import aiplatform

# Initialize client
aiplatform.init(project="YOUR_PROJECT_ID", location="us-central1")

# Replace with your actual endpoint resource name or ID
endpoint = aiplatform.Endpoint("ENDPOINT_ID")          # or full path: projects/.../endpoints/...

response = endpoint.predict(
    instances=[{
        "prompt": "Write a haiku about data engineering"
    }]
)

print(response.predictions)
```

---

## Cost & Quotas

Approximate on-demand pricing (us-central1, mid-2025):

| Resource       | Approx. Cost              |
|----------------|---------------------------|
| NVIDIA L4 GPU  | $0.60 – $0.85 / hour      |
| g2-standard-12 | ~$0.35 – $0.50 / hour     |
| Total (1 GPU)  | ~$1.00 – $1.35 / hour     |

- You are **charged only while the endpoint is deployed**
- **Always undeploy** when not in use (especially overnight / weekends)

---
## High-Level Architecture

```
Client 
   ↘
Vertex AI Endpoint 
   ↘
Managed LLaMA 3.1 8B container 
   ↘
NVIDIA L4 GPU 
   ↘
Generated Response
```
