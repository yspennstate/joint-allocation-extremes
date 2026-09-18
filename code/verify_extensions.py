#!/usr/bin/env python3
"""Exact finite checks for the multiconstraint and Poisson-marking arguments.

The program tests finite identities, not asymptotic local limit theorems.
Requires only the Python standard library. All comparisons use Fraction.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

Vector = tuple[int, ...]


def add(x: tuple, y: tuple) -> tuple:
    return tuple(a + b for a, b in zip(x, y))


def scale(c, x: tuple) -> tuple:
    return tuple(c * a for a in x)


def norm2(x: tuple):
    return sum(a * a for a in x)


def conv(a: dict, b: dict) -> dict:
    out = defaultdict(int)
    for x, v in a.items():
        for y, w in b.items():
            out[add(x, y)] += v * w
    return dict(out)


def check_vector(weights: dict[Vector, int], n: int, block: set[int], rare: set[Vector]) -> dict:
    if not weights or n < 1 or not block <= set(range(n)):
        raise ValueError('Invalid weights, sample size, or coordinate block')
    dim = len(next(iter(weights)))
    if any(len(x) != dim or w <= 0 for x, w in weights.items()):
        raise ValueError('Weights must be positive on equally sized vectors')
    low = {x: w for x, w in weights.items() if x not in rare}
    if not low:
        raise ValueError('This test requires a nonempty complement')
    zero = (0,) * dim
    denominator = sum(weights.values())
    lowden = sum(low.values())
    mu = tuple(sum(F(w * x[j], denominator) for x, w in weights.items()) for j in range(dim))
    b = tuple(sum(F(w * x[j], lowden) for x, w in low.items()) for j in range(dim))
    q = F(sum(w for x, w in weights.items() if x in rare), denominator)
    a = tuple(sum(F(w * x[j], denominator) for x, w in weights.items() if x in rare) for j in range(dim))
    assert add(a, scale(-q, b)) == add(mu, scale(-1, b))
    lowsums = [{zero: 1}]
    for _ in range(n):
        lowsums.append(conv(lowsums[-1], low))
    totals = defaultdict(int)
    records = defaultdict(int)
    joint = defaultdict(int)
    mean_u = [F(0)] * dim
    second_u = F(0)
    configurations = 0
    centering = 0
    for word in itertools.product(weights, repeat=n):
        configurations += 1
        w = math.prod(weights[x] for x in word)
        prob = F(w, denominator ** n)
        s = tuple(sum(x[j] for x in word) for j in range(dim))
        record = tuple(x if i in block or x in rare else None for i, x in enumerate(word))
        totals[s] += w
        records[record] += w
        joint[record, s] += w
        u = [F(0)] * dim
        for i, x in enumerate(word):
            term = add(x, scale(-1, mu)) if i in block else add(
                scale(int(x in rare), add(x, scale(-1, b))), add(b, scale(-1, mu)))
            for j in range(dim):
                u[j] += term[j]
        revealed = [x for x in record if x is not None]
        k = tuple(sum(x[j] for x in revealed) for j in range(dim))
        residual_n = n - len(revealed)
        for target in (s, zero):
            left = add(add(target, scale(-1, k)), scale(-residual_n, b))
            right = add(add(target, scale(-n, mu)), scale(-1, tuple(u)))
            assert left == right
            centering += 1
        for j in range(dim):
            mean_u[j] += prob * u[j]
        second_u += prob * norm2(tuple(u))
    assert all(x == 0 for x in mean_u)
    variance = sum(F(w, denominator) * norm2(add(x, scale(-1, mu))) for x, w in weights.items())
    c = add(mu, scale(-1, b))
    rare_variance = sum(F(w, denominator) * norm2(add(
        scale(int(x in rare), add(x, scale(-1, b))), scale(-1, c))) for x, w in weights.items())
    assert second_u == len(block) * variance + (n - len(block)) * rare_variance
    upper = len(block) * variance + (n - len(block)) * sum(
        F(w, denominator) * norm2(add(x, scale(-1, b))) for x, w in weights.items() if x in rare)
    assert second_u <= upper
    density_equalities = 0
    for s, totalw in totals.items():
        norm = F(0)
        abs_diff = F(0)
        negative_diff = F(0)
        for record, recordw in records.items():
            revealed = [x for x in record if x is not None]
            k = tuple(sum(x[j] for x in revealed) for j in range(dim))
            nn = n - len(revealed)
            wanted = add(s, scale(-1, k))
            ratio = F(lowsums[nn].get(wanted, 0), lowden ** nn) / F(totalw, denominator ** n)
            actual = F(joint[record, s] * denominator ** n, totalw * recordw)
            assert ratio == actual
            pr = F(recordw, denominator ** n)
            norm += pr * ratio
            abs_diff += pr * abs(ratio - 1)
            negative_diff += pr * max(F(0), 1 - ratio)
            density_equalities += 1
        assert norm == 1 and abs_diff / 2 == negative_diff
    return {'dimension': dim, 'sample_size': n, 'block': sorted(block),
            'configurations': configurations, 'density_equalities': density_equalities,
            'centering_identities': centering, 'conditioning_totals': len(totals),
            'second_centered_revealed_moment': str(second_u)}


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def valid(word: tuple[int, ...]) -> bool:
    s = 0
    for k in word[:-1]:
        s += k - 1
        if s < 0:
            return False
    return sum(word) == len(word) - 1


def check_leaf_rotations() -> dict:
    words = 0
    classes = 0
    rotations = 0
    for n in range(2, 9):
        allwords = defaultdict(int)
        treewords = defaultdict(int)
        for word in compositions(n - 1, n):
            words += 1
            leaves = word.count(0)
            shifts = [word[j:] + word[:j] for j in range(n)]
            assert len(set(shifts)) == n
            assert sum(valid(x) for x in shifts) == 1
            assert all(x.count(0) == leaves for x in shifts)
            rotations += n
            allwords[leaves] += 1
            treewords[leaves] += int(valid(word))
        for leaves in allwords:
            assert allwords[leaves] == n * treewords[leaves]
            classes += 1
    return {'degree_words': words, 'rotations': rotations, 'leaf_classes': classes}


def check_common_marking_kernel() -> dict:
    # The Poisson proof uses this identity for a countable total-count law.
    # Here two finite rational total-count laws test its algebra exactly.
    laws = [([F(1, 2), F(1, 3), F(1, 6)], [F(1, 4), F(1, 4), F(1, 2)]),
            ([F(0), F(1, 2), F(0), F(1, 2)], [F(1, 8), F(1, 8), F(1, 4), F(1, 2)])]
    marks = (F(1, 2), F(1, 3), F(1, 6))
    equations = 0
    for p, q in laws:
        total_tv = sum(abs(a - b) for a, b in zip(p, q)) / 2
        marked_tv = F(0)
        for n, (pn, qn) in enumerate(zip(p, q)):
            mass = F(0)
            for counts in compositions(n, len(marks)):
                multinomial = F(math.factorial(n), math.prod(math.factorial(c) for c in counts))
                kernel = multinomial * math.prod(a ** c for a, c in zip(marks, counts))
                mass += kernel
                marked_tv += abs(pn - qn) * kernel / 2
                equations += 1
            assert mass == 1
        assert total_tv == marked_tv
    return {'marking_terms': equations, 'distance_equalities': len(laws)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('extension_checks.json'))
    args = parser.parse_args()
    leaf = {(0, 1): 4, (1, 0): 3, (2, 0): 2, (4, 0): 1}
    signed = {(-1, 0): 1, (0, 0): 2, (0, 1): 3, (2, -1): 1}
    vector3 = {(0, 1, 0): 2, (1, 0, 1): 3, (2, 0, 0): 2, (3, 0, 0): 1}
    cases = [(leaf, 5, {0, 3}, {(4, 0)}), (leaf, 5, set(), {(0, 1), (4, 0)}),
             (signed, 4, {2}, {(-1, 0), (2, -1)}), (leaf, 4, {0}, set()),
             (vector3, 4, {0, 2}, {(3, 0, 0)})]
    results = [check_vector(*case) for case in cases]
    out = {'all_checks_passed': True,
           'scope': 'Exact finite identities only; not a formal or numerical proof of the limiting theorems.',
           'vector_cases': results,
           'totals': {key: sum(r[key] for r in results) for key in
                      ('configurations', 'density_equalities', 'centering_identities', 'conditioning_totals')},
           'leaf_rotations': check_leaf_rotations(),
           'common_marking_kernel': check_common_marking_kernel()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
