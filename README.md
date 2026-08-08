# Real Estate STO and REITs Comparison Study

Replication materials for the master's thesis:

**“A Comparative Study of Real Estate STOs and REITs: Structural Differences, Return and Risk Characteristics, and Investor Protection Frameworks”**

This repository provides data documentation, processed research outputs, analysis code, validation materials, and reproducibility notes used in the thesis.

The empirical analysis focuses on U.S. residential RealTokens issued through the RealT platform and integrates transaction data from two secondary markets, YAM and Swapcat.

---

## 1. Study Scope

- Main analysis period: 2022–2025 complete calendar years
- STO sample: U.S. residential rental RealTokens
- Secondary markets: YAM and Swapcat
- Primary REIT benchmark: FTSE Nareit U.S. Real Estate Index Series, Residential sector
- Supplementary REIT benchmark: FTSE EPRA Nareit Global Real Estate Index Series, Global USD Total Return
- 2026 data: used only for partial-year supplementary analysis and not directly compared with complete-year REIT returns

YAM and Swapcat are treated as two secondary markets for the same RealToken assets rather than as separate STO products. Transactions are integrated using RealToken contract addresses.

---

## 2. Main Data Sources

### 2.1 RealT Asset Data

Path:

`data/realt/realt_asset_year_source.xlsx`

Main variables include:

- RealToken contract address
- Asset name and token symbol
- Annual total investment value
- Annual net rent
- Annual rental-yield proxy
- RealT platform-displayed tokenPrice
- Asset type and observation information

RealT rental yields are platform-provided annual indicators and do not reconstruct the actual cash distributions received by individual investors.

### 2.2 YAM and Swapcat Secondary-Market Data

Path:

`data/secondary_market/`

Main outputs include:

- Annual transaction counts and trading values
- Asset-year transaction prices
- 30-day, 60-day, and 90-day year-end VWAPs
- Common-asset capital-return estimates
- Equal-weighted, median, and trade-value-weighted results
- Minimum-trade-value and outlier robustness checks
- Sample diagnostics and exclusion results

Large raw and processed transaction-level datasets are provided separately through GitHub Release v2.0.0.

### 2.3 Mint and Burn Data

Path:

`data/mint_burn/`

Mint and burn events are identified using ERC-20 Transfer events involving the zero address.

- Zero address → regular address: mint
- Regular address → zero address: burn

Burn events alone do not identify the economic reason for token disappearance, including asset sale, redemption, liquidation, migration, or technical restructuring.

### 2.4 REIT Benchmark Documentation

Path:

`data/reits/README.md`

#### Primary Benchmark

- Index series: FTSE Nareit U.S. Real Estate Index Series
- Property sector: Residential
- Currency: U.S. Dollars
- Return type: Annual Total Return
- Period used: 2022–2025
- Role: Primary benchmark
- Source document: Annual Returns by Property Sector and Subsector

#### Supplementary Benchmark

- Index series: FTSE EPRA Nareit Global Real Estate Index Series
- Geographic scope: Global
- Currency: USD
- Return type: Total Return
- Period used: 2022–2025
- Role: Supplementary benchmark

The underlying FTSE/Nareit index data and machine-readable reproductions are not redistributed in this repository due to licensing and redistribution restrictions.

Researchers should obtain the underlying index data directly from the official Nareit/FTSE source.

---

## 3. Sample Construction

The main secondary-market sample includes RealTokens satisfying the following conditions:

1. A valid link between the RealT asset and token contract address is available.
2. The underlying property is located in the United States.
3. The asset is a residential rental property.
4. A valid YAM or Swapcat transaction is observed.
5. A year-end 90-day VWAP can be calculated.
6. The same token contract is observed in adjacent comparison periods.

The following are excluded from the main sample:

- Payment tokens and stablecoins
- Governance or ecosystem tokens
- Lending products
- Receivable or revenue-participation products
- Non-U.S. assets
- Non-residential assets
- Invalid-decimal or non-economic transactions
- Assets without sufficient year-end price observations

Detailed sample criteria are documented in:

`docs/Appendix_B_Sample_Construction.md`

---

## 4. Return Measures

### 4.1 Year-End Market Price

The primary year-end market price is the transaction-quantity-weighted average price over the final 90 days of each year.

### 4.2 Secondary-Market Capital Return

Capital returns are calculated only for assets with valid year-end VWAP observations in two adjacent periods.

Results are reported using:

- Equal weighting
- Median return
- Trade-value weighting

### 4.3 Market-Price-Reflected Composite-Return Proxy

For assets for which both rental information and secondary-market prices are available, the study combines the rental-yield proxy with the observed secondary-market capital return.

This measure is referred to as a **market-price-reflected composite-return proxy**.

It is not an exact holding-period total return because actual investor-level distribution timing and complete cash-flow histories are not reconstructed.

---

## 5. Repository Structure

```text
sto-reits-comparison-study-final/
├── README.md
├── code/
│   └── recalculate_yam_swapcat.py
├── data/
│   ├── metadata/
│   ├── mint_burn/
│   ├── realt/
│   ├── reits/
│   │   └── README.md
│   └── secondary_market/
├── docs/
├── logs/
├── results/
├── requirements.txt
└── .gitignore
