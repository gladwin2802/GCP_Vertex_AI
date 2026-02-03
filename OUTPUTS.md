# Vertex AI Model Deployment Workflow

## Step 1: Upload Model Files to Google Cloud Storage

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\gcs.py"
```

**Output:**
```
Uploading model from qwen2.5-3b-instruct...
  ✓ Uploaded qwen2.5-3b-instruct\chat_template.jinja
  ✓ Uploaded qwen2.5-3b-instruct\config.json
  ✓ Uploaded qwen2.5-3b-instruct\generation_config.json
  ✓ Uploaded qwen2.5-3b-instruct\model.safetensors
  ✓ Uploaded qwen2.5-3b-instruct\tokenizer.json
  ✓ Uploaded qwen2.5-3b-instruct\tokenizer_config.json
Upload complete!
```

**Status:** ✓ Success - All model files uploaded to GCS

---

## Step 2: Register Model in Vertex AI

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\vertex_register_model.py"
```

**Output:**
```
Creating Model
Create Model backing LRO: projects/671902667767/locations/us-central1/models/2783241062389383168/operations/1035444167557251072
Model created. Resource name: projects/671902667767/locations/us-central1/models/2783241062389383168@1
To use this Model in another session:
model = aiplatform.Model('projects/671902667767/locations/us-central1/models/2783241062389383168@1')
Model registered: projects/671902667767/locations/us-central1/models/2783241062389383168
Model ID: 2783241062389383168
```

**Status:** ✓ Success - Model registered with ID: `2783241062389383168`

---

## Step 3: Deploy Model to Endpoint (First Attempt - Failed)

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\vertex_model_deployment.py"
```

**Output:**
```
============================================================
DEPLOYING REGISTERED MODEL TO ENDPOINT
============================================================
Creating endpoint 'qwen-endpoint'...
Creating Endpoint
Create Endpoint backing LRO: projects/671902667767/locations/us-central1/endpoints/6123311096968249344/operations/8845741452580356096
Endpoint created. Resource name: projects/671902667767/locations/us-central1/endpoints/6123311096968249344
To use this Endpoint in another session:
endpoint = aiplatform.Endpoint('projects/671902667767/locations/us-central1/endpoints/6123311096968249344')
✓ Endpoint created: projects/671902667767/locations/us-central1/endpoints/6123311096968249344
✓ Found model: projects/671902667767/locations/us-central1/models/2783241062389383168
Deploying model (ID: 2783241062389383168) to endpoint...
✗ Error deploying model: Given accelerator_type `NVIDIA_TESLA_L4` invalid. Choose one of ['ACCELERATOR_TYPE_UNSPECIFIED', 'NVIDIA_TESLA_K80', 'NVIDIA_TESLA_P100', 'NVIDIA_TESLA_V100', 'NVIDIA_TESLA_P4', 'NVIDIA_TESLA_T4', 'NVIDIA_TESLA_A100', 'NVIDIA_A100_80GB', 'NVIDIA_L4', 'NVIDIA_H100_80GB', 'NVIDIA_H100_MEGA_80GB', 'NVIDIA_H200_141GB', 'NVIDIA_B200', 'NVIDIA_GB200', 'NVIDIA_RTX_PRO_6000', 'TPU_V2', 'TPU_V3', 'TPU_V4_POD', 'TPU_V5_LITEPOD']
```

**Status:** ✗ Failed - Invalid accelerator type `NVIDIA_TESLA_L4`. Should use `NVIDIA_L4` instead.

**Error Details:**
- The accelerator type `NVIDIA_TESLA_L4` is not valid
- Valid options include: `NVIDIA_L4`, `NVIDIA_TESLA_T4`, `NVIDIA_TESLA_A100`, etc.
- Endpoint was created successfully but model deployment failed

---

## Step 4: Re-register Model and Clean Up Endpoint

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\vertex_register_model.py"
```

**Output:**
```
Creating Model
Create Model backing LRO: projects/671902667767/locations/us-central1/models/8340656614285508608/operations/2827947187994886144
Model created. Resource name: projects/671902667767/locations/us-central1/models/8340656614285508608@1
To use this Model in another session:
model = aiplatform.Model('projects/671902667767/locations/us-central1/models/8340656614285508608@1')
Model registered: projects/671902667767/locations/us-central1/models/8340656614285508608
Deleting endpoint 'qwen-endpoint'...
Deleting Endpoint : projects/671902667767/locations/us-central1/endpoints/6123311096968249344
Endpoint deleted. . Resource name: projects/671902667767/locations/us-central1/endpoints/6123311096968249344
Deleting Endpoint resource: projects/671902667767/locations/us-central1/endpoints/6123311096968249344
Delete Endpoint backing LRO: projects/671902667767/locations/us-central1/operations/5136041997022265344
Endpoint resource projects/671902667767/locations/us-central1/endpoints/6123311096968249344 deleted.
✓ Endpoint deleted successfully!

MODEL_ID = 8340656614285508608
```

