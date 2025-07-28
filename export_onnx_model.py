from transformers import AutoTokenizer, AutoModel
from transformers.onnx import export
from pathlib import Path
import torch

model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Output path for ONNX model
onnx_path = Path("models/sbert.onnx")
onnx_path.parent.mkdir(parents=True, exist_ok=True)

# Export model
export(
    preprocessor=tokenizer,
    model=model,
    config=model.config,
    opset=12,
    output=onnx_path
)

print(f"✅ Exported ONNX model to {onnx_path}")
