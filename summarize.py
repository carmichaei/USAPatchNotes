# summarize.py
import os
import json
from datetime import datetime
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

TEMPLATE = """
**Patch Notes: {title}**

Summary:
{summary}

Patch Impact:
{impact}
"""

def load_latest_raw():
    raw_dir = "data/raw"
    files = sorted(
        [f for f in os.listdir(raw_dir) if f.endswith(".json")],
        reverse=True
    )
    if not files:
        raise FileNotFoundError("No raw EO files found.")
    latest_file = os.path.join(raw_dir, files[0])
    with open(latest_file, "r") as f:
        data = json.load(f)
    return data.get("results", []), files[0].split("_")[1].split(".")[0]  # returns EOs + date string

def initialize_model():
    model_id = "tiiuae/falcon-rw-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

def style_patch_note(eo, summarizer):
    raw_text = eo.get("summary", eo.get("title", ""))
    prompt = f"Rewrite this executive order summary like it's a League of Legends patch note. Be concise and slightly humorous.\n\n'{raw_text}'\n\nPatch Note:"
    response = summarizer(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    return response[0]["generated_text"].split("Patch Note:")[-1].strip()

def save_patch_notes(patch_notes, date_str):
    os.makedirs("data/processed", exist_ok=True)
    file_path = f"data/processed/patch_notes_{date_str}.md"
    with open(file_path, "w") as f:
        f.write("\n\n".join(patch_notes))
    print(f"Saved patch notes to {file_path}")

if __name__ == "__main__":
    eos, date_str = load_latest_raw()
    summarizer = initialize_model()
    notes = [style_patch_note(eo, summarizer) for eo in eos]
    save_patch_notes(notes, date_str)

