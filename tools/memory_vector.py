#!/usr/bin/env python3
"""Shared semantic memory bus — Rook + Castle hydration -> Qdrant.

Usage:
  python3 tools/memory_vector.py ingest [--files data/memory-bus/rook-hydration.jsonl ...]
  python3 tools/memory_vector.py query "<text>" [-k 5]
  python3 tools/memory_vector.py stats

No LLM on the read path. Embeddings: bge-m3 (cached at ~/.cache/huggingface).
Citations are path-only from the hydration files (they carry path, no line ranges).
"""
import argparse, json, sys, os, time

QDRANT_URL = os.environ.get('QDRANT_URL', 'http://127.0.0.1:6333')
COLLECTION = os.environ.get('MEMORY_BUS_COLLECTION', 'memory_bus')
EMBED_MODEL = os.environ.get('MEMORY_BUS_EMBED', 'BAAI/bge-m3')

def get_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL, device='cpu')

def ensure_collection(dim):
    from qdrant_client import QdrantClient
    from qdrant_client.models import VectorParams, Distance
    client = QdrantClient(url=QDRANT_URL, timeout=30)
    cols = {c.name for c in client.get_collections().collections}
    if COLLECTION not in cols:
        client.create_collection(COLLECTION, vectors_config=VectorParams(size=dim, distance=Distance.COSINE))
        print(f'[bus] created collection {COLLECTION} dim={dim}', flush=True)
    return client

def ingest(files):
    model = get_embedder()
    dim = model.get_sentence_embedding_dimension()
    client = ensure_collection(dim)
    from qdrant_client.models import PointStruct
    total = 0
    for f in files:
        batch, ids = [], []
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                batch.append(rec['text'])
                ids.append(rec)
                if len(batch) >= 32:
                    vecs = model.encode(batch, normalize_embeddings=True, show_progress_bar=False)
                    pts = [PointStruct(id=abs(hash(r['id'])) % (2**63), vector=list(map(float, v)),
                                       payload=r) for r, v in zip(ids, vecs)]
                    client.upsert(COLLECTION, points=pts)
                    total += len(pts); batch, ids = [], []
        if batch:
            vecs = model.encode(batch, normalize_embeddings=True, show_progress_bar=False)
            pts = [PointStruct(id=abs(hash(r['id'])) % (2**63), vector=list(map(float, v)),
                               payload=r) for r, v in zip(ids, vecs)]
            client.upsert(COLLECTION, points=pts)
            total += len(pts)
        print(f'[bus] ingested {f} total={total}', flush=True)
    print(f'[bus] done total={total}', flush=True)

def query(text, k):
    model = get_embedder()
    client = ensure_collection(model.get_sentence_embedding_dimension())
    vec = model.encode([text], normalize_embeddings=True)[0]
    res = client.query_points(COLLECTION, query=list(map(float, vec)), limit=k).points
    for p in res:
        pl = p.payload or {}
        print(f'{p.score:.3f} | {pl.get("source")} | {pl.get("path")} | {pl.get("text","")[:160]}')

def stats():
    from qdrant_client import QdrantClient
    client = QdrantClient(url=QDRANT_URL, timeout=10)
    try:
        info = client.get_collection(COLLECTION)
        print(f'collection={COLLECTION} points={info.points_count} status={info.status}')
    except Exception as e:
        print(f'collection missing or error: {e}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    ing = sub.add_parser('ingest'); ing.add_argument('--files', nargs='+', required=True)
    q = sub.add_parser('query'); q.add_argument('text'); q.add_argument('-k', type=int, default=5)
    sub.add_parser('stats')
    args = ap.parse_args()
    if args.cmd == 'ingest':
        ingest(args.files)
    elif args.cmd == 'query':
        query(args.text, args.k)
    else:
        stats()
