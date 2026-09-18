#!/usr/bin/env python3
"""Exact finite checks for rare-record conditioning (Python standard library).

These checks verify finite identities, not the asymptotic theorems.
Run: python verify.py --output checks.json
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Callable


def convolution(a: dict[int, int], b: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for x, v in a.items():
        for y, w in b.items():
            out[x + y] += v * w
    return dict(out)


def sums(weights: dict[int, int], n: int) -> list[dict[int, int]]:
    out = [{0: 1}]
    for _ in range(n):
        out.append(convolution(out[-1], weights))
    return out


def check_records(weights: dict[int, int], n: int, rare: set[int], a: int, d: int) -> dict:
    if n < 1 or not weights or any(w <= 0 for w in weights.values()):
        raise ValueError("Positive weights and sample size are required")
    if not set(weights) - rare:
        raise ValueError("A nonempty low support is required for this finite check")
    if any((x - a) % d for x in weights):
        raise ValueError("Wrong lattice")
    normalizer = sum(weights.values()) ** n
    low = {x: w for x, w in weights.items() if x not in rare}
    low_mass = sum(low.values())
    low_sums = sums(low, n)
    total: dict[int, int] = defaultdict(int)
    records: dict[tuple, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    clouds: dict[tuple, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    configurations = 0
    for sample in itertools.product(weights, repeat=n):
        w = math.prod(weights[x] for x in sample)
        m = sum(sample)
        z = tuple(x if x in rare else None for x in sample)
        cloud = tuple(sorted(x for x in sample if x in rare))
        records[z][m] += w
        clouds[cloud][m] += w
        total[m] += w
        configurations += 1
    assert sum(total.values()) == normalizer
    checks = 0
    representative_tv = {}
    for name, groups in (("indexed", records), ("multiset", clouds)):
        for m, denominator_weight in sorted(total.items()):
            tv = Fraction(0)
            negative_part = Fraction(0)
            density_mean = Fraction(0)
            for key, joint in groups.items():
                revealed = tuple(x for x in key if x is not None)
                r, k = len(revealed), sum(revealed)
                assert (m - k - (n - r) * a) % d == 0
                p_record = Fraction(sum(joint.values()), normalizer)
                p_cond = Fraction(joint.get(m, 0), denominator_weight)
                density = p_cond / p_record
                p_low = Fraction(low_sums[n - r].get(m - k, 0), low_mass ** (n - r))
                formula = p_low / Fraction(denominator_weight, normalizer)
                assert density == formula, (name, m, key)
                tv += abs(p_cond - p_record) / 2
                negative_part += p_record * max(1 - density, 0)
                density_mean += p_record * density
                checks += 1
            assert density_mean == 1
            assert tv == negative_part
            if m == round(n * sum(x * w for x, w in weights.items()) / sum(weights.values())):
                representative_tv[name] = {"exact": str(tv), "decimal": float(tv), "target": m}
    return {"weights": weights, "n": n, "rare_values": sorted(rare), "lattice": [a, d],
            "configurations": configurations, "indexed_records": len(records),
            "rare_multisets": len(clouds), "targets": len(total),
            "exact_density_equalities": checks, "representative_tv": representative_tv,
            "status": "PASS"}


def check_tilts() -> dict:
    weights = {0: 4, 1: 3, 2: 2, 5: 1}
    c, d, n = 2, 3, 5
    max_x = max(weights)
    tilted = {x: w * c ** x * d ** (max_x - x) for x, w in weights.items()}
    s0, s1 = sums(weights, n)[n], sums(tilted, n)[n]
    checked = 0
    for sample in itertools.product(weights, repeat=n):
        m = sum(sample)
        p0 = Fraction(math.prod(weights[x] for x in sample), s0[m])
        p1 = Fraction(math.prod(tilted[x] for x in sample), s1[m])
        assert p0 == p1
        checked += 1
    return {"n": n, "tilt": "2/3", "conditional_point_equalities": checked, "status": "PASS"}


def compositions(total: int, length: int):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


def valid_degree_word(word: tuple[int, ...]) -> bool:
    partial = 0
    for x in word[:-1]:
        partial += x - 1
        if partial < 0:
            return False
    return partial + word[-1] - 1 == -1


def check_trees() -> dict:
    results = []
    for n in range(2, 9):
        allocation = defaultdict(int)
        tree = defaultdict(int)
        count = 0
        for word in compositions(n - 1, n):
            good = [j for j in range(n) if valid_degree_word(word[j:] + word[:j])]
            assert len(good) == 1
            # An arbitrary positive weight on each finite support value.
            weight = math.prod(x + 1 for x in word)
            key = tuple(sorted(word, reverse=True))
            allocation[key] += weight
            if valid_degree_word(word):
                tree[key] += weight
            count += 1
        assert all(allocation[key] == n * tree[key] for key in allocation)
        results.append({"n": n, "degree_words": count, "rank_types": len(allocation)})
    return {"cases": results, "status": "PASS"}


def check_overflow() -> dict:
    # With p(0)=1/2, p(1)=p(3)=1/4, a count on [1,1] misses value 3.
    n = 4
    no_truncated_exceedance = Fraction(3, 4) ** n
    actual_max_below_one = Fraction(1, 2) ** n
    difference = no_truncated_exceedance - actual_max_below_one
    assert difference > 0
    return {"n": n, "truncated_count_zero": str(no_truncated_exceedance),
            "maximum_below_one": str(actual_max_below_one), "difference": str(difference),
            "conclusion": "A truncated exceedance count requires a separate overflow event", "status": "PASS"}


def check_residual_algebra() -> dict:
    checked = 0
    for n in (3, 7, 20):
        for q in (Fraction(0), Fraction(1, 10), Fraction(2, 5)):
            mu, tail_mean = Fraction(7, 3), Fraction(2, 3) * q
            low_mean = (mu - tail_mean) / (1 - q)
            for r in range(n + 1):
                for k in (r, 2 * r, 5 * r):
                    for m in (n, 2 * n, 3 * n):
                        left = m - k - (n - r) * low_mean
                        right = (m - n * mu) - (k - n * tail_mean) + (r - n * q) * low_mean
                        assert left == right
                        checked += 1
    return {"exact_equalities": checked, "status": "PASS"}



def check_censored_ranks() -> dict:
    """Check threshold padding, including ties and upper overflow."""
    support = (0, 2, 3, 7)
    cases = 0
    for n in range(1, 7):
        for sample in itertools.product(support, repeat=n):
            for a, b in ((0, 3), (2, 3), (2, 7), (3, 7)):
                retained = sorted((x for x in sample if a < x <= b), reverse=True)
                for k in range(1, n + 1):
                    if max(sample) <= b and sum(x >= a for x in sample) >= k:
                        padded = (retained + [a] * k)[:k]
                        assert padded == sorted(sample, reverse=True)[:k]
                        cases += 1
    return {"identities": cases, "max_sample_size": 6, "status": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("checks.json"))
    args = parser.parse_args()
    results = {
        "description": "Exact rational finite identities only; not asymptotic proof certification",
        "record_cases": [
            check_records({0: 4, 1: 3, 2: 2, 5: 1}, 6, {2, 5}, 0, 1),
            check_records({1: 2, 3: 3, 5: 1, 9: 1}, 5, {5, 9}, 1, 2),
            check_records({0: 4, 1: 3, 2: 2, 5: 1}, 5, {1, 5}, 0, 1),
            check_records({0: 1, 2: 2, 4: 1}, 5, set(), 0, 2),
            check_records({-3: 2, -1: 1, 1: 4, 5: 1}, 5, {-3, 5}, 1, 2),
        ],
        "tilt_invariance": check_tilts(),
        "tree_cycle_identity": check_trees(),
        "overflow_counterexample": check_overflow(),
        "residual_centering": check_residual_algebra(),
        "censored_rank_identity": check_censored_ranks(),
        "all_checks_passed": True,
    }
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_checks_passed": True,
        "density_equalities": sum(x["exact_density_equalities"] for x in results["record_cases"]),
        "enumerated_iid_configurations": sum(x["configurations"] for x in results["record_cases"]),
        "tree_degree_words": sum(x["degree_words"] for x in results["tree_cycle_identity"]["cases"]),
        "output": str(args.output)}, indent=2))

if __name__ == "__main__":
    main()
