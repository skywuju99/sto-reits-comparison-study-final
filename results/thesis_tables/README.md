# Thesis Table Replication Outputs

These CSV files reproduce selected values reported in the thesis tables and supplementary empirical outputs.

## Scope and Classification

The secondary-market outputs use the final U.S. residential classification defined in `data/metadata/asset_master_clean.csv`.

The address-level classification universe contains **404 unique RealToken contract addresses**. This is a classification universe before year-specific transaction filters, year-end 90-day VWAP availability, and adjacent-period matching are applied. Accordingly, the sample size reported in each table may be smaller than 404.

## Important Limitations

- Table 5-3 and Table 5-4 use RealT platform annual data and exploratory proxy measures. They are not affected by the final secondary-market address-classification adjustment.
- Table 5-8 reports annual YAM–Swapcat secondary-market sample diagnostics after application of the final U.S. residential classification and transaction filters.
- Table 5-9 reports observed secondary-market capital returns based on year-end 90-day VWAPs for common RealToken assets. Under the final classification, the 2024–2025 common-asset sample contains 382 assets.
- Table 5-10 combines platform annual-net-rent-based rental-yield proxies with observed secondary-market capital-return components for assets satisfying both rental-data and secondary-market matching requirements. This measure is an exploratory composite-return proxy and is not an exact investor-level holding-period total return.
- Under the final classification, the 2025 Table 5-10 merged sample contains 243 assets, with a rental-yield proxy of approximately 10.48%, a capital-return component of approximately -15.80%, and a composite-return proxy of approximately -5.32%.
- Table 5-11 is a non-contemporaneous supplementary price-level comparison using the RealT platform-displayed `tokenPrice` contained in the RealT tokenHistory research snapshot archived on April 6, 2026 (KST, UTC+9).
- The secondary-market comparison price in Table 5-11 is based on the recent 90-day transaction VWAP through the common 2026 source-coverage cutoff of July 6, 2026 20:28:20 UTC.
- Under the final classification, the 2026 Table 5-11 comparison contains 283 assets. The displayed relative difference is approximately -72.5% when rounded to one decimal place.
- Year-specific samples in Table 5-11 differ. Relative differences across years must not be interpreted as a continuous same-asset pricing-gap series, contemporaneous pricing gaps, or investment returns.
- The 2026 common-asset supplementary output compares the 2025 year-end 90-day VWAP with the recent 2026 90-day VWAP for matched assets and is separate from the Table 5-11 platform-price comparison.
- Under the final classification, this 2026 common-asset sample contains 283 matched assets, all of which show a decline. The trade-value-weighted change is approximately -71.28%.
- `table_5_12_monthly_price_key_points.csv` contains selected monthly descriptive price-level points rather than a complete monthly transaction panel or a fixed-portfolio return series.
- Table 5-13 reports robustness results using alternative outlier treatments, weighting methods, and transaction-value thresholds. The primary 2024–2025 equal-weighted sample contains 382 assets, while the USD 5 minimum-trade-value robustness sample contains 381 assets.
- Table 5-7 is not included because the exact variable name and unit reported in Smith and Baur (2025) were not independently reproduced in the repository source data.

The 2026 results are supplementary partial-year analyses and are not interpreted as completed annual returns.

## Files

- `table_5_03_platform_composite_return_proxy.csv`
- `table_5_04_platform_capital_return_sample.csv`
- `table_5_08_secondary_market_summary.csv`
- `table_5_09_secondary_market_capital_returns.csv`
- `table_5_10_market_price_composite_return_proxy.csv`
- `table_5_11_platform_price_level_comparison.csv`
- `supplement_2026_common_asset_returns.csv`
- `table_5_12_monthly_price_key_points.csv`
- `table_5_13_robustness.csv`
