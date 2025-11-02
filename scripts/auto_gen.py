import json
import random
import re

# Load extracted text
with open("strategy_texts.json", "r") as f:
    data = json.load(f)

pairs = []

# Common strategy instruction templates
templates = [
    "Summarize the key AI and digital transformation trends from this report.",
    "List the major companies and industries discussed in this document.",
    "Extract three strategic insights that could guide an enterprise strategy team.",
    "Explain the report’s implications for business leaders investing in AI.",
    "Generate a SWOT-style summary of the opportunities and risks described.",
    "Identify emerging technologies and their potential business impact.",
    "Condense this report into a 3-point executive summary."
]

# Domain keywords mapping
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

# Category keywords (used to label type of document)
category_map = {
    "trend": ["trend", "forecast", "insight"],
    "analysis": ["analysis", "report", "study"],
    "investment": ["investment", "valuation", "funding"],
    "strategy": ["strategy", "framework", "roadmap"],
    "policy": ["policy", "governance", "regulation"]
}

# Normalize list/dict input
if isinstance(data, dict):
    items = data.items()
elif isinstance(data, list):
    items = [(entry.get("filename", "unknown"), entry.get("text", "")) for entry in data]
else:
    raise TypeError(f"Unexpected data type: {type(data)}")

# Helper functions
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

# Generate enriched pairs
for filename, text in items:
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

# Save as JSONL
with open("strategy_pairs_enriched.jsonl", "w") as f:
    for p in pairs:
        json.dump(p, f)
        f.write("\n")

print(f"✅ Created {len(pairs)} enriched strategy pairs in strategy_pairs_enriched.jsonl")
