> **과거 버전 보존자료 / Historical version.** 최신 논문 재현은 저장소 최상위 README와 `replication/empirical-20261023-v1/`을 사용하십시오. 이 문서의 “final/current”는 당시 버전을 뜻합니다.

# Appendix B. Sample Construction

## B.1 Unit of Analysis

The empirical unit is a normalized RealToken contract address associated with a U.S. residential rental property.

YAM and Swapcat are treated as trading venues for the same underlying RealToken assets, rather than as separate STO products. Transactions from the two venues are integrated using normalized RealToken contract addresses.

The address-level U.S. residential classification is constructed before year-specific trading and VWAP filters are applied.

## B.2 Address-Level U.S. Residential Classification

The asset-matching source is grouped by normalized RealToken contract address.

For each address:

1. `source_true` is set to `TRUE` when at least one source row has `is_us_residential=TRUE`;
2. available asset names are checked for a U.S. state or District of Columbia code;
3. instruments or foreign assets matching the exclusion criteria are removed; and
4. addresses with `source_true=FALSE` are not added to the U.S. residential sample solely because their names contain a U.S. state or District of Columbia code.

Final address-level inclusion therefore requires:

`source_true = TRUE`

**AND**

a U.S. state or District of Columbia code is confirmed in the available asset name

**AND**

no exclusion criterion is matched.

The final U.S. residential classification universe contains **404 unique RealToken contract addresses**.

The address-level classification is stored in:

- `data/metadata/asset_master_match.csv`
- `data/metadata/asset_master_clean.csv`

The `classification_reason` field in `asset_master_clean.csv` uses the following values:

- `us_state_in_name`
- `source_flag_false`
- `excluded_instrument_or_foreign`
- `no_us_state_match`

## B.3 Primary Transaction and Return-Sample Inclusion Criteria

After address-level classification, an observation is included in the primary secondary-market sample when:

1. the normalized RealToken contract address is included in the final U.S. residential classification;
2. a valid YAM or Swapcat secondary-market transaction can be identified;
3. the payment asset satisfies the direct USD-like payment-token criteria;
4. token and payment-token decimals can be validly normalized;
5. the transaction has a calculated USD trade value of at least USD 1;
6. a valid year-end 90-day VWAP can be calculated for the relevant period; and
7. for capital-return calculation, the same normalized RealToken contract address has valid year-end 90-day VWAP observations in both adjacent comparison periods.

The 404-address classification universe is therefore larger than the year-specific return samples because trading activity, transaction-value filters, and year-end VWAP availability are additionally required.

## B.4 Exclusion Criteria

The following are excluded from the primary sample where applicable:

- addresses not included in the final U.S. residential classification;
- payment tokens and stablecoins when they appear as the RealToken-side asset rather than as payment assets;
- governance and ecosystem tokens;
- loans and factoring products;
- receivable, revenue-participation, and profit-sharing products;
- non-U.S. or other foreign assets;
- non-residential assets;
- malformed, invalid-decimal, or non-economic transactions;
- transactions with a calculated trade value below USD 1;
- observations without valid token or payment-token decimal information;
- assets without a calculable year-end 90-day VWAP; and
- token contracts that do not have valid year-end 90-day VWAP observations in both adjacent comparison periods when capital returns are calculated.

Token migrations or reissued contracts are not joined across different contract addresses unless an authoritative migration mapping is available. No inferred migration mapping is used in the primary analysis.

## B.5 Robustness Samples

The primary transaction-value threshold is USD 1.

Robustness checks include:

- a minimum transaction-value threshold of USD 5; and
- a broader USD-like payment-token specification.

These variants are reported separately from the primary sample.

## B.6 Sample Diagnostics

The repository provides annual diagnostics for the primary and robustness samples:

- `data/secondary_market/annual_sample_diagnostics_us_residential.csv`
- `data/secondary_market/annual_sample_diagnostics_all_variants.csv`
- `data/secondary_market/common_asset_returns_robustness.csv`

These files document the number of assets and transactions retained under the main and robustness specifications, including year-specific common-asset counts used for return calculation.

Additional classification documentation is provided in:

- `data/metadata/asset_master_clean.csv`
- `data/metadata/raw_validation_report.csv`
- `data/metadata/data_dictionary.csv`
