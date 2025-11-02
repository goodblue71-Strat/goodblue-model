import json

with open("strategy_pairs_filled.jsonl") as f:
    for i, line in enumerate(f):
        if i == 3: break
        print(json.dumps(json.loads(line), indent=2)[:700], "\n---")
