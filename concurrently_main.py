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
from Providers import Nvidia
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- File I/O ---
def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(filepath, data):
    temp_path = filepath + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.replace(temp_path, filepath)  # atomic write

# --- Output Generation ---
def generate_output(item):
    """
    Generates model output for a single item with retry logic.
    Runs safely inside threads.
    """
    instruction = item["instruction"]
    input_text = item.get("input", "")
    prompt = f"Instruction: {instruction}\nInput: {input_text}" if input_text else instruction

    while True:
        try:
            output = BASE_MODEL.generate(prompt=prompt)

            if output and isinstance(output, str) and output.strip():
                return output.strip()
            else:
                print(f"{BOLD_BRIGHT_RED}⚠️ Empty output received. Retrying...{RESET}")
        except Exception as e:
            print(f"{BOLD_BRIGHT_RED}❌ Error while generating output: {e}{RESET}")

        wait = random.uniform(2, 5)
        print(f"{BOLD_BRIGHT_RED}⏳ Retrying in {wait:.1f} seconds...{RESET}")
        time.sleep(wait)

# --- Main Processing ---
def process_file(filepath, batch_size=3):
    print(f"{BOLD_BRIGHT_MAGENTA}Processing dataset file: {filepath}{RESET}")
    data = load_data(filepath)

    total = len(data)
    for i in range(0, total, batch_size):
        batch = data[i:i + batch_size]

        # Skip batch if all already have output
        if all("output" in item and item["output"] for item in batch):
            continue

        print(f"{BOLD_BRIGHT_YELLOW}\n🔹 Processing items {i+1} to {min(i+batch_size, total)} / {total}{RESET}")

        # --- Run batch concurrently ---
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = {executor.submit(generate_output, item): idx for idx, item in enumerate(batch)}

            # Collect results in the same order
            results = [None] * len(batch)
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    results[idx] = result
                    print(f"{BOLD_BRIGHT_GREEN}✅ Output generated for item {i+idx+1}{RESET}")
                except Exception as e:
                    print(f"{BOLD_BRIGHT_RED}❌ Failed for item {i+idx+1}: {e}{RESET}")
                    results[idx] = None

        # --- Save results to data safely in order ---
        for j, output in enumerate(results):
            if output:
                data[i + j]["output"] = output

        save_data(filepath, data)
        print(f"{BOLD_BRIGHT_CYAN}💾 Progress saved after batch {i//batch_size + 1}.{RESET}")

        # Small delay between batches
        time.sleep(2)

    print(f"{BOLD_BRIGHT_GREEN}🎉 All items in {filepath} processed successfully!\n{RESET}")

# --- Run ---
if __name__=="__main__":
    BASE_MODEL = Nvidia(api_key="nvapi-AOxxxx", system_prompt="You are a helpful assistant.")
    for filepath in os.listdir(DATASET_FILES_DIR):
        if filepath.endswith(".json"):
            full_filepath = os.path.join(DATASET_FILES_DIR, filepath)
            process_file(full_filepath, batch_size=3)
