from pypdf import PdfReader
import os, json

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

def extract_text_from_pdfs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    all_docs = []
    for file in os.listdir(RAW_DIR):
        if file.endswith(".pdf"):
            path = os.path.join(RAW_DIR, file)
            print(f"Extracting text from {file}...")
            reader = PdfReader(path)
            text = " ".join([page.extract_text() or "" for page in reader.pages])
            filtered = filter_relevant_sections(text)
            all_docs.append({"file": file, "content": filtered})
    out_path = os.path.join(PROCESSED_DIR, "strategy_texts.json")
    with open(out_path, "w") as f:
        json.dump(all_docs, f, indent=2)
    print(f"✅ Extracted text saved to {out_path}")

def filter_relevant_sections(text):
    # Keep only strategy-related content
    keywords = ["strategy", "vision", "growth", "market", "innovation", "plan", "roadmap", "objective", "ai"]
    return " ".join([s for s in text.split(".") if any(k in s.lower() for k in keywords)])

if __name__ == "__main__":
    extract_text_from_pdfs()
