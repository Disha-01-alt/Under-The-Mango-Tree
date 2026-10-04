import csv
import os
import sys
import json
import time
from dotenv import load_dotenv

# ----------------------------------------
# Ensure app is importable
# ----------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT)

load_dotenv()

from app.db.pg_vector_store import PGVectorStore
from app.llm_providers.api_client import get_llm_client

store = PGVectorStore()
llm = get_llm_client()

CSV_DIR = os.path.join(ROOT, "app/dataset")
CHECKPOINT_FILE = os.path.join(ROOT, "app/dataset", "ingestion_state.json")

BATCH_SIZE = 50          
EMBED_DELAY = 0.5        

# --- CHECKPOINT HELPERS ---
def load_checkpoint():
    """Reads the last processed row number for each file from JSON."""
    if not os.path.exists(CHECKPOINT_FILE):
        return {}
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_checkpoint(filename, last_row_idx):
    """Updates the checkpoint file with the latest row index."""
    data = load_checkpoint()
    data[filename] = last_row_idx
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- INGESTION FUNCTION ---
def ingest_csv(filename, table):
    path = os.path.join(CSV_DIR, filename)
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    # 1. Load existing progress
    checkpoints = load_checkpoint()
    last_processed_row = checkpoints.get(filename, 0)

    print(f"\n📥 Ingesting {filename} → {table}")
    if last_processed_row > 0:
        print(f"🔄 Resuming from row {last_processed_row + 1}...")

    records = []
    inserted = 0
    failed = 0
    
    # We track the highest row index currently in the buffer to update checkpoint safely
    current_batch_max_idx = 0 

    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=1):
            # 2. SKIP LOGIC: If we already did this row, skip it
            if idx <= last_processed_row:
                continue

            # --- MAPPING LOGIC ---
            if "Kanda/Book" in row:
                # Ramayana format
                chapter = f"{row.get('Kanda/Book', '').strip()} - {row.get('Sarga/Chapter', '').strip()}"
                verse = (row.get("Shloka/Verse Number") or "").strip()
                speaker = "Valmiki" 
                sanskrit = ""
                translation = (row.get("English Translation") or "").strip()
            else:
                # Gita/Yoga format
                chapter = (row.get("chapter") or "").strip()
                verse = (row.get("verse") or "").strip()
                speaker = (row.get("speaker") or "Unknown").strip()
                sanskrit = (row.get("sanskrit") or "").strip()
                translation = (row.get("translation") or "").strip()
            
            youtube = (row.get("youtube_link") or "").strip()
            download = (row.get("download_link") or "").strip()

            if not translation:
                print(f"⚠️ Row {idx}: Skipping due to empty translation.")
                # Even if we skip logic-wise, we mark this row 'processed' so we don't get stuck
                save_checkpoint(filename, idx) 
                continue

            text_for_embedding = f"""
Speaker: {speaker}
Source: {table.replace('_collection', '').capitalize()}
Location: {chapter} Verse {verse}
Sanskrit: {sanskrit}
Meaning: {translation}
""".strip()

            # --- EMBEDDING ---
            embedding = None
            for attempt in range(3):
                try:
                    embedding = llm.embed(text_for_embedding)
                    break
                except Exception as e:
                    print(f"⚠️ Row {idx}: embed retry {attempt + 1}/3 failed: {e}")
                    time.sleep(2)

            if embedding is None:
                print(f"❌ Row {idx}: Failed to generate embedding. Skipping.")
                failed += 1
                continue

            # Add to buffer
            records.append((
                embedding, chapter, verse, speaker, sanskrit, 
                translation, youtube, download, 
                json.dumps({"source": table, "filename": filename})
            ))
            
            # Update the tracker for the current batch
            current_batch_max_idx = idx

            if EMBED_DELAY > 0:
                time.sleep(EMBED_DELAY)

            # --- BATCH INSERT ---
            if len(records) >= BATCH_SIZE:
                try:
                    store.upsert_knowledge(table, records)
                    inserted += len(records)
                    print(f"✅ Inserted {len(records)} rows (up to row {current_batch_max_idx})")
                    
                    # 3. SAVE CHECKPOINT: Only after successful DB insert
                    save_checkpoint(filename, current_batch_max_idx)
                    
                    records.clear()
                except Exception as e:
                    print(f"❌ Batch insertion failed: {e}")
                    # Do NOT save checkpoint here, so we retry these rows next time
                    failed += len(records)
                    records.clear()

        # Final flush for remaining records
        if records:
            try:
                store.upsert_knowledge(table, records)
                inserted += len(records)
                save_checkpoint(filename, current_batch_max_idx) # Save final progress
                print(f"✅ Final batch inserted (up to row {current_batch_max_idx})")
            except Exception as e:
                print(f"❌ Final batch failed: {e}")
                failed += len(records)

    print(f"\n🎉 INGEST COMPLETE FOR {table.upper()}")
    print(f"✅ Successfully Inserted: {inserted}")
    print(f"❌ Failed/Skipped: {failed}")


if __name__ == "__main__":
    # The script will now auto-resume if interrupted
    ingest_csv("gita_collection.csv", "gita_collection")
    ingest_csv("yoga_collection.csv", "yoga_collection")
    ingest_csv("valmiki-ramayana-verses.csv", "ramayana_collection")
