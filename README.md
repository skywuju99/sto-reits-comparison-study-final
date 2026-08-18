# Real Estate STO and REITs Comparison Study

Replication materials for the master's thesis:

**“A Comparative Study on Return–Risk Characteristics and Investor Protection Systems of Real Estate STOs and REITs”**

This repository provides data documentation, processed research outputs, analysis code, validation materials, and reproducibility notes used in the thesis.

The empirical analysis focuses on U.S. residential RealTokens issued through the RealT platform and integrates transaction data from two secondary markets, YAM and Swapcat.

---

## 1. Study Scope

- Main analysis period: 2022–2025 complete calendar years
- STO sample: U.S. residential rental RealTokens
- Final U.S. residential classification universe: 404 unique RealToken contract addresses
- Secondary markets: YAM and Swapcat
- Primary REIT benchmark: FTSE Nareit U.S. Real Estate Index Series, Residential sector
- Supplementary REIT benchmark: FTSE EPRA Nareit Global Real Estate Index Series, Global USD Total Return
- 2026 data: used only for partial-year supplementary analysis and not directly compared with complete-year REIT returns

The 404-address classification universe is the final address-level U.S. residential classification before year-specific trading-activity and year-end VWAP availability filters are applied.

YAM and Swapcat are treated as two secondary markets for the same RealToken assets rather than as separate STO products. Transactions are integrated using RealToken contract addresses.

---

## 2. Main Data Sources

### 2.1 RealT Asset Data

Path:

`data/realt/realt_asset_year_source.xlsx`

Source:

`https://api.realtoken.community/v1/tokenHistory`

Snapshot:

The RealT tokenHistory source data used in the thesis were retrieved and archived as a research snapshot on April 6, 2026 (KST, UTC+9).

Main variables include:

- RealToken contract address
- Asset name and token symbol
- Annual total investment value
- Annual net rent
- Annual rental-yield proxy
- RealT platform-displayed tokenPrice
- Asset type and observation information

The platform-displayed tokenPrice used in the supplementary price-level comparison is taken from the same RealT research snapshot archived on April 6, 2026.

RealT rental yields are platform-provided annual indicators and do not reconstruct the actual cash distributions received by individual investors.

### 2.2 YAM and Swapcat Secondary-Market Data

Path:

`data/secondary_market/`

Contracts:

- Swapcat: `0xB18713Ac02Fc2090c0447e539524a5c76f327a3b`
- YAM: `0xc759aa7f9dd9720a1502c104dae4f9852bb17c14`

Verification source:

- Gnosis Chain RPC: `https://rpc.gnosischain.com`

Main outputs include:

- Annual transaction counts and trading values
- Asset-year transaction prices
- 30-day, 60-day, and 90-day year-end VWAPs
- Common-asset capital-return estimates
- Equal-weighted, median, and trade-value-weighted results
- Minimum-trade-value and outlier robustness checks
- Sample diagnostics and robustness results

Large raw transaction-level source files are provided separately through GitHub Release v2.0.0.

The final processed replication archive corresponding to the **404-address U.S. residential classification** is provided through GitHub Release v2.0.1:

`secondary_market_processed_results_v2.0.1.zip`

The processed archive in Release v2.0.0 reflects the earlier preliminary 408-address classification and is retained only for version history.

Current processed CSV outputs corresponding to the final 404-address classification are also maintained in:

`data/secondary_market/`

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

### 3.1 Address-Level U.S. Residential Classification

The integrated asset-matching source is first grouped by normalized RealToken contract address.

For each address:

1. `source_true` is set to `TRUE` if at least one source row has `is_us_residential=TRUE`.
2. Available asset names are checked for a U.S. state or District of Columbia code.
3. Instruments or foreign assets matching the exclusion criteria are removed.
4. Addresses with `source_true=FALSE` are not broadened into the U.S. residential sample solely because their names contain a U.S. state code.

Final inclusion is therefore:

`source_true = TRUE`  
**AND** U.S. state/DC code confirmed in the available asset name  
**AND** no exclusion criterion matched.

This procedure produces a final U.S. residential classification universe of **404 unique RealToken contract addresses**.

The address-level classification is documented in:

`data/metadata/asset_master_match.csv`  
`data/metadata/asset_master_clean.csv`

### 3.2 Transaction and Return-Sample Filters

After address-level classification, the period-specific secondary-market analysis additionally requires:

