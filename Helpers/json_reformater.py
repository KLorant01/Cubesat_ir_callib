import json
import time

data = json.loads(input("JSON file: "))
output_file = f"numeric_variable_formatted_{time.time()}.json"

# Mentés szépen formázva
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)

print("fin")