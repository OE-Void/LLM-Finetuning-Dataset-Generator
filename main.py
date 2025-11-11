import os
import json
import time
import random
from Config.config import (
    BOLD_BRIGHT_CYAN,
    BOLD_BRIGHT_GREEN,
    BOLD_BRIGHT_MAGENTA,
    BOLD_BRIGHT_RED,
    BOLD_BRIGHT_YELLOW,
    RESET,
    DATASET_FILES_DIR
)
from Providers import DeepInfra

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(filepath, data):
    temp_path = filepath + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.replace(temp_path, filepath)  # atomic write

def iterate_output(item):
    """
    Continuously tries generating an output until success.
    No max retries – it keeps going forever until a valid response is returned.
    """
    instruction = item["instruction"]
    input_text = item.get("input", "")

    prompt = f"Instruction: {instruction}\nInput: {input_text}" if input_text else instruction
    while True:
        try:
            output = BASE_MODEL.generate(prompt=prompt)

            # Check if output is non-empty and valid
            if output and isinstance(output, str) and output.strip():
                return output
            else:
                print(f"{BOLD_BRIGHT_RED}⚠️ Empty output received. Retrying...{RESET}")

        except Exception as e:
            print(f"{BOLD_BRIGHT_RED}❌ Error while receiving output: {e}{RESET}")

        # Wait a random short time before retrying to avoid hammering the API
        wait = random.uniform(2, 5)
        print(f"{BOLD_BRIGHT_RED}⏳ Retrying in {wait:.1f} seconds...{RESET}")
        time.sleep(wait)

def process_file(filepath):
    print(f"{BOLD_BRIGHT_MAGENTA}Processing dataset file: {filepath}{RESET}")
    data = load_data(filepath)

    for idx, item in enumerate(data):
        if item.get("output"):
            continue

        print(f"{BOLD_BRIGHT_YELLOW}[{idx+1}/{len(data)}] {item['instruction'][:40]}...{RESET}")

        # Keep trying until valid output
        output = iterate_output(item)
        data[idx]["output"] = output
        print(f"{BOLD_BRIGHT_GREEN}Output generated successfully.{RESET}")

        # Save progress safely every 3 items
        if idx % 3 == 0:
            save_data(filepath, data)
            print(f"{BOLD_BRIGHT_CYAN}💾 Progress saved safely.\n{RESET}")

        # Small delay between items
        time.sleep(2)

    save_data(filepath, data)
    print(f"{BOLD_BRIGHT_GREEN}🎉 All items in {filepath} processed successfully.\n{RESET}")

# --- Run --- #
if __name__=="__main__":
    BASE_MODEL = DeepInfra(system_prompt="You are a helpful assistant.")
    for filepath in os.listdir(DATASET_FILES_DIR):
        if filepath.endswith(".json"):
            full_filepath = os.path.join(DATASET_FILES_DIR, filepath)
            process_file(full_filepath)