1. A valid YAM or Swapcat transaction.
2. A valid transaction price and quantity after decimal normalization.
3. Compliance with the transaction-value threshold.
4. A calculable year-end 90-day VWAP for the relevant period.
5. The same token contract to have valid year-end VWAP observations in adjacent periods when calculating capital returns.

The main analysis applies a minimum transaction-value threshold of USD 1. A USD 5 threshold is used as a robustness specification.

The following are excluded from the main transaction sample where applicable:

- Payment tokens and stablecoins
- Governance or ecosystem tokens
- Lending products
- Receivable or revenue-participation products
- Non-U.S. assets
- Non-residential assets
- Invalid-decimal or non-economic transactions
- Assets without a calculable year-end 90-day VWAP

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

### 4.4 Supplementary Platform-Price Comparison

The supplementary 2026 price-level comparison uses the RealT platform-displayed tokenPrice contained in the dataset collected on April 6, 2026.

The observed secondary-market price is based on the most recent 90-day transaction VWAP through July 6, 2026.

Because the platform price and the observed secondary-market price refer to different dates, the resulting relative difference should not be interpreted as a contemporaneous price gap, direct investment-performance difference, or measure of platform overvaluation.

This analysis is treated only as a partial-year supplementary comparison.

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
└── .gitignore
```

The large raw YAM and Swapcat transaction files are not tracked directly in the main repository because of file-size limits. The unchanged raw source data are distributed separately through GitHub Release v2.0.0.

The final processed replication outputs corresponding to the **404-address U.S. residential classification** are distributed through GitHub Release v2.0.1. The processed archive in v2.0.0 reflects the earlier preliminary 408-address classification and is retained only for version history.

---

## 6. Reproducibility

### 6.1 Environment

- Python 3.10 or later
- The main recalculation script uses only Python standard-library modules and does not require additional third-party packages.

### 6.2 Main Analysis Script

The large raw transaction files required for the YAM and Swapcat recalculation are distributed separately through GitHub Release v2.0.0.

Download:

`secondary_market_raw_sources_v2.0.zip`

The release archive contains the raw YAM and Swapcat transaction data used in the study. These raw source data are unchanged by the subsequent U.S. residential classification correction.

Before running the analysis, create the following local directory:

```text
data/raw_secondary_market/

```

Place the following two files from the release archive in that directory:

```text
data/raw_secondary_market/yam_offeraccepted_raw.csv
data/raw_secondary_market/swapcat_realtoken_trades.csv
```

The metadata files required by the script are already included in the main repository:

```text
data/metadata/yam_token_metadata.csv
data/metadata/asset_master_match.csv
```

The expected local structure before execution is:

```text
sto-reits-comparison-study-final/
├── code/
│   └── recalculate_yam_swapcat.py
└── data/
    ├── metadata/
    │   ├── yam_token_metadata.csv
    │   └── asset_master_match.csv
    └── raw_secondary_market/
        ├── yam_offeraccepted_raw.csv
        └── swapcat_realtoken_trades.csv
