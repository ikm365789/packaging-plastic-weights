"""
Packaging Plastic Weights — quickstart example.

Loads the dataset, validates a barcode, and looks up a few sample
receipt items. Run with:

    python examples/quickstart.py

Requires only the Python standard library.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------- Loading ----------

def load_products() -> list[dict]:
    with (DATA_DIR / "products.csv").open() as f:
        return list(csv.DictReader(f))


def load_categories() -> dict[str, dict]:
    with (DATA_DIR / "categories.csv").open() as f:
        return {row["category"]: row for row in csv.DictReader(f)}


# ---------- Barcode validation ----------

def _digits(code: str) -> str:
    return re.sub(r"\D", "", code or "")


def _ean13_check(body12: str) -> int:
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(body12))
    return (10 - total % 10) % 10


def _upca_check(body11: str) -> int:
    total = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(body11))
    return (10 - total % 10) % 10


def validate_barcode(raw: str) -> tuple[bool, str]:
    """Return (is_valid, normalized_form_or_error)."""
    d = _digits(raw)
    if len(d) == 12:
        return (int(d[11]) == _upca_check(d[:11]),
                "0" + d if int(d[11]) == _upca_check(d[:11]) else "checksum fail")
    if len(d) == 13:
        return (int(d[12]) == _ean13_check(d[:12]),
                d if int(d[12]) == _ean13_check(d[:12]) else "checksum fail")
    return (False, f"wrong length: {len(d)} digits")


# ---------- Lookup ----------

def lookup(receipt_text: str, products: list[dict], categories: dict[str, dict]) -> dict:
    """Look up a receipt line by name. Tries exact name, alias, keyword, then category fallback."""
    text = receipt_text.upper().strip()

    # Exact name match
    for p in products:
        if p["name"].upper() == text:
            return {"plastic_grams": float(p["plastic_grams"]),
                    "confidence": p["confidence"],
                    "method": "exact_name",
                    "product_id": p["id"]}

    # Alias match (aliases stored as JSON array string)
    import json
    for p in products:
        try:
            aliases = json.loads(p.get("aliases") or "[]")
        except json.JSONDecodeError:
            aliases = []
        if text in [a.upper() for a in aliases]:
            return {"plastic_grams": float(p["plastic_grams"]),
                    "confidence": p["confidence"],
                    "method": "alias",
                    "product_id": p["id"]}

    # Keyword overlap (looser)
    text_words = set(re.findall(r"\w+", text.lower()))
    best = None
    best_overlap = 0
    for p in products:
        keywords = [k.strip().lower() for k in (p.get("keywords") or "").split(",")]
        overlap = len(text_words & set(keywords))
        if overlap > best_overlap:
            best, best_overlap = p, overlap
    if best and best_overlap >= 2:
        return {"plastic_grams": float(best["plastic_grams"]),
                "confidence": best["confidence"],
                "method": "keyword",
                "product_id": best["id"]}

    # Last resort: nothing matched
    return {"plastic_grams": 0,
            "confidence": "unknown",
            "method": "no_match",
            "product_id": None}


# ---------- Demo ----------

if __name__ == "__main__":
    products = load_products()
    categories = load_categories()
    print(f"Loaded {len(products)} products, {len(categories)} categories\n")

    # Barcode validation
    print("Barcode validation:")
    for code in ["049000028928", "049000028927", "0698178830026", "abc"]:
        ok, note = validate_barcode(code)
        print(f"  {'✓' if ok else '✗'} {code:<16} {note}")
    print()

    # A simulated receipt
    receipt = [
        "OATLY OAT MILK",
        "WHOLE FOODS GENERIC MILK 1 GALLON",
        "BARNES & NOBLE COFFEE",  # noise / unknown
        "TJ OAT BEV",
    ]
    print("Receipt lookup:")
    total = 0
    for line in receipt:
        result = lookup(line, products, categories)
        total += result["plastic_grams"]
        print(f"  {line:<40} → {result['plastic_grams']:>5.0f}g  ({result['method']}, {result['confidence']})")
    print(f"\n  Total plastic: {total:.0f}g")
