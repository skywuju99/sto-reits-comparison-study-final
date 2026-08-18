# Appendix A. Data Sources and Coverage

## A.1 Overview

This appendix documents the datasets used in the empirical analysis of RealT-based real estate tokens and listed REITs.

| Dataset | Main contents | Coverage | Main use |
|---|---|---|---|
| RealT tokenHistory asset-year data | Token address, asset information, rental yield, platform tokenPrice, investment amount | 2021–2026 | Rental-yield and supplementary platform-price analysis |
| Swapcat trades | Secondary-market executions involving RealTokens | 2020–2026 | Market-price and liquidity analysis |
| YAM OfferAccepted events | Secondary-market executions involving RealTokens | 2022–2026 | Market-price and liquidity analysis |
| RealToken Transfer events | Mint and burn events identified through zero-address transfers | 2021–2026 | Token-supply change analysis |
| FTSE Nareit U.S. Real Estate Index Series - Residential | U.S. Residential, U.S. Dollars, Annual Total Return | 2022–2025 | Primary REIT benchmark |
| FTSE EPRA Nareit Global Real Estate Index Series | Global, USD, Total Return | 2022–2025 | Supplementary REIT benchmark |

## A.2 Main Analysis Period

The main comparative analysis uses complete calendar years from 2022 through 2025.

The year 2026 is excluded from the main annual-return comparison because it is incomplete and the STO and REIT observations do not share an identical cutoff date. The 2026 data are used only for supplementary partial-year analysis.

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

For the combined 2026 analysis, YAM observations after the common cutoff are excluded.

## A.4 Currency and Timing Conventions

- Monetary values are expressed in U.S. dollars where possible.
- Blockchain timestamps are standardized to UTC.
- Token contract addresses are normalized to lowercase.
- REIT returns are annual total returns including distributions.
- Secondary-market year-end prices are estimated using transaction-quantity-weighted VWAPs over the final 90 calendar days of each year.

## A.5 Repository Files

- `data/realt/realt_asset_year_source.xlsx`
- `data/secondary_market/`
- `data/mint_burn/`
- `data/reits/`
- `data/metadata/`
- `logs/data_snapshot_log.csv`
