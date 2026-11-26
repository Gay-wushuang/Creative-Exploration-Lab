#!/usr/bin/env python3
"""Reproducible local sampling of a real, caller-supplied public catalog snapshot. No network."""
import argparse
import hashlib
import json
import random
import secrets
from pathlib import Path
from urllib.parse import urlsplit

def sample(rows, count, seed):
    if not isinstance(rows, list) or not 1 <= count <= len(rows):
        raise ValueError('count must be within a nonempty list')
    seen = set()
    for item in rows:
        if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip() for k in ('title','source','url')):
            raise ValueError('each item needs nonempty title, source and url')
        u = urlsplit(item['url'])
        if u.scheme not in ('http','https') or not u.hostname or u.username or u.password:
            raise ValueError('public HTTP(S) source URL required')
        key = (item['title'].strip(), item['url'].strip())
        if key in seen:
            raise ValueError('duplicate catalog item; clean snapshot before sampling')
        seen.add(key)
    canonical = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode('utf-8')
    indices = random.Random(seed).sample(range(len(rows)), count)
    return {'scope':'supplied catalog snapshot only','seed':seed,'population':len(rows),'snapshot_sha256':hashlib.sha256(canonical).hexdigest(),'sample':[{'index':i,'item':rows[i]} for i in indices]}

def plan(seed):
    """Randomize sampling methods, not the knowledge universe or the provider results."""
    routes = ['provider_random', 'catalog_snapshot', 'link_walk']
    return {'scope':'sampling-method order only', 'seed':seed,
            'routes':random.Random(seed).sample(routes,len(routes)),
            'note':'Host must fetch real public records; this plan does not sample live knowledge.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path, nargs='?', help='local JSON array of publicly sourced title/source/url objects')
    parser.add_argument('--plan', action='store_true', help='randomize methods before looking for public records')
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--count', type=int, default=1)
    args = parser.parse_args()
    if args.plan == (args.snapshot is not None):
        parser.error('choose exactly one: --plan or a snapshot file')
    seed = args.seed if args.seed is not None else secrets.randbits(64)
    try:
        result = plan(seed) if args.plan else sample(json.loads(args.snapshot.read_text(encoding='utf-8')), args.count, seed)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError,OSError) as e:
        parser.error(str(e))
if __name__ == '__main__':
    main()
