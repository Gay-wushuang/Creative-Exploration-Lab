#!/usr/bin/env python3
"""Draw independent creativity stimuli; stdlib only, reproducible via seed."""
import argparse
import json
import random
import secrets
from pathlib import Path

def draw(pool, seed, count):
    if not 1 <= count <= len(pool):
        raise ValueError('count outside available categories')
    if any(not items or len(items) != len(set(items)) for items in pool.values()):
        raise ValueError('empty category or duplicate cards')
    rng = random.Random(seed)
    categories = rng.sample(sorted(pool), count)
    return {'seed': seed, 'cards': [{'category': c, 'card': rng.choice(pool[c])} for c in categories]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--count', type=int, default=3)
    args = parser.parse_args()
    pool = json.loads((Path(__file__).resolve().parent.parent / 'cards/pool.json').read_text(encoding='utf-8'))
    seed = args.seed if args.seed is not None else secrets.randbits(64)
    try:
        result = draw(pool, seed, args.count)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
