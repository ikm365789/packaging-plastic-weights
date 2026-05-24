# Methodology

How the Loop plastic data is gathered, weighed, and labelled.

This is the document we'd want to be torn apart by a methodologist. Honesty about uncertainty is the whole point — a dataset that hides its weaknesses gets dismissed; one that surfaces them gets used.

---

## 1. What we measure

For each product (one SKU at one size), we record the **mass of plastic packaging in grams** required to bring that product home. This includes:

- The primary container (bottle, tub, pouch, film wrap)
- Plastic caps, lids, seals, and labels
- Inner liners in otherwise non-plastic packaging (e.g. the LDPE bag inside a cereal box)
- Plastic-coated paper packaging only the plastic portion

It does **not** include:
- Cardboard, glass, metal, or paper components (those are tracked separately if recorded at all)
- Transport packaging the consumer doesn't take home (shrink wrap on pallets, cardboard cases)
- Plastic in the product itself (e.g. microplastics in toothpaste — out of scope for now)

## 2. Confidence tiers

Every row is tagged with one of three confidence levels. **This is the single most important field for downstream users to respect.**

| Tier | What it means | When we use it |
|---|---|---|
| `measured` | Packaging weighed on a kitchen scale, recorded with date, source field cites the weighing | Whenever physically possible |
| `category-avg` | We don't have a specific weight, so we use the average for this category | Quick fallback for new products in a known category |
| `inferred` | Estimated from similar products in the database (same brand, same packaging type, different size) | When neither direct measurement nor category fallback fits |

Treat `measured` numbers as accurate to ±2g (scale precision). Treat `inferred` and `category-avg` as ballpark — useful for aggregates, not for individual product claims.

## 3. How a product gets weighed

The reproducible procedure for adding a `measured` row:

1. **Buy the product** (or use one already in the household). Empty and rinse.
2. **Separate components by material**. PET bottle, HDPE cap, PP label backing — each kept distinct.
3. **Dry thoroughly** (overnight on a rack). Wet plastic skews readings by several grams.
4. **Weigh on a tared kitchen scale**, precision 1g. Record total and per-component if helpful.
5. **Record the source** — date of weighing and who did it, e.g. `"Internal weighing 2025-11-14"`. Without this, the row is not `measured` — it's `inferred` at best.

For high-stakes products (large pack sizes, popular SKUs, controversial categories like cleaning products), we weigh **two of the same product** and use the average. This catches outliers from manufacturing variance.

## 4. Categories and category averages

`categories.csv` contains 19 product categories with a typical plastic weight per unit. These exist for two reasons:

- **Lookup fallback**: when a user scans an unknown receipt item, we can return a category-average estimate while marking it `category-avg`. Better than no answer.
- **Sanity check**: a new `measured` row that's 10x its category average is probably a typo or a different size.

Category averages were derived from the `measured` rows. As the dataset grows, these will improve.

## 5. The barcode field

When present, barcodes are **checksum-validated** UPC-A (12 digits) or EAN-13 (13 digits). A barcode that fails its checksum is rejected at ingest. See [`examples/quickstart.py`](../examples/quickstart.py) for validation code.

A row without a barcode is still useful — many supermarket own-brand and bulk items lack UPC codes. The barcode is the most reliable join key when it's there.

## 6. Sources

The `source` column is mandatory and must be a traceable reference. Acceptable sources:

- `Internal weighing YYYY-MM-DD` — measured by a contributor with date
- `Manufacturer LCA, [report name + year]` — published lifecycle assessment
- `Academic paper: [author + year + DOI]` — peer-reviewed study
- `Industry database: [name + accessed date]` — recognised packaging databases
- `Crowdsourced submission [id] from [contributor]` — added via the Loop submission system, after review

Sources that are NOT acceptable: marketing claims, vague "manufacturer says" without a citable document, AI-generated estimates without verification.

## 7. Known limitations

We're upfront about the things this dataset cannot do yet:

- **Geographic skew**: most rows are US-coded. UK and EU coverage is partial.
- **Size coverage**: we typically weigh one or two sizes per SKU, then infer the rest. The "infer" is reasonable but not measured.
- **Packaging redesigns**: when a brand changes packaging (Coca-Cola moves to 100% rPET, or Heinz removes a plastic seal), our row becomes stale until re-weighed. Updates are date-stamped but not automatic.
- **Multi-pack ambiguity**: a 12-pack of bottles has 12 caps and shrink-wrap. We try to capture the per-unit and the total — but inconsistencies exist.
- **Mixed materials**: a tube with an aluminium body and a plastic cap gets `primary_material: mixed`. We list the dominant material but don't always break out the proportions.
- **No LCA**: this dataset measures *mass*, not impact. 50g of recycled PET is not equivalent in environmental footprint to 50g of virgin HDPE. Users should not infer environmental impact from grams alone without an LCA framework on top.

## 8. Versioning and updates

The dataset is updated as contributions arrive. Major versions are tagged in the GitHub releases. The `updated_at` column on each row records when it was last reviewed; rows older than 24 months are flagged as needing reverification.

## 9. How to challenge a number

If you think a row is wrong, you have three options:

1. **Open an issue** with the `data-question` template. Include the row ID, what you think is wrong, and any evidence (a competing measurement, a manufacturer datasheet).
2. **Submit a PR** with the corrected row and an updated `source` field.
3. **Email** the maintainers (see repo About). For systematic issues across many rows.

Good-faith challenges are welcome. The dataset is stronger when wrong numbers are found and fixed than when nobody looks.

## 10. Schema reference

Full column list in `products.csv`:

| Column | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | Slug-style unique identifier |
| `name` | string | yes | Display name |
| `brand` | string | no | Manufacturer / brand |
| `category` | string | yes | One of the 19 from `categories.csv` |
| `subcategory` | string | no | Finer grouping within category |
| `size_value` | number | yes | Package size, in `size_unit` |
| `size_unit` | string | yes | `fl_oz`, `g`, `kg`, `ml`, `l`, `count`, etc. |
| `plastic_grams` | number | yes | Total plastic packaging mass |
| `primary_material` | string | yes | HDPE, PET, LDPE, PP, mixed, etc. |
| `confidence` | string | yes | `measured`, `category-avg`, `inferred` |
| `source` | string | yes | Traceable citation (see §6) |
| `barcode` | string | no | UPC-A or EAN-13, checksum-valid |
| `recyclable_pct` | number | no | Percent of packaging that's curbside-recyclable |
| `bioplastic_pct` | number | no | Percent that's bio-based |
| `keywords` | string | no | Comma-separated search terms |
| `aliases` | string | no | JSON array of alternate receipt-text spellings |
| `region` | string | yes | `US`, `UK`, `EU`, or `global` |
| `updated_at` | date | yes | YYYY-MM-DD of last review |
