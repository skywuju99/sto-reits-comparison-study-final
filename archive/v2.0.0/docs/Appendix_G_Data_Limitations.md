> **과거 버전 보존자료 / Historical version.** 최신 논문 재현은 저장소 최상위 README와 `replication/empirical-20261023-v1/`을 사용하십시오. 이 문서의 “final/current”는 당시 버전을 뜻합니다.

# Appendix G. Data Limitations

## G.1 Single-Platform Case Study

The analysis focuses on RealT and cannot be generalized directly to the entire real estate STO market.

## G.2 Asset-Classification Limitation

The final U.S. residential secondary-market classification is constructed from the available asset-matching source and token/asset names.

At the normalized address level, `source_true` is set to `TRUE` when at least one source row has `is_us_residential=TRUE`. Final inclusion additionally requires confirmation of a U.S. state or District of Columbia code in the available asset name and the absence of an exclusion condition for foreign assets or non-primary instruments.

Addresses with `source_true=FALSE` are not broadened into the U.S. residential sample solely because their names contain a U.S. state or District of Columbia code.

This procedure produces a final classification universe of 404 unique RealToken contract addresses. However, the classification remains dependent on the completeness and correctness of the source flags and available naming information. Therefore, residual classification error cannot be ruled out.

The 404-address classification universe should also not be interpreted as the number of assets entering every annual return calculation. Year-specific samples are smaller because valid trading activity, transaction-value filters, year-end 90-day VWAPs, and adjacent-period matching are additionally required.

## G.3 Missing Investor-Level Cash Flows

Complete investor-level cumulative distributions, distribution dates, transaction costs, taxes, and reinvestment histories were not available.

Accordingly, the return measures constructed in this study should not be interpreted as exact investor-level holding-period returns.

## G.4 Total-Investment-Value Limitation

Changes in total investment value may reflect token-price changes, token-quantity changes, issuance or redemption activity, and platform-data updates.

Because complete historical token-quantity information is not available for all asset-year observations, price effects and quantity effects cannot always be separated precisely.

## G.5 Low-Liquidity Observations

Observed transaction prices are based only on executed trades and do not imply that the entire outstanding token supply can be sold at the observed price.

Low transaction frequency and concentrated trading volume may also cause observed market prices to differ from prices that would prevail under deeper market liquidity.

## G.6 Common-Asset Selection

Capital returns are calculated only for assets with valid price observations in both adjacent comparison periods.

This matched-asset requirement may create selection bias because assets without sufficient trading activity are excluded from the corresponding return calculation.

## G.7 Year-End 90-Day VWAP

The final 90-day VWAP may be affected by a small number of transactions, concentrated volume, stale trading activity, and differences in traded-asset composition.

The 90-day window improves price availability relative to a single-date observation but does not eliminate liquidity-related measurement limitations.

## G.8 Monthly Aggregate VWAP

Monthly aggregate VWAP is affected by changes in traded-asset composition and is interpreted as a descriptive price-level indicator rather than a continuous fixed-portfolio market-return index.

## G.9 Non-Contemporaneous Platform-Price Comparison

The RealT platform-displayed `tokenPrice` used in the supplementary price-level comparison is taken from the RealT tokenHistory research snapshot archived on April 6, 2026 (KST, UTC+9).

Historical year-end 90-day VWAP observations and the recent 90-day secondary-market period through July 6, 2026 do not share the same measurement date as the April 6 platform-price snapshot.

Accordingly, the resulting relative differences are non-contemporaneous price-level comparisons.

They must not be interpreted as:

- contemporaneous pricing gaps;
- investment returns;
- measures of platform overvaluation; or
- a continuous same-asset pricing-gap series.

Year-specific asset samples also differ across the historical comparisons.

## G.10 Snapshot-Time and Source-Coverage Limitation

The RealT tokenHistory research snapshot was archived on April 6, 2026.

The contemporaneous research work record indicates an approximate collection time of 19:48 KST (UTC+9). This time is not an independently machine-embedded timestamp and is therefore reported as approximate rather than as an exact collection timestamp.

Blockchain transaction timing is based on block timestamps standardized to UTC.

The final observed source timestamps are:

- Swapcat: July 6, 2026 20:28:20 UTC
- YAM: August 3, 2026 20:09:20 UTC

For the combined 2026 analysis, both markets are restricted to the common source-coverage cutoff of July 6, 2026 20:28:20 UTC.

A total of 1,502 YAM observations after the common cutoff are excluded from the combined 2026 analysis.

The exact cutoff block number was not separately recorded and is therefore not reconstructed or inferred.

## G.11 Partial-Year 2026 Analysis

The combined 2026 analysis ends at the common source-coverage cutoff of July 6, 2026 20:28:20 UTC.

Although the YAM source contains later observations, transactions after the common cutoff are excluded from the combined analysis.

The 2026 results are supplementary partial-year observations and are not interpreted as completed annual returns.

## G.12 Mint, Burn, Sale, Redemption, and Migration

Mint and burn events are identified through ERC-20 Transfer events involving the zero address.

A burn event alone does not reveal whether the economic cause was a property sale, investor redemption, liquidation, token migration, contract restructuring, or another technical or economic event.

The on-chain event records therefore establish the occurrence and timing of mint and burn events but do not establish their economic causes.

Complete historical token-quantity information, authoritative economic reasons for individual mint and burn events, token-level redemption amounts, and an official migration mapping were not available.

Different contract addresses are therefore not joined through inferred migration mappings in the primary analysis.

The mint-and-burn collection universe is broader than the final 404-address U.S. residential classification used for the main secondary-market return analysis, and the two counts refer to different analytical universes.

## G.13 REIT Comparison

STO observed secondary-market capital returns exclude rental distributions, whereas official REIT total returns include both price changes and distributions.

The market-price-reflected STO composite-return measure includes a rental-yield proxy but remains an exploratory approximation rather than a directly equivalent total-return measure.

The STO–REIT comparison is therefore descriptive and should not be interpreted as a comparison of identically constructed return measures.

## G.14 Official REIT Index Data

The primary REIT benchmark is the FTSE Nareit U.S. Real Estate Index Series Residential sector, and the FTSE EPRA Nareit Global USD Total Return series is used as a supplementary benchmark.

The complete proprietary FTSE/Nareit index datasets and machine-readable source data are not redistributed in this repository because of licensing and redistribution restrictions.

The repository therefore documents the benchmark definitions, official sources, access records, and methodology required to identify the series used in the thesis.

Researchers seeking to reproduce the REIT comparison must obtain the corresponding benchmark observations independently from the official Nareit/FTSE sources.
