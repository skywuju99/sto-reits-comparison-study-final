# Appendix A. Data Sources and Coverage

## A.1 Overview

This appendix documents the datasets used in the empirical analysis of RealT-based real estate tokens and listed REITs.

| Dataset | Main contents | Coverage | Main use |
|---|---|---|---|
| RealT asset-year data | Token address, asset information, rental yield, platform token price, investment amount | 2021–2026 | Rental-yield and platform-price analysis |
| Swapcat trades | Secondary-market executions involving RealTokens | 2020–2026 | Market-price and liquidity analysis |
| YAM OfferAccepted events | Secondary-market executions involving RealTokens | 2022–2026 | Market-price and liquidity analysis |
| RealToken Transfer events | Mint and burn events identified through zero-address transfers | 2021–2026 | Token-supply change analysis |
| FTSE EPRA Nareit Global Real Estate Index Series | Global, USD, Total Return | 2022–2025 | REIT benchmark |

## A.2 Main analysis period

The main comparative analysis uses complete calendar years from 2022 through 2025.

The year 2026 is excluded from the main annual-return comparison because it is incomplete and the STO and REIT observations do not share an identical cutoff date.

## A.3 Currency and timing conventions

- Monetary values are expressed in U.S. dollars where possible.
- Blockchain timestamps are converted to UTC.
- Token contract addresses are normalized to lowercase.
- REIT returns are annual total returns including distributions.
- Secondary-market year-end prices are estimated using trades executed during the final 90 days of each calendar year.

## A.4 Repository files

- `data/realt/realt_asset_year_source.xlsx`
- `data/secondary_market/`
- `data/mint_burn/`
- `data/reits/`
- `data/metadata/`
