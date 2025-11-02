import json
import random
import re

# ---------------------------
# 1. Load the extracted data
# ---------------------------
with open("data/processed/strategy_texts.json", "r") as f:
    data = json.load(f)

pairs = []

# ---------------------------
# 2. Instruction templates
# ---------------------------
templates = [
    "Summarize the key AI and digital transformation trends from this report.",
    "List the major companies and industries discussed in this document.",
    "Extract three strategic insights that could guide an enterprise strategy team.",
    "Explain the report’s implications for business leaders investing in AI.",
    "Generate a SWOT-style summary of the opportunities and risks described.",
    "Identify emerging technologies and their potential business impact.",
    "Condense this report into a 3-point executive summary."
]

# ---------------------------
# 3. Domain & Category Maps
# ---------------------------
domain_map = {
    "mckinsey": "consulting",
    "bain": "consulting",
    "bcg": "consulting",
    "pwc": "consulting",
    "deloitte": "consulting",
    "kpmg": "consulting",
    "anthropic": "ai",
    "openai": "ai",
    "meta": "ai",
    "goldman": "finance",
    "wef": "policy",
    "baker": "energy",
    "schlumberger": "energy",
    "aveva": "industrial"
}

category_map = {
    "trend": ["trend", "forecast", "insight"],
    "analysis": ["analysis", "report", "study"],
    "investment": ["investment", "valuation", "funding"],
    "strategy": ["strategy", "framework", "roadmap"],
    "policy": ["policy", "governance", "regulation"]
}

# ---------------------------
# 4. Normalize input structure
# ---------------------------
if isinstance(data, dict):
    # { "filename.pdf": "text..." }
    items = list(data.items())
    print(f"📂 Detected dictionary with {len(items)} documents.")
elif isinstance(data, list):
    items = []
    for entry in data:
        # Try to detect likely keys dynamically
        filename = (
            entry.get("filename")
            or entry.get("file")
            or entry.get("name")
            or entry.get("source")
            or "unknown"
        )
        text = (
            entry.get("text")
            or entry.get("content")
            or entry.get("data")
            or entry.get("body")
            or ""
        )
        items.append((filename, text))
    print(f"📂 Detected list with {len(items)} documents.")
else:
    raise TypeError(f"Unexpected data type: {type(data)}")

# Debug: show first detected entry
if items:
    sample_name, sample_text = items[0]
    print(f"🔍 Sample detected file: {sample_name}")
    print(f"🔍 Text length: {len(sample_text)} characters")

# ---------------------------
# 5. Helper functions
# ---------------------------
def infer_domain(filename):
    name = filename.lower()
    for key, val in domain_map.items():
        if key in name:
            return val
    return "general"

def infer_category(filename, text):
    name = filename.lower()
    text_snippet = text[:500].lower()
    for cat, words in category_map.items():
        if any(w in name or w in text_snippet for w in words):
            return cat
    return "general"

# ---------------------------
# 6. Generate enriched pairs
# ---------------------------
for filename, text in items:
    if not text.strip():
        continue  # skip empty entries
    snippet = text[:3000].strip()
    domain = infer_domain(filename)
    category = infer_category(filename, text)
    
    for _ in range(3):
        pairs.append({
            "source": filename,
            "domain": domain,
            "category": category,
            "instruction": random.choice(templates),
            "input": snippet,
            "output": "Generated strategy insight placeholder."
        })

# ---------------------------
# 7. Save JSONL output
# ---------------------------
if not pairs:
    print("⚠️ No valid text entries found. Check your strategy_texts.json structure.")
else:
    out_file = "data/processed/strategy_pairs_enriched.jsonl"
    with open(out_file, "w") as f:
        for p in pairs:
            json.dump(p, f)
            f.write("\n")

    print(f"✅ Created {len(pairs)} enriched strategy pairs in {out_file}")
    print(f"🧾 Example record:\n{json.dumps(pairs[0], indent=2)[:500]}")
