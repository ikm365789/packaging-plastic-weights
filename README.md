# Loop Plastic Data

An open dataset of **plastic packaging weights** for everyday consumer products. 60 measured products + 19 category averages, with sources, confidence levels, and barcodes.

> "How much plastic is in my weekly shop?" — a question with no good public answer. This dataset is a start.

[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Contributors welcome](https://img.shields.io/badge/contributors-welcome-brightgreen)](CONTRIBUTING.md)

---

## What's in here

```
data/
├── products.csv      60 products with measured/estimated plastic weights
└── categories.csv    19 category averages (for items not yet in products)
docs/
└── METHODOLOGY.md    How weights are measured, confidence tiers, limitations
examples/
└── quickstart.py     Look up a receipt item in 20 lines of Python
```

## The schema, at a glance

Each row in `products.csv` is one product (one SKU, one size). The columns that matter most:

| Column | Meaning |
|---|---|
| `plastic_grams` | Weight of plastic packaging in grams |
| `confidence` | `measured` (weighed in-house), `category-avg` (fallback to category), or `inferred` (estimated from similar products) |
| `primary_material` | HDPE, PET, LDPE, PP, PVC, mixed, etc. |
| `source` | Where the number came from — must be a real, traceable reference |
| `barcode` | UPC-A or EAN-13, checksum-validated. Optional |
| `region` | Where this SKU is sold (`US`, `UK`, `EU`, `global`) |

Full schema in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## Using the data

```python
import csv

with open("data/products.csv") as f:
    products = list(csv.DictReader(f))

# Find all measured oat milks
oat_milks = [p for p in products
             if p["subcategory"] == "oat-milk" and p["confidence"] == "measured"]
for p in oat_milks:
    print(f"{p['name']}: {p['plastic_grams']}g {p['primary_material']}")
```

See [`examples/quickstart.py`](examples/quickstart.py) for a slightly bigger example that handles a full receipt.

## What this dataset is — and is not

**It is:**
- A starting point for plastic packaging research, sustainability tooling, and consumer apps
- Honest about uncertainty — every row carries a confidence tier
- Free for any use under [CC-BY-SA-4.0](LICENSE), including commercial, provided you attribute and share-alike

**It is not:**
- Comprehensive — 60 products is a seed, not a survey of the supermarket
- A substitute for primary measurement — `inferred` rows should be treated as ballpark estimates
- An LCA (life-cycle assessment) — we measure packaging, not full environmental impact
- An audited dataset — see [METHODOLOGY](docs/METHODOLOGY.md) for sources and limitations

## Contributing

Got a kitchen scale? You can help. Most useful contributions: weighing real packaging for products not yet in the database, especially outside the US.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the submission process. The short version: open an issue with the `new-product` template, or open a PR adding a row.

## Citation

If you use this dataset in research, please cite it. See [CITATION.cff](CITATION.cff), or use:

> Loop Plastic Data. (2026). *An open dataset of consumer packaging weights.*
> https://github.com/ikm365789/packaging-plastic-weights

## License

Data and documentation: [CC-BY-SA-4.0](LICENSE). You must attribute the source and share derivative datasets under the same licence.

## A note on origin

This dataset was originally built for [Loop](https://loop.app) — a receipt-tracking app that helps people see the plastic in their shopping. The dataset is published openly because plastic packaging data is a public good. Loop maintains it; anyone can use it; pull requests are welcome from any direction.
