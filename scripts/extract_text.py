from pypdf import PdfReader
import os, json

# ----------------------------
# Folder paths
# ----------------------------
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ----------------------------
# Helper: filter strategic sections
# ----------------------------
def filter_relevant_sections(text):
    keywords = [
        "strategy", "vision", "growth", "market",
        "innovation", "plan", "roadmap", "objective", "ai"
    ]
    return " ".join(
        [s for s in text.split(".") if any(k in s.lower() for k in keywords)]
    )

# ----------------------------
# Main extraction function
# ----------------------------
def extract_text_from_pdfs():
    all_docs = []
    for file in os.listdir(RAW_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(RAW_DIR, file)
        print(f"Extracting text from {file}...")

        try:
            # Quick validity check
            with open(path, "rb") as f:
                if not f.read(4).startswith(b"%PDF"):
                    raise ValueError("Invalid PDF header")

            # Read and extract text
            reader = PdfReader(path)
            text = " ".join([page.extract_text() or "" for page in reader.pages])
            filtered = filter_relevant_sections(text)
            all_docs.append({"file": file, "content": filtered})

        except Exception as e:
            print(f"⚠️  Skipped {file}: {e}")
            continue

    # Save extracted results
    out_path = os.path.join(PROCESSED_DIR, "strategy_texts.json")
    with open(out_path, "w") as f:
        json.dump(all_docs, f, indent=2)

    print(f"✅ Extraction complete. Saved to {out_path}")

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    extract_text_from_pdfs()
