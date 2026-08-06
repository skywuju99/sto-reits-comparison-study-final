# Appendix F. REIT Benchmarks

## F.1 Primary benchmark

The primary REIT benchmark is:

- Index series: FTSE Nareit U.S. Real Estate Index Series
- Property sector: Residential
- Currency: U.S. Dollars
- Return type: Annual Total Return
- Analysis period: 2022–2025
- Role: Primary comparison benchmark

The U.S. Residential sector is used as the primary benchmark because the RealT sample analyzed in this study consists of U.S. residential rental properties.

However, RealT and listed Residential REITs differ in portfolio structure, leverage, management, diversification, liquidity, and price formation. The comparison is therefore exploratory and does not represent a comparison of identical assets.

## F.2 Primary benchmark annual returns

| Year | U.S. Residential REIT total return |
|---|---:|
| 2022 | -31.34% |
| 2023 | +7.66% |
| 2024 | +12.83% |
| 2025 | -7.43% |

Repository file:

`data/reits/ftse_nareit_us_residential_total_return_2022_2025_final.csv`

Official source page:

`https://www.reit.com/data-research/reit-market-data/report/annual-index-values-returns`

Source workbook listed by Nareit:

`https://www.reit.com/sites/default/files/returns/AnnualSectorReturns.xlsx`

## F.3 Supplementary global benchmark

The supplementary benchmark is:

- Index series: FTSE EPRA Nareit Global Real Estate Index Series
- Geographic scope: Global
- Currency: USD
- Return type: Total Return
- Analysis period: 2022–2025
- Role: Supplementary global-market indicator

| Year | Global USD total return |
|---|---:|
| 2022 | -23.58% |
| 2023 | +9.78% |
| 2024 | +1.57% |
| 2025 | +11.04% |

Repository file:

`data/reits/ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv`

Official source:

`https://www.reit.com/sites/default/files/returns/GlobalReturns.pdf`

## F.4 Interpretation

The STO observed capital-return measure and the official REIT total-return measure do not have the same measurement scope.

The STO capital-return measure excludes rental distributions. The REIT total-return measure includes both price changes and distributions.

Their comparison is therefore used to examine differences in observed price adjustment and market structure, not to establish direct performance superiority.

The market-price-reflected composite-return proxy is also not identical to the official REIT total-return measure because it relies on annual platform net-rent data rather than reconstructed investor-level cash flows.

## F.5 ETF proxy data

ETF adjusted-price data for VNQ, VNQI, IYR, REZ, and RWR are not official FTSE Nareit index observations.

They are not used as the primary benchmark in the empirical analysis.

## F.6 Repository files

- `data/reits/ftse_nareit_us_residential_total_return_2022_2025_final.csv`
- `data/reits/ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv`
- `data/reits/README.md`
- `logs/reits_official_data_collection_log.txt`
- `results/thesis_tables/table_5_05_reit_benchmarks.csv`
