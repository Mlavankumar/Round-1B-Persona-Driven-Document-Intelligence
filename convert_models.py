from transformers import AutoTokenizer, AutoModel
from optimum.exporters.onnx import main_export
import os

os.makedirs("models", exist_ok=True)

main_export(
    model_name_or_path="sentence-transformers/all-MiniLM-L6-v2",
    output=os.path.join("models", "sbert"),
    task="feature-extraction"
)