**Status:** ✓ Success - New model registered with ID: `8340656614285508608`, old endpoint cleaned up

---

## Step 5: Run Inference on Deployed Model

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\vertex_inference_online.py"
```

**Output:**

### Example 1: Single Text Prediction
```
============================================================
EXAMPLE 1: Single Text Prediction
============================================================
✓ Found endpoint: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4

📝 Sending inference request...
Prompt: What is machine learning?...
✓ Inference completed

🤖 Model Response:
============================================================
Machine learning is a subset of artificial intelligence (AI) that involves the use of algorithms and statistical models to enable machines to learn from data, make decisions, and improve their performance over time without being explicitly programmed.

Machine learning is based on the idea that machines can learn from experience and improve their performance on a task by analyzing data and identifying patterns, relationships, and trends. This is in contrast to traditional programming, where a machine is given a set of rules and instructions to follow.

There are several key characteristics of machine learning:

1. **Learning from data**: Machine learning algorithms use data to learn and improve their performance.
2. **Improvement over time**: As machines learn from data, they can improve their performance over time.
3. **Autonomy**: Machine learning algorithms can operate independently, making decisions and taking actions without human intervention.
4. **Flexibility**: Machine learning algorithms can be applied to a wide range of tasks, from image and speech recognition to natural language processing and predictive modeling.

Machine learning involves several key concepts, including:

1. **Supervised learning**: The machine is trained on labeled data, where the correct output is already known.
2. **Unsupervised learning**: The machine is trained on unlabeled data, and it must find patterns and relationships on its own.
3. **Reinforcement learning**: The machine learns by interacting with an environment and receiving feedback in the form of rewards or penalties.
4. **Deep learning**: A type of machine learning that uses neural networks with multiple layers to learn complex patterns and relationships.

Machine learning has many applications, including:

1. **Image and speech recognition**: Machines can recognize and classify images and speech patterns.
2. **Natural language processing**: Machines can understand and generate human language.
3. **Predictive modeling**: Machines can predict outcomes based on historical data and patterns.
4. **Recommendation systems**: Machines can recommend products or services based on user behavior and preferences.

Overall, machine learning is a powerful tool that enables machines to learn from data and improve their performance over time, leading to many exciting applications and innovations.
```

### Example 2: Chat Completion
```
============================================================
EXAMPLE 2: Chat Completion
============================================================
✓ Found endpoint: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4

💬 Sending chat completion request...
Messages: 1
✓ Chat inference completed
Arrrr, ye landlubber! Ye be wantin' to know about machine learnin', eh? Alright then, listen close and I'll tell ye the tale.

Machine learnin' be a type o' computer magic that lets machines learn from experience, just like a swashbucklin' pirate learns from his adventures on the high seas. It be a way o' trainin' computers to make decisions based on data, like a trusty map that helps ye navigate through tre
```

**Status:** ✓ Success - Both inference examples completed successfully

**Endpoint Used:** `mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4`

---

## Step 6: Undeploy Model from Endpoint

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\vertex_model_deployment.py"
```

**Output:**
```
Undeploying model 2395035942214696960...
Undeploying Endpoint model: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4
Undeploy Endpoint model backing LRO: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4/operations/3949818484233338880
Endpoint model undeployed. Resource name: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4
✓ Model undeployed successfully!
```

**Status:** ✓ Success - Model `2395035942214696960` undeployed from endpoint

---

## Step 7: Delete Endpoint

```bash
python -u "c:\Users\thanya.r\Downloads\Gcloud\vertex_model_deployment.py"
```

**Output:**
```
Deleting endpoint 'llama-3-1-8b-instruct-mg-one-click-deploy'...
Deleting Endpoint : projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4  
Endpoint deleted. . Resource name: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4
Deleting Endpoint resource: projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4
Delete Endpoint backing LRO: projects/671902667767/locations/us-central1/operations/1457076090483769344
Endpoint resource projects/671902667767/locations/us-central1/endpoints/mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4 deleted.
✓ Endpoint deleted successfully!
```

**Status:** ✓ Success - Endpoint `mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4` deleted

---

## Summary

### Successful Operations:
1. ✓ Model files uploaded to GCS
2. ✓ Model registered (ID: `2783241062389383168` and `8340656614285508608`)
3. ✓ Endpoint created
4. ✓ Inference requests completed successfully
5. ✓ Model undeployed
6. ✓ Endpoint deleted

### Issues Encountered:
- ✗ Invalid accelerator type `NVIDIA_TESLA_L4` - should use `NVIDIA_L4` instead

### Key Resource IDs:
- **Model IDs:** `2783241062389383168`, `8340656614285508608`
- **Endpoint ID:** `mg-endpoint-198d8af8-d573-4ad5-9f9f-b0fbc71b8fd4`
- **Project:** `671902667767`
- **Location:** `us-central1`

