# The Margin Trap — extended retail profitability analysis

This folder contains a revised local dashboard, not a live deployment. It preserves the original four charts and region controls, corrects unsupported descriptions, and adds six sections with actual calculations from the available aggregates.

## Findings

- Standardizing every region to the same 17-sub-category sales mix produces margins of West 14.77%, South 14.26%, East 12.38%, and Central 6.87%. Broad product mix alone does not explain Central's low margin.
- Central is 5.81 percentage points below the other regions combined. A reference-weight decomposition splits this into +1.04 points from product mix and -6.85 from within-sub-category margins.
- Binders, Appliances and Furnishings contribute -5.78 points to that within-sub-category component. This is an accounting attribution, not evidence of causal drivers.
- Fourteen negative sub-category–region groups sum to $36,971 in net losses, versus $22,387 across nationally negative sub-categories. Gains elsewhere offset $14,584 at national aggregation.
- Negative discount tiers contain 1,393 source records (13.9%) and $135,376 of net losses, offsetting 32.1% of the $421,773 earned by the other tiers.
- The business action is to audit targeted product–region combinations and test a specific discount policy against current practice, rather than assume all heavy discounts or all transactions in a loss category destroy value.

## Source and limits

The input is the `DATA` object embedded in:
https://takizawadaiki.github.io/retail-profitability-analysis/
Retrieved September 16, 2026. The public repository's main-branch tree contained only `index.html`. The linked `analysis_queries.sql` returned HTTP 404. Original transaction records, data provenance, dates and SQL were not available.

The extension therefore uses only published, rounded aggregates. It does not substitute a similarly named Superstore dataset from elsewhere, claim to validate raw records, estimate demand elasticity, or infer transaction-level causal effects. Counts are labeled source records because distinct orders and line items cannot be distinguished. Profit is the dataset field, whose cost coverage is unknown. The original “real retail orders” description is not independently supported.

The source labels `21-40%` and `40%+` overlap at 40%. They are preserved as source labels rather than silently redefining missing SQL boundaries. Average-discount weighting is also unverified.

## Reproduce the numerical results

Python 3.9+ standard library only:

```sh
python3 reanalysis.py
```

The script reads `aggregate-data.json` and writes `analysis-results.json`. It asserts that every region has the same 17 sub-categories and that the decomposition sums to the observed margin gap. Reconciliation results show discrepancies of at most $2 between each dimension's sum and its region KPI, consistent with displayed-dollar rounding.

### Standardization

For sub-category k, w[k] = total sales across the four regions in k / total sales across all regional cells. For each region r, m[r,k] = profit[r,k] / sales[r,k]. Common-mix margin = sum(w[k] * m[r,k]). Observed margin uses summed sub-category profit / summed sub-category sales. All weights derive from regional cells, so these comparisons are internally consistent.

This is a descriptive reweighting holding observed margins fixed. It does not estimate a feasible assortment change. Differences within broad categories remain uncontrolled.

### Decomposition

Reference O pools West, East and South; comparison C is Central. Define each region group's sales share w and margin m for each sub-category.

- Mix = sum((wC - wO) * mO)
- Within = sum(wC * (mC - mO))
- Total = Central margin - other-region margin

The allocation depends on the selected reference. These are accounting components, not causal effects. `benchmark_gap_dollars` in the JSON is the arithmetic difference at other-region margins holding Central sales fixed; it is not recoverable profit or a forecast.

### Loss pool and scenario

Sum the absolute negative profits of sub-category–region groups, excluding positive groups. This is a net group loss pool; individual losing transactions may be offset within a group. The same transactions contribute to product, region and discount summaries, so losses across views must not be added together.

The interactive scenario assumes a selected fraction of this pool is eliminated, then subtracts an entered incremental cost. It does not predict recovery. Sales, cross-selling and underlying costs are held unchanged by construction; actual outcomes can fall outside the scenario. Default assumptions are 25% recovery and $5,000 intervention cost, chosen only for illustration.

## Next layer requires raw data

Please provide the original transaction file or notebook, with its source, coverage dates, unique order and line IDs, product IDs, region, customer segment, quantity, discount, sales, profit, return handling and cost definitions. This enables:

1. Validation of counts, duplicates, totals, boundaries and dates.
2. Within-product discount comparisons with time/region controls and explicit overlap checks.
3. Concentration of losses by individual product/customer/order and seasonality.
4. A prospective pilot using incremental contribution profit per eligible customer/store, including non-purchases and returns, rather than margin among buyers alone.

Conditional observational comparisons remain vulnerable to selective discounting. A randomized pilot is proposed, not performed.

## Preview and publication

Open `index.html` or serve the folder with `python3 -m http.server 8766`. Chart.js 4.4.0 is local with its license header preserved; web fonts require connectivity and have system fallbacks.

Upload the files inside this folder to the root of the **retail-profitability-analysis** repository. This is a different repository from the main portfolio. Replace that repository's `index.html`; do not overwrite the main portfolio's `index.html`. No deployment has been performed by this task.
