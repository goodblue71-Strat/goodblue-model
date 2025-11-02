import json

file_path = "strategy_pairs_filled.jsonl"

required_fields = ["instruction", "input", "output"]

print(f"🔍 Validating file: {file_path}\n")

total = 0
invalid_json = 0
missing_fields = 0
empty_fields = 0
valid_records = 0

sample_examples = []

with open(file_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, start=1):
        total += 1
        line = line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            invalid_json += 1
            print(f"❌ Invalid JSON at line {line_num}: {e}")
            continue

        # Check required fields
        missing = [k for k in required_fields if k not in record]
        if missing:
            missing_fields += 1
            print(f"⚠️ Missing fields {missing} at line {line_num}")
            continue

        # Check for emptiness
        empty = [k for k in required_fields if not str(record[k]).strip()]
        if empty:
            empty_fields += 1
            print(f"⚠️ Empty fields {empty} at line {line_num}")
            continue

        valid_records += 1
        if len(sample_examples) < 3:
            sample_examples.append(record)

print("\n🧾 Validation Summary")
print("-" * 40)
print(f"Total lines checked: {total}")
print(f"✅ Valid records: {valid_records}")
print(f"❌ Invalid JSON lines: {invalid_json}")
print(f"⚠️ Records missing fields: {missing_fields}")
print(f"⚠️ Records with empty fields: {empty_fields}")
print("-" * 40)

if sample_examples:
    print("\n📘 Sample valid records:")
    for ex in sample_examples:
        print(json.dumps(ex, indent=2)[:800])
        print("-" * 80)
else:
    print("No valid examples found.")
