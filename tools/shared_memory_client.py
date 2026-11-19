#!/usr/bin/env python3
"""
Shared Memory Client — Castle & Rook Boundary Pipe (Cloudflare Tunnel Edition)
Connects Castle (HPE) to Rook's T340 services via Cloudflare tunnels.

Usage:
    python3 shared_memory_client.py --action <search|upsert|health>
"""

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

CONFIG_PATH = Path(__file__).parent / "boundary_pipe_config.json"

def load_config():
    """Load tunnel endpoints from config."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}

def get_endpoint(service, config):
    """Get the best available endpoint for a service."""
    tunnels = config.get("tunnels", {})
    recommended = config.get("recommended_for_castle", {})
    
    # Try recommended first
    if service in recommended:
        return recommended[service]
    
    # Fallback: find any tunnel for this service
    for name, info in tunnels.items():
        if service in name:
            return info.get("url")
    
    return None

def http_get(url, timeout=10, retries=2):
    """Simple GET request with retries."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers={"User-Agent": "castle-rook-shared-memory/1.0"})
            with urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except (URLError, HTTPError, TimeoutError) as e:
            last_error = e
            if attempt < retries:
                time.sleep(1)
    return f"ERROR: {last_error}"

def http_post(url, data, timeout=10, retries=2):
    """Simple POST request with JSON body and retries."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            body = json.dumps(data).encode("utf-8")
            req = Request(url, data=body, headers={
                "Content-Type": "application/json",
                "User-Agent": "castle-rook-shared-memory/1.0"
            })
            with urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except (URLError, HTTPError, TimeoutError) as e:
            last_error = e
            if attempt < retries:
                time.sleep(1)
    return f"ERROR: {last_error}"

def qdrant_health(qdrant_url):
    """Check Qdrant health via tunnel."""
    return http_get(qdrant_url)

def qdrant_collections(qdrant_url):
    """List Qdrant collections."""
    return http_get(f"{qdrant_url}/collections")

def qdrant_search(qdrant_url, collection, vector, limit=10):
    """Search Qdrant collection via tunnel."""
    payload = {"vector": vector, "limit": limit, "with_payload": True}
    return http_post(f"{qdrant_url}/collections/{collection}/points/search", payload)

def qdrant_upsert(qdrant_url, collection, points):
    """Upsert points to Qdrant collection."""
    payload = {"points": points}
    return http_post(f"{qdrant_url}/collections/{collection}/points", payload)

def survival_health(survival_url):
    """Check survival backend health."""
    return http_get(f"{survival_url}/api/health")

def survival_search(survival_url, query, k=5):
    """Search survival backend RAG."""
    payload = {"query": query, "k": k}
    return http_post(f"{survival_url}/api/search", payload)

def survival_ask(survival_url, query):
    """Ask survival backend with LLM."""
    payload = {"query": query}
    return http_post(f"{survival_url}/api/ask", payload)

def searxng_search(searxng_url, query, format="json"):
    """Search SearXNG."""
    from urllib.parse import urlencode
    params = urlencode({"q": query, "format": format})
    return http_get(f"{searxng_url}/search?{params}")

def main():
    config = load_config()
    
    # Get endpoints
    qdrant_url = get_endpoint("qdrant", config)
    survival_url = get_endpoint("survival", config)
    searxng_url = get_endpoint("searxng", config)
    
    parser = argparse.ArgumentParser(description="Shared Memory Client for Castle-Rook Boundary Pipe")
    parser.add_argument("--qdrant-url", default=qdrant_url, help="Qdrant Cloudflare tunnel URL")
    parser.add_argument("--survival-url", default=survival_url, help="Survival backend Cloudflare tunnel URL")
    parser.add_argument("--searxng-url", default=searxng_url, help="SearXNG Cloudflare tunnel URL")
    parser.add_argument("--action", required=True, choices=[
        "qdrant-health", "qdrant-collections", "qdrant-search", "qdrant-upsert",
        "survival-health", "survival-search", "survival-ask",
        "searxng-search"
    ], help="Action to perform")
    
    # Search/ask parameters
    parser.add_argument("--collection", default="memory_bus", help="Qdrant collection name")
    parser.add_argument("--vector", help="Search vector (JSON array)")
    parser.add_argument("--limit", type=int, default=10, help="Search limit")
    parser.add_argument("--query", help="Query string for survival/searxng")
    parser.add_argument("--points", help="Points to upsert (JSON array)")
    
    args = parser.parse_args()
    
    if not args.qdrant_url and args.action.startswith("qdrant"):
        print("ERROR: No Qdrant URL available in config or via --qdrant-url")
        sys.exit(1)
    if not args.survival_url and args.action.startswith("survival"):
        print("ERROR: No survival URL available in config or via --survival-url")
        sys.exit(1)
    if not args.searxng_url and args.action == "searxng-search":
        print("ERROR: No SearXNG URL available in config or via --searxng-url")
        sys.exit(1)
    
    if args.action == "qdrant-health":
        print(qdrant_health(args.qdrant_url))
    elif args.action == "qdrant-collections":
        print(qdrant_collections(args.qdrant_url))
    elif args.action == "qdrant-search":
        if not args.vector:
            print("ERROR: --vector required for qdrant-search")
            sys.exit(1)
        vector = json.loads(args.vector)
        print(qdrant_search(args.qdrant_url, args.collection, vector, args.limit))
    elif args.action == "qdrant-upsert":
        if not args.points:
            print("ERROR: --points required for qdrant-upsert")
            sys.exit(1)
        points = json.loads(args.points)
        print(qdrant_upsert(args.qdrant_url, args.collection, points))
    elif args.action == "survival-health":
        print(survival_health(args.survival_url))
    elif args.action == "survival-search":
        if not args.query:
            print("ERROR: --query required for survival-search")
            sys.exit(1)
        print(survival_search(args.survival_url, args.query, args.limit))
    elif args.action == "survival-ask":
        if not args.query:
            print("ERROR: --query required for survival-ask")
            sys.exit(1)
        print(survival_ask(args.survival_url, args.query))
    elif args.action == "searxng-search":
        if not args.query:
            print("ERROR: --query required for searxng-search")
            sys.exit(1)
        print(searxng_search(args.searxng_url, args.query))

if __name__ == "__main__":
    main()
