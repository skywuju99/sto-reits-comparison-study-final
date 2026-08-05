# Appendix B. Sample Construction

## B.1 Unit of analysis

The empirical unit is a RealToken contract associated with a U.S. residential rental property.

YAM and Swapcat are treated as trading venues for the same underlying RealToken assets, rather than as separate STO products.

## B.2 Inclusion criteria

An observation is included in the main sample when:

1. the token can be matched to a RealT asset;
2. the underlying asset is located in the United States;
3. the asset is classified as residential rental real estate;
4. valid secondary-market trades can be identified;
5. a year-end 90-day VWAP can be calculated for the relevant year; and
6. the same token address can be matched across adjacent years for capital-return calculation.

## B.3 Exclusion criteria

The following are excluded from the main sample:

- payment tokens and stablecoins;
- governance and ecosystem tokens;
- loans, factoring products, and profit-sharing products;
- non-U.S. assets;
- non-residential assets;
- malformed or non-economic trades;
- observations without valid token or payment-token decimals;
- assets without sufficient year-end trading activity; and
- address pairs that cannot be verified as the same asset across adjacent years.

## B.4 Sample diagnostics

The repository provides annual diagnostics for the primary and robustness samples:

- `annual_sample_diagnostics_us_residential.csv`
- `annual_sample_diagnostics_all_variants.csv`
- `exclusion_report.csv`

These files document the number of assets retained or excluded at each processing stage.