```

Run the main recalculation script from the repository root:

```bash
python code/recalculate_yam_swapcat.py
```

The script generates recalculated outputs in:

```text
recalculated_output/
```

and creates the replication archive:

```text
yam_swapcat_recalculated_results.zip
```

For researchers who do not wish to rerun the raw-data processing, the final processed replication archive corresponding to the **404-address U.S. residential classification** is available in GitHub Release v2.0.1:

```text
secondary_market_processed_results_v2.0.1.zip
```

The processed archive in Release v2.0.0 corresponds to the preliminary 408-address classification and should not be used to reproduce the final thesis results.

### 6.3 Analysis Procedure

The script performs the following steps:

1. Load YAM and Swapcat transaction data.
2. Standardize RealToken and payment-token contract addresses.
3. Apply payment-token decimal specifications.
4. Identify eligible USD-linked payment transactions.
5. Calculate RealToken quantities, payment quantities, transaction prices, and USD trading values.
6. Group the asset-matching source by normalized RealToken address and construct the final U.S. residential classification using `source_true`, U.S. state/DC-name confirmation, and exclusion criteria.
7. Do not broaden addresses with `source_true=FALSE` solely on the basis of the asset name.
8. Remove duplicate YAM event records using transaction hash and log index and defensively remove exact duplicate Swapcat trade records.
9. Apply the primary USD 1 minimum transaction-value threshold.
10. Calculate asset-level 30-day, 60-day, and 90-day VWAPs.
11. Use the final 90-calendar-day VWAP as the primary year-end observed market-price measure.
12. Match identical normalized RealToken contract addresses across adjacent periods.
13. Calculate equal-weighted, median, and trade-value-weighted capital returns.
14. Recalculate USD 5 and broader USD-like robustness specifications.
15. Generate asset-year summaries, annual sample diagnostics, common-asset return outputs, and validation files.

The final address-level U.S. residential classification generated by this procedure contains **404 unique RealToken contract addresses**.

The 404-address figure represents the address-level classification universe before year-specific trading, transaction-value, year-end VWAP, and adjacent-period matching requirements are applied. Period-specific return sample sizes are therefore smaller than 404.

### 6.4 2026 Source-Coverage Cutoff

The final observed Swapcat transaction timestamp is:

`July 6, 2026 20:28:20 UTC`

The final observed YAM transaction timestamp is:

`August 3, 2026 20:09:20 UTC`

For the combined 2026 analysis, both markets are restricted to the common source-coverage cutoff:

`July 6, 2026 20:28:20 UTC`

A total of **1,502 YAM observations** after this cutoff are excluded from the combined 2026 analysis.

The 2026 results are treated only as supplementary partial-year evidence and are not interpreted as completed annual returns.

---

## 7. Key Repository Documentation

Detailed methodological documentation is provided in:

- `docs/Appendix_A_Data_Sources.md`
- `docs/Appendix_B_Sample_Construction.md`
- `docs/Appendix_C_YAM_Swapcat_Integration.md`
- `docs/Appendix_D_Return_Calculation.md`
- `docs/Appendix_E_Mint_Burn_Analysis.md`
- `docs/Appendix_F_REITs_Benchmark.md`
- `docs/Appendix_G_Data_Limitations.md`

Important metadata and validation files include:

- `data/metadata/source_list.csv`
- `data/metadata/data_dictionary.csv`
- `data/metadata/payment_token_decimals.csv`
- `data/metadata/raw_validation_report.csv`
- `data/metadata/asset_master_match.csv`
- `data/metadata/asset_master_clean.csv`

Source-collection and timing records are documented in:

- `logs/data_snapshot_log.csv`
- `logs/mint_burn_missing_token_log.txt`
- `logs/reits_official_data_collection_log.txt`

Selected thesis-table replication outputs are provided in:

`results/thesis_tables/`

---

## 8. Important Interpretation Notes

The RealT platform-based return measures, observed secondary-market capital returns, market-price-reflected composite-return proxies, and official REIT total returns do not have identical definitions.

In particular:

- RealT platform rental-yield measures do not reconstruct investor-level distribution timing.
- Observed secondary-market capital returns reflect executed YAM and Swapcat transaction prices and exclude rental distributions.
- The market-price-reflected composite-return measure is an exploratory proxy rather than an exact holding-period total return.
- REIT benchmark returns are official total-return measures that include distributions.
- Low secondary-market liquidity may affect observed RealToken prices and VWAP estimates.
- The supplementary platform-price comparison is non-contemporaneous because the RealT platform `tokenPrice` snapshot and the observed secondary-market VWAP do not share the same measurement date.
- Mint and burn events establish the occurrence and timing of token creation or destruction but do not establish the underlying economic cause.
- Different RealToken contract addresses are not joined through inferred migration mappings without an authoritative migration record.

Accordingly, the STO–REIT comparison is descriptive and exploratory and should not be interpreted as a comparison of identically constructed investment-return measures.

---

## 9. Version Note

The final U.S. residential secondary-market classification contains **404 unique RealToken contract addresses**.

GitHub Release v2.0.0 contains:

- the unchanged raw YAM and Swapcat source archive used for recalculation; and
- an earlier processed archive based on a preliminary 408-address classification, retained only for version history.

GitHub Release v2.0.1 contains:

- the corrected processed replication archive corresponding to the final 404-address classification.

Researchers seeking to reproduce the final thesis results should use:

- `secondary_market_raw_sources_v2.0.zip` from Release v2.0.0; and
- the current `code/recalculate_yam_swapcat.py` and repository metadata,

or use the corrected precomputed archive:

- `secondary_market_processed_results_v2.0.1.zip` from Release v2.0.1.
