import json
import time
from openai import OpenAI

# ---------------------------
# 1. Initialize OpenAI client
# ---------------------------
client = OpenAI()  # Make sure OPENAI_API_KEY is set in your environment or Streamlit secrets

input_file = "data/processed/strategy_pairs_enriched.jsonl"
output_file = "data/train/strategy_pairs_filled.jsonl"

# ---------------------------
# 2. Load the enriched data
# ---------------------------
pairs = []
with open(input_file, "r") as f:
    for line in f:
        try:
            pairs.append(json.loads(line))
        except json.JSONDecodeError:
            continue

print(f"📚 Loaded {len(pairs)} enriched pairs from {input_file}")

# ---------------------------
# 3. Generate real outputs
# ---------------------------
filled = []
for i, record in enumerate(pairs):
    instruction = record.get("instruction", "")
    input_text = record.get("input", "")[:4000].strip()

    # Skip empty cases
    if not input_text:
        continue

    prompt = (
        f"You are an expert AI strategy consultant.\n\n"
        f"Instruction: {instruction}\n\n"
        f"Document excerpt:\n{input_text}\n\n"
        f"Provide a well-structured and insightful answer for a strategy audience. "
        f"Keep the tone professional and concise."
    )

    try:
        # Use a smaller model to save cost (can switch to 'gpt-4-turbo' or 'gpt-4.1-mini')
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=300
        )
        output_text = response.output_text.strip()

        # Add the new output
        record["output"] = output_text
        filled.append(record)

        # Print progress every few records
        if (i + 1) % 5 == 0:
            print(f"✅ Processed {i + 1}/{len(pairs)} records...")

        # Throttle slightly to avoid rate limits
        time.sleep(1.5)

    except Exception as e:
        print(f"⚠️ Error on record {i}: {e}")
        time.sleep(3)
        continue

# ---------------------------
# 4. Save the final JSONL
# ---------------------------
if filled:
    with open(output_file, "w") as f:
        for rec in filled:
            json.dump(rec, f)
            f.write("\n")
    print(f"🎯 Saved {len(filled)} GPT-filled pairs to {output_file}")
    print(f"💡 Example output:\n{json.dumps(filled[0], indent=2)[:700]}")
else:
    print("⚠️ No valid pairs generated. Check your input file or API key.")
