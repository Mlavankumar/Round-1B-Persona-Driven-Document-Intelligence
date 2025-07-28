from optimum.exporters.onnx import main_export
import os

os.makedirs("models", exist_ok=True)

main_export(
    model_name_or_path="microsoft/deberta-v3-base",
    output=os.path.join("models", "entailment"),
    task="sequence-classification"
)
