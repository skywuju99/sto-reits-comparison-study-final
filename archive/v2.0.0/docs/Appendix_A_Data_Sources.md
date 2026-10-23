> **과거 버전 보존자료 / Historical version.** 최신 논문 재현은 저장소 최상위 README와 `replication/empirical-20261023-v1/`을 사용하십시오. 이 문서의 “final/current”는 당시 버전을 뜻합니다.

# Appendix A. Data Sources and Coverage

## A.1 Overview

This appendix documents the datasets used in the empirical analysis of RealT-based real estate tokens and listed REITs.

| Dataset | Main contents | Coverage | Main use |
|---|---|---|---|
| RealT tokenHistory asset-year data | Token address, asset information, rental yield, platform tokenPrice, investment amount | 2021–2026 | Rental-yield and supplementary platform-price analysis |
| Swapcat trades | Secondary-market executions involving RealTokens | 2020–2026 | Market-price and liquidity analysis |
| YAM OfferAccepted events | Secondary-market executions involving RealTokens | 2022–2026 | Market-price and liquidity analysis |
| RealToken asset-classification metadata | Address matching, source classification flag, final U.S. residential classification | Integrated trade-source universe | Address-level sample construction |
| RealToken Transfer events | Mint and burn events identified through zero-address transfers | 2021–2026 | Token-supply change analysis |
| FTSE Nareit U.S. Real Estate Index Series - Residential | U.S. Residential, U.S. Dollars, Annual Total Return | 2022–2025 | Primary REIT benchmark |
| FTSE EPRA Nareit Global Real Estate Index Series | Global, USD, Total Return | 2022–2025 | Supplementary REIT benchmark |

## A.2 Main Analysis Period

The main comparative analysis uses complete calendar years from 2022 through 2025.

The year 2026 is excluded from the main annual-return comparison because it is incomplete and does not represent a complete calendar-year observation comparable with the 2022–2025 annual REIT-return series. The 2026 STO data are used only for supplementary partial-year analysis.

## A.3 Source Snapshots and Coverage

The RealT tokenHistory source data were retrieved from:

`https://api.realtoken.community/v1/tokenHistory`

The research snapshot used in the thesis was archived on April 6, 2026 (KST, UTC+9). The platform-displayed tokenPrice used in the supplementary price-level comparison is taken from the same snapshot.

Swapcat and YAM transaction records are verified using Gnosis Chain data.

- Gnosis Chain RPC: `https://rpc.gnosischain.com`
- Swapcat contract: `0xB18713Ac02Fc2090c0447e539524a5c76f327a3b`
- YAM contract: `0xc759aa7f9dd9720a1502c104dae4f9852bb17c14`
- Final observed Swapcat timestamp: July 6, 2026 20:28:20 UTC
- Final observed YAM timestamp: August 3, 2026 20:09:20 UTC
- Common 2026 source-coverage cutoff: July 6, 2026 20:28:20 UTC
- YAM observations after the common cutoff excluded from the combined 2026 analysis: 1,502

For the combined 2026 analysis, both YAM and Swapcat are therefore restricted to the common source-coverage cutoff above.

Large raw YAM and Swapcat transaction files are not stored directly in the main repository. The raw source archive and the final processed replication archive are distributed through GitHub Release v2.0.0:

`secondary_market_raw_sources_v2.0.zip`

`secondary_market_processed_results_v2.0.zip`

The processed archive corresponds to the final **404-address U.S. residential classification**.

Current processed CSV outputs corresponding to the same final classification are also maintained in:

`data/secondary_market/`

## A.4 Asset Classification Coverage

The integrated asset-matching source contains 783 unique normalized RealToken contract addresses.

The final U.S. residential classification is constructed at the address level using the following logic:

1. `source_true=TRUE` when at least one source row for the normalized address has `is_us_residential=TRUE`;
2. the available asset name contains a U.S. state or District of Columbia code; and
3. the address is not identified as an excluded instrument or foreign asset.

Addresses with `source_true=FALSE` are not added to the U.S. residential sample solely because their names contain a U.S. state or District of Columbia code.

This procedure produces a final U.S. residential classification universe of **404 unique RealToken contract addresses**.

The relevant files are:

- `data/metadata/asset_master_match.csv`
- `data/metadata/asset_master_clean.csv`
- `data/metadata/raw_validation_report.csv`

The 404-address classification universe is distinct from year-specific transaction and return samples, which may be smaller because valid transactions, transaction-value thresholds, year-end 90-day VWAPs, and adjacent-period price observations are additionally required.

## A.5 Currency and Timing Conventions

- Monetary values are expressed in U.S. dollars where possible.
- Blockchain timestamps are standardized to UTC.
- Token contract addresses are normalized to lowercase.
- REIT returns are annual total returns including distributions.
- Secondary-market year-end prices are estimated using transaction-quantity-weighted VWAPs over the final 90 calendar days of each period.
- The primary secondary-market transaction filter uses directly identified USD-linked payment tokens and a minimum calculated trade value of USD 1.
- A USD 5 minimum and a broader USD-like payment-token specification are used as robustness variants.

## A.6 Repository Files

- `data/realt/realt_asset_year_source.xlsx`
- `data/secondary_market/`
- `data/mint_burn/`
- `data/reits/`
- `data/metadata/`
- `logs/data_snapshot_log.csv`

Additional source and variable documentation is provided in:

- `data/metadata/source_list.csv`
- `data/metadata/data_dictionary.csv`
