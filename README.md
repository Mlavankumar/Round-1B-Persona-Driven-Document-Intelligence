# Round-1B-Persona-Driven-Document-Intelligence
AI-powered, persona-driven document analysis system for Adobe Hackathon 2025. Extracts relevant sections from multilingual PDFs based on user intent using ONNX SBERT, OCR, and zero-shot entailment. Fully offline, CPU-optimized, Dockerized, and outputs structured JSON for fast, smart insights.  


An AI-powered offline document analysis system for the Adobe India Hackathon 2025.
This project intelligently extracts contextually relevant sections from multilingual PDFs based on a given persona and job-to-be-done, supporting image-based PDFs (via OCR) and text-based PDFs. It uses semantic search, zero-shot classification, and entailment models, all optimized for CPU-only, offline, and Dockerized deployment.

 # Features
 Persona & Task-aware extraction (e.g., “Cybersecurity Analyst extracting compliance policies”)
 Semantic Matching with ONNX-optimized SBERT (under 1GB)
 Multilingual Support using FastText language detection
 Image-based PDF Support via Tesseract OCR
 Structured JSON Output with relevance scoring and explanation
 Fully Offline |  CPU-only |  Dockerized |  <60 seconds


 Tech Stack & Libraries (Used in Project)
 Embedding Model:
sentence-transformers/all-MiniLM-L6-v2 (converted to ONNX for faster, CPU-only inference)
 Intent Matching:
Zero-shot classification using facebook/bart-large-mnli (ONNX version)
 PDF Parsing:
PyMuPDF used for structured text extraction with layout and metadata support
 Language Detection:
FastText with pretrained lid.176.bin model for multilingual document support
 OCR (Optical Character Recognition):
Tesseract OCR integrated via pytesseract to process image-based PDFs
 ONNX Runtime & Tokenization:
onnxruntime for model execution
transformers and tokenizers for preprocessing and model I/O
 Noise Filtering:
Custom rule-based scoring filters, heuristic thresholds, and text cleaning to remove irrelevant content
 Containerization:
Docker used to ensure consistent, isolated, and reproducible environment for offline CPU-based execution



# File Structure
persona_pdf_intelligence/
│
├── app/
│   ├── main.py                       
│   ├── config.py                     
│   ├── pdf_parser.py                 
│   ├── semantic_matcher.py           
│   ├── snippet_refiner.py            
│   ├── output_generator.py           
│   ├── entailment_checker.py
│   ├── intent_encoder.py
│   ├── language_utils.py
│   ├── noise_filter.py
│   ├──zeroshot_classifier.py
│   ├──section_extractor.py
│
├── models/
│   ├── sbert.onnx                    
│   ├── tokenizer_config.json        
│   ├── entailment.onnx
│   └── lid.176.bin                  
│
├── sample_pdfs/
│   └── ...                          
│
├── Dockerfile
├── requirements.txt
├── README.md
└── output/ 



# How to Run via Docker
Step 1: Build the Docker Image
docker build -t persona_pdf_intelligence .

Step 2: Run the Container with Your Input PDFs
Mount your local sample_pdfs directory into the container and run:
docker run -it --rm -v "$(pwd)/sample_pdfs:/app/sample_pdfs" persona_pdf_intelligence \
  python main.py \
    --pdf_dir sample_pdfs \
    --persona "Cybersecurity Analyst in a Government Agency" \
    --job "Extract policy and legal compliance sections from documents"


    
# Output
A structured JSON file will be saved in the output/ directory with:

File-level metadata

Page-level matched sections

Refined text snippets with relevance scores and explanation

# Sample Output (JSON)
{
  "doc_id": "7993f85a-e2af-4094-a460-2ca0b5c8b971",
  "timestamp": "2025-07-28T22:03:14.703934",
  "persona": "Cybersecurity Analyst in a government agency",
  "task": "Extract policy and legal compliance sections from documents",
  "metadata": {
    "documents": [
      "Career_in_Cyber_Security_july2024.pdf",
      "dharmanand3-1.pdf",
      "Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C-1-10.pdf"
    ],
    "persona": "Cybersecurity Analyst in a government agency",
    "job": "Extract policy and legal compliance sections from documents",
    "timestamp": "2025-07-28T22:03:14.703934"
  },
  "num_relevant_sections": 0,
  "relevant_sections": [],
  "subsection_analysis": []
}




# Setup Without Docker (For Devs)

1. Install Requirements
 pip install -r requirements.txt

2. Run Locally
   python main.py \
  --pdf_dir sample_pdfs \
  --persona "PhD Researcher in Computational Biology" \
  --job "Summarize datasets and methods used in cancer detection"



# Contributors
Madhu Lavan Kumar – BTech CSE | Amrita Vishwa Vidyapeetham


# License
This project is for educational and non-commercial use only, developed as part of the Adobe India Hackathon 2025.
