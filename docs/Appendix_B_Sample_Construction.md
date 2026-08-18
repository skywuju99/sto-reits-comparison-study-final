# Appendix B. Sample Construction

## B.1 Unit of Analysis

The empirical unit is a RealToken contract associated with a U.S. residential rental property.

YAM and Swapcat are treated as trading venues for the same underlying RealToken assets, rather than as separate STO products. Transactions from the two venues are integrated using normalized RealToken contract addresses.

## B.2 Inclusion Criteria

An observation is included in the primary sample when:

1. the token contract can be matched to a RealT asset;
2. the underlying asset is located in the United States;
3. the asset is classified as residential rental real estate;
4. a valid YAM or Swapcat secondary-market transaction can be identified;
5. the payment asset satisfies the direct USD-like payment-token criteria;
6. the transaction has a calculated USD trade value of at least USD 1;
7. a valid year-end 90-day VWAP can be calculated for the relevant year; and
8. the same normalized RealToken contract address is observed in both adjacent comparison periods for capital-return calculation.

## B.3 Exclusion Criteria

The following are excluded from the primary sample:

- payment tokens and stablecoins when they appear as the RealToken-side asset rather than as payment assets;
- governance and ecosystem tokens;
- loans, factoring products, receivable or revenue-participation products, and profit-sharing products;
- non-U.S. assets;
- non-residential assets;
- malformed, invalid-decimal, or non-economic transactions;
- transactions with a calculated trade value below USD 1;
- observations without valid token or payment-token decimal information;
- assets without sufficient year-end trading activity to calculate the required VWAP; and
- token contracts that cannot be matched using the same normalized contract address across adjacent comparison periods.

Token migrations or reissued contracts are not joined across different contract addresses unless an authoritative migration mapping is available. No inferred migration mapping is used in the primary analysis.

## B.4 Robustness Samples

The primary transaction-value threshold is USD 1.

Robustness checks include:

- a minimum transaction-value threshold of USD 5; and
- a broader USD-like payment-token specification.

These variants are reported separately from the primary sample.

## B.5 Sample Diagnostics

The repository provides annual diagnostics for the primary and robustness samples:

- `annual_sample_diagnostics_us_residential.csv`
- `annual_sample_diagnostics_all_variants.csv`
- `exclusion_report.csv`

These files document the number of assets and transactions retained or excluded during the main processing stages.
