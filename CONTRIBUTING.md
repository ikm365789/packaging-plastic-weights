# Contributing to Packaging Plastic Weights

The dataset gets more useful with every contribution. There are three ways to help, listed easiest to most involved.

## 1. Report a wrong number (5 minutes)

If you think a row is incorrect, open an issue with the `data-question` template. Useful information:

- The row `id` (e.g. `oat-milk-oatly-64oz`)
- What you think is wrong
- Evidence — a measurement you took, a manufacturer datasheet, a published study

We treat data challenges as gifts. No defensiveness; if the number is wrong, we fix it.

## 2. Add a new product (15 minutes per product)

The most useful contribution. You need a kitchen scale (precision 1g) and a product not yet in the database.

### What we accept

- **Real packaging** — buy the product, use it, weigh the packaging. Or weigh what you already have.
- **Honest sources** — your weighing counts. A manufacturer's published LCA counts. A peer-reviewed paper counts. A guess doesn't.
- **Any region** — we're skewed US right now and especially want UK / EU / rest-of-world.

### The process

**Option A — open an issue** with the `new-product` template. We'll handle the data entry. Best if you're not comfortable with Git.

**Option B — open a pull request** with the new row. Best if you're going to add several.

Either way, follow the methodology in [docs/METHODOLOGY.md](docs/METHODOLOGY.md) — especially the weighing procedure and source requirements.

### What gets rejected

- AI-generated estimates without a real measurement underneath
- "About X grams" without a procedure
- Rows missing required fields (see schema in METHODOLOGY)
- Barcodes that fail UPC-A or EAN-13 checksum validation
- Sources that are marketing claims rather than traceable references

We're not trying to be hostile — we're trying to keep the dataset citable. A dataset that accepts unverified entries stops being trusted.

## 3. Improve the methodology or tooling (any time)

Things outside the data itself that are welcome:

- Spotting limitations we haven't documented
- Adding example code in other languages (we have Python; R / JS / Go welcome)
- Suggesting better category schemes
- Building lookup or visualisation tools that consume the dataset

Open an issue first to discuss bigger changes before writing code.

## Pull request etiquette

- One product per PR keeps reviews quick. If adding several, group by category in one PR rather than one giant batch.
- Commit message: `add: [product name] (measured / inferred)` — the confidence tier helps the reviewer.
- Don't reformat the CSV — keep diffs small.
- If you're updating an existing row, explain what changed in the PR body.

## A note on attribution

This dataset is CC-BY-SA-4.0. By contributing, you agree your contribution is also released under that licence. Contributors are listed in the GitHub commit history; if you'd like to be credited differently in the dataset itself (e.g. as the `source` on rows you measured), say so in your PR.

## Questions

Open a discussion in the repo's Discussions tab, or comment on an existing issue.
