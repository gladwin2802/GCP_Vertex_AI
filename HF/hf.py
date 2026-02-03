# Used to download models from huggingface

from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "Qwen/Qwen2.5-3B-Instruct"
local_dir = "./qwen2.5-3b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto"
)

tokenizer.save_pretrained(local_dir)
model.save_pretrained(local_dir)
