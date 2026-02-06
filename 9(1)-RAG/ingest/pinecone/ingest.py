"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    # TODO: Implement Pinecone upsert
    
    embeddings_path = PROCESSED_DIR / "embeddings.npy"
    ids_path = PROCESSED_DIR / "embedding_ids.json"
    corpus_path = RAW_DIR / "corpus.jsonl"

    if not embeddings_path.exists() or not ids_path.exists():
        raise FileNotFoundError(f"Embeddings or ID cache not found. Plz run embedding first.")
    
    if not corpus_path.exists():
        print(f"Corpus file not found at {corpus_path}.")

    print("Loading embeddings and IDs...")
    embeddings = np.load(embeddings_path)
    
    ids = json.loads(ids_path.read_text(encoding="utf-8"))

    if len(embeddings) != len(ids):
        raise ValueError("Data mismatch")

    id_to_text = {}
    if corpus_path.exists():
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    doc = json.loads(line)
                    if "id" in doc and "text" in doc:
                        id_to_text[doc["id"]] = doc["text"]
                except json.JSONDecodeError:
                    continue  

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX", "ybragsession") 

    if not api_key:
        raise ValueError("PINECONE_API_KEY environment variable is missing.")

    try:
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)
    except Exception as e:
        print(f"Failed to connect to Pinecone index '{index_name}': {e}")
        raise

    total_vectors = len(ids)
    upserted_count = 0
        
    for i in tqdm(range(0, total_vectors, BATCH_SIZE), desc="Upserting"):
        batch_ids = ids[i : i + BATCH_SIZE]
        batch_vecs = embeddings[i : i + BATCH_SIZE]
        
        vectors = []
        for vec_id, vec_emb in zip(batch_ids, batch_vecs):
            text = id_to_text.get(vec_id, "")
            
            if len(text) > TEXT_LIMIT:
                text = text[:TEXT_LIMIT]
            
            vectors.append({
                "id": vec_id,
                "values": vec_emb.tolist(),
                "metadata": {"text": text}
            })

        if vectors:
            try:
                index.upsert(vectors=vectors)
                upserted_count += len(vectors)
                
                if progress_callback:
                    progress_callback(upserted_count, total_vectors)
                    
            except Exception as e:
                print(f"Error upserting batch starting at index {i}: {e}")

    return upserted_count

if __name__ == "__main__":
    ingest()
