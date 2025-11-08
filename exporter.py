import pandas as pd
import json
import os

def export_to_csv(data, filename="output/threads_data.csv"):
    os.makedirs("output", exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"[+] CSV was saved: {filename}")

def export_to_json(data, filename="output/threads_data.json"):
    os.makedirs("output", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[+] JSON was saved: {filename}")
