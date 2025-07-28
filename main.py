# main.py

import argparse
import os
import time
import orjson
import uuid
from datetime import datetime

from app.pdf_parser import parse_pdf_documents
from app.intent_encoder import IntentEncoder
from app.section_extractor import SectionExtractor
from app.noise_filter import NoiseFilter
from app.semantic_matcher import SemanticMatcher
from app.snippet_refiner import SnippetRefiner
from app.output_generator import OutputGenerator
from tokenizer.tokenizer_utils import ONNXTokenizer


def process_documents(pdf_dir, persona, job, output_path):
    start_time = time.time()

    print("[🔍] Parsing PDF documents...")
    documents = parse_pdf_documents(pdf_dir)

    print("[🧠] Encoding intent...")
    tokenizer = ONNXTokenizer(model_name="bert-base-uncased")
    encoder = IntentEncoder(tokenizer)
    persona_task = f"{persona.strip()} | Task: {job.strip()}"
    intent_embedding = encoder.encode_intent(persona, job)

    print("[📚] Extracting sections...")
    extractor = SectionExtractor()
    section_metadata = []
    for doc in documents:
        filename = doc["filename"]
        for page_num, page_blocks in enumerate(doc["pages"]):
            sections = extractor.extract_sections(page_blocks)
            for section in sections:
                section_metadata.append({
                    "document": filename,
                    "page_number": page_num + 1,
                    "section_title": section["heading"],
                    "raw": section["raw"]
                })

    print("[🧹] Filtering noise...")
    noise_filter = NoiseFilter()
    clean_sections = noise_filter.clean_blocks(section_metadata)

    print("[📌] Ranking relevant sections...")
    matcher = SemanticMatcher()
    ranked_sections = matcher.rank_blocks(persona_task, clean_sections)

    print("[🔬] Refining relevant sections...")
    refiner = SnippetRefiner()
    refined_sections = refiner.refine_snippets(persona_task, ranked_sections)

    print("[📤] Generating output...")
    metadata = {
        "documents": [doc["filename"] for doc in documents],
        "persona": persona,
        "job": job,
        "timestamp": datetime.now().isoformat()
    }

    generator = OutputGenerator()
    output_json = generator.generate_json_output(
        persona=persona,
        task=job,
        file_metadata=metadata,
        top_sections=refined_sections,
    )

    output_json["doc_id"] = str(uuid.uuid4())
    output_json["timestamp"] = metadata["timestamp"]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(orjson.dumps(output_json, option=orjson.OPT_INDENT_2))

    end_time = time.time()
    print(f"[✅] Done in {end_time - start_time:.2f}s. Output saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence")
    parser.add_argument("--pdf_dir", type=str, required=True, help="Directory containing PDF files")
    parser.add_argument("--persona", type=str, required=True, help="Persona description")
    parser.add_argument("--job", type=str, required=True, help="Job to be done")
    parser.add_argument("--output", type=str, default="data/output/final_output.json", help="Output JSON path")

    args = parser.parse_args()
    process_documents(args.pdf_dir, args.persona, args.job, args.output)
