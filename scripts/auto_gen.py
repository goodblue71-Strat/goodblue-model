import json
import random

# Load extracted text
with open("strategy_texts.json", "r") as f:
    data = json.load(f)

pairs = []

# Define some common instruction templates for your strategy model
templates = [
    "Summarize the key AI trends from this report.",
    "List the main companies and industries discussed.",
    "Extract the top 3 strategic insights relevant to business leaders.",
    "Explain the implications of this report for enterprise AI adoption.",
    "Generate a SWOT analysis summary based on this document.",
    "Identify the opportunities and risks mentioned in the report.",
    "Summarize the report in 3 bullet points for a C-suite audience."
]

# For each file’s text, generate a few examples
for filename, text in data.items():
    snippet = text[:2500]  # truncate for brevity if large
    for _ in range(3):
        pairs.append({
            "instruction": random.choice(templates),
            "input": snippet,
            "output": "Generated summary or insight placeholder."
        })

# Save as JSONL
with open("strategy_pairs.jsonl", "w") as f:
    for p in pairs:
        json.dump(p, f)
        f.write("\n")

print(f"Created {len(pairs)} instruction pairs in strategy_pairs.jsonl")