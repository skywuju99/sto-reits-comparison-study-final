> **과거 버전 보존자료 / Historical version.** 최신 논문 재현은 저장소 최상위 README와 `replication/empirical-20261023-v1/`을 사용하십시오. 이 문서의 “final/current”는 당시 버전을 뜻합니다.

# Appendix C. Integration of YAM and Swapcat Trades

## C.1 Market Treatment

YAM and Swapcat are treated as two secondary-market venues in which the same RealToken assets have been traded.

The relevant contracts are:

- Swapcat: `0xB18713Ac02Fc2090c0447e539524a5c76f327a3b`
- YAM: `0xc759aa7f9dd9720a1502c104dae4f9852bb17c14`

Trades from both venues are integrated using normalized RealToken contract addresses. YAM and Swapcat are therefore not treated as separate STO products.

No inferred cross-address migration mapping is applied when different token contract addresses cannot be linked through an authoritative migration record.

## C.2 Standardization

The processing procedure applies the following standardization steps:

1. convert RealToken and payment-token contract addresses to lowercase;
2. use blockchain block timestamps and standardize timestamps to UTC;
3. apply RealToken and payment-token decimal specifications;
4. calculate economic RealToken quantity and payment amount from raw on-chain values;
5. calculate the transaction price per RealToken;
6. calculate transaction value in USD for eligible USD-linked payment transactions;
7. identify the source venue as YAM or Swapcat;
8. include both RealToken-sold and RealToken-bought transaction directions after normalization; and
9. remove duplicate records using transaction hash and log index where applicable.

## C.3 Asset Matching and Final U.S. Residential Classification

The integrated trade universe is matched to asset metadata using normalized RealToken contract addresses.

The source asset-matching file may contain multiple rows for the same normalized token address. For each address:

1. `source_true` is set to `TRUE` if at least one source row has `is_us_residential=TRUE`;
2. all available asset names for that address are considered;
3. a U.S. state or District of Columbia code must be identifiable in the available asset name; and
4. instruments or foreign assets matching the exclusion criteria are removed.

Addresses with `source_true=FALSE` are not added to the U.S. residential sample solely because their names contain a U.S. state or District of Columbia code.

Final inclusion therefore requires:

`source_true = TRUE`

**AND**

a U.S. state or District of Columbia code match

**AND**

no exclusion criterion matched.

This procedure produces a final address-level U.S. residential classification universe of **404 unique RealToken contract addresses**.

The relevant metadata files are:

- `data/metadata/asset_master_match.csv`
- `data/metadata/asset_master_clean.csv`

The 404-address classification universe is distinct from year-specific trading and return samples, which can be smaller after transaction-value, year-end VWAP, and adjacent-period matching requirements are applied.

## C.4 Payment-Token Treatment

The primary USD-denominated sample uses directly identifiable USD-linked payment tokens.

The principal decimal specifications applied in the processing procedure include:

- USDC: 6 decimals
- WXDAI: 18 decimals
- legacy USDC representation: 18 decimals
- USDT: 6 decimals

Raw blockchain amounts are divided by the corresponding decimal factor before transaction quantities, payment amounts, prices, and USD trade values are calculated.

RealToken-to-RealToken swaps and transactions involving unidentified or non-direct payment assets are excluded from the primary USD-denominated sample unless a defensible USD value can be established.

A broader USD-like payment-token specification is examined separately as a robustness check.

The validated payment-token decimal metadata are documented in:

`data/metadata/payment_token_decimals.csv`

## C.5 Trade Filters

The primary analysis applies a minimum transaction-value threshold of:

`USD 1`

Transactions with a calculated USD trade value below USD 1 are excluded from the primary sample.

A higher minimum transaction-value threshold of:

`USD 5`

is used as a robustness check.

Malformed, invalid-decimal, duplicate, or non-economic transaction records are excluded from the relevant analytical sample.

## C.6 2026 Source-Coverage Alignment

The final observed transaction timestamps differ between the two secondary markets:

- Swapcat: July 6, 2026 20:28:20 UTC
- YAM: August 3, 2026 20:09:20 UTC

For the combined 2026 analysis, both markets are restricted to the common source-coverage cutoff:

`July 6, 2026 20:28:20 UTC`

A total of 1,502 YAM observations occurring after this common cutoff are excluded from the combined 2026 analysis.

The 2026 results are used only as supplementary partial-year evidence.

## C.7 Output Files

The principal integration and return-analysis outputs include:

- `data/secondary_market/platform_year_summary_us_residential.csv`
- `data/secondary_market/asset_year_price_summary_us_residential.csv`
- `data/secondary_market/common_asset_return_detail_us_residential.csv`
- `data/secondary_market/common_asset_returns_us_residential.csv`
- `data/secondary_market/common_asset_returns_robustness.csv`
- `data/secondary_market/annual_sample_diagnostics_us_residential.csv`
- `data/secondary_market/annual_sample_diagnostics_all_variants.csv`

The main integrated analysis is reproduced using:

`code/recalculate_yam_swapcat.py`

The current files in `data/secondary_market/` correspond to the final 404-address U.S. residential classification procedure.
