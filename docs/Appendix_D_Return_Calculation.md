# Appendix D. Return and Price Calculation

## D.1 Scope

The empirical analysis distinguishes among:

1. Platform-data-based rental-yield and capital-return proxies
2. Platform-data-based exploratory composite-return proxies
3. Swapcat–YAM observed secondary-market capital returns
4. Market-price-reflected composite-return proxies
5. Supplementary platform-price-level comparisons
6. Official REIT total returns

These measures do not have identical definitions and are not interpreted as directly interchangeable performance measures.

## D.2 Matched Asset Sets

For each platform-data comparison period, the matched set \(M(t)\) consists of assets observed in both \(t-1\) and \(t\).

Platform-based rental-yield and capital-return proxies use the same matched asset set and the same beginning-period total-investment-value basis.

For secondary-market capital-return calculations, assets are matched using the same normalized RealToken contract address across adjacent comparison periods. Different contract addresses are not joined through inferred migration mappings unless an authoritative migration mapping is available.

The secondary-market analysis uses the final U.S. residential address-level classification described in Appendix B. The final classification universe contains 404 unique RealToken contract addresses before year-specific trading, transaction-value, year-end VWAP, and adjacent-period matching filters are applied.

## D.3 Year-End Observed VWAP

For each RealToken asset, the primary year-end observed market price is calculated from valid USD-linked secondary-market transactions during the final 90 calendar days of each year.

\[
VWAP_{i,t}
=
\frac{\sum_j P_{i,t,j}Q_{i,t,j}}
{\sum_j Q_{i,t,j}}
\]

where:

- \(P_{i,t,j}\) is the observed transaction price per RealToken;
- \(Q_{i,t,j}\) is the RealToken quantity traded; and
- \(j\) indexes valid YAM and Swapcat transactions for asset \(i\).

Only assets with valid year-end VWAP observations in both adjacent comparison periods are included in the corresponding capital-return calculation.

The observed VWAP is a transaction-based reference price and does not imply that the entire outstanding token supply could be sold at that price.

## D.4 Observed Secondary-Market Capital Return

For an asset observed in two adjacent comparison periods:

\[
CR_{i,t}
=
\frac{VWAP_{i,t}-VWAP_{i,t-1}}
{VWAP_{i,t-1}}
\]

Observed capital returns are summarized using:

- equal-weighted mean;
- median return; and
- trade-value-weighted mean.

The trade-value-weighted result is used to reflect differences in observed transaction activity, while the equal-weighted mean and median are reported as complementary measures.

Under the final 404-address U.S. residential classification, the 2024–2025 secondary-market common-asset sample contains **382 assets**. The trade-value-weighted observed capital return for this sample is approximately **-15.15%**.

This result should be distinguished from the rental-data-merged sample described below.

## D.5 Platform-Data-Based Exploratory Composite-Return Proxy

The platform-data-based exploratory proxy combines:

1. an annual-net-rent-based rental-yield proxy; and
2. a total-investment-value-based capital-return proxy.

Both components are calculated using the same matched asset set and the same beginning-period total-investment-value basis.

Changes in total investment value may reflect token-quantity changes, platform-data updates, or other changes in addition to economic asset-value changes.

Accordingly, this measure is not interpreted as a strict holding-period total return.

## D.6 Market-Price-Reflected Composite-Return Proxy

For assets with both rental information and valid secondary-market price observations:

\[
MCR_t = RY_t + CR_t
\]

where:

- \(RY_t\) is the annual rental-yield proxy; and
- \(CR_t\) is the observed secondary-market capital-return component for the same matched sample.

For this merged sample, the rental-yield proxy is calculated as total annual net rent in the ending year divided by the same sample's beginning-period total investment value. The capital-return component is weighted by the same beginning-period total-investment-value basis.

The rental-data-merged sample is smaller than the full secondary-market sample because the same asset must have RealT rental/investment observations in both adjacent years as well as valid adjacent-period secondary-market VWAP observations.

Under the final 404-address classification, the merged-sample results are:

| Ending year | Matched assets | Rental-yield proxy | Capital-return component | Composite-return proxy |
|---|---:|---:|---:|---:|
| 2022 | 17 | 7.91% | 5.98% | 13.89% |
| 2023 | 56 | 9.25% | -2.50% | 6.75% |
| 2024 | 287 | 10.75% | 10.17% | 20.93% |
| 2025 | 243 | 10.48% | -15.80% | -5.32% |

For 2025 in particular:

- Full secondary-market common-asset sample: \(N=382\)
- Trade-value-weighted capital return for the full secondary-market sample: approximately -15.15%
- Rental-data-merged sample: \(N=243\)
- Rental-yield proxy: approximately 10.48%
- Capital-return component on the beginning-period investment-value basis: approximately -15.80%
- Market-price-reflected composite-return proxy: approximately -5.32%

Therefore, -15.15% and -15.80% refer to different samples and weighting bases and should not be treated as conflicting estimates.

The reported composite proxy is calculated from the unrounded rental-yield and capital-return components and then rounded for presentation.

This proxy does not reconstruct investor-level distribution dates, reinvestment, complete cash-flow histories, transaction costs, or taxes, and therefore is not an exact holding-period total return.

## D.7 Comparison with REIT Returns

The primary REIT benchmark is the FTSE Nareit U.S. Real Estate Index Series Residential sector annual total return.

The official REIT measure includes both price changes and distributions.

By contrast, the Swapcat–YAM observed capital-return measure reflects secondary-market price changes only and excludes rental distributions.

The market-price-reflected composite-return proxy adds a rental-yield proxy to the observed secondary-market capital-return component, but it remains an exploratory approximation rather than a fully reconstructed investor holding-period return.

Therefore, comparisons with REIT returns are descriptive and do not establish direct performance superiority.

## D.8 Supplementary Platform-Price-Level Comparison

The supplementary platform-price comparison uses the RealT platform-displayed `tokenPrice` contained in the RealT tokenHistory research snapshot archived on April 6, 2026 (KST, UTC+9).

The secondary-market comparison price is based on each asset's most recent 90-day transaction VWAP through the common 2026 source-coverage cutoff of July 6, 2026 20:28:20 UTC.

For each matched asset, the relative difference is calculated as:

\[
Relative\ Difference_i
=
\left(
\frac{Observed\ VWAP_i}
{Platform\ tokenPrice_i}
-1
\right)
\times 100
\]

The cross-asset summary is trade-value weighted using each asset's transaction value in the corresponding 2026 trailing 90-day window.

Under the final 404-address classification, **283 assets** have the required 2026 trailing 90-day observed price in the secondary-market sample. The resulting trade-value-weighted platform-price relative difference is approximately **-72.48%**.

The April 6 platform `tokenPrice` and the secondary-market VWAP through July 6 do not refer to the same date. The -72.48% figure is therefore a non-contemporaneous price-level comparison and must not be interpreted as:

- a contemporaneous pricing gap;
- an investment return;
- a direct measure of platform overvaluation; or
- a completed annual performance measure.

Historical same-date platform-price snapshots are not reconstructed for each secondary-market comparison period, and year-specific asset samples differ.

## D.9 2026 Common-Asset Secondary-Market Supplement

A separate 2026 supplementary calculation compares observed secondary-market prices for common assets between the 2025 year-end 90-day period and the most recent 90-day period ending at the common 2026 cutoff.

Under the final classification, the common-asset sample contains \(N=283\):

- Equal-weighted return: **-72.78%**
- Median return: **-74.01%**
- Trade-value-weighted return: **-71.28%**

All **283** matched assets show a decline under this comparison.

The -71.28% result is conceptually different from the -72.48% platform-price-level comparison in Section D.8.

- -72.48% compares the April 6, 2026 RealT platform `tokenPrice` with observed secondary-market prices through July 6, 2026.
- -71.28% compares two observed secondary-market price windows for the same matched assets: the 2025 year-end 90-day period and the recent 2026 90-day period.

Neither result is treated as a completed 2026 annual return.

## D.10 Monthly Analysis

Monthly aggregate VWAP is used as a descriptive price-level indicator.

Because the composition of assets traded can change across months, changes in aggregate monthly VWAP may reflect both price movements and changes in the composition of traded assets.

Accordingly, monthly aggregate VWAP is not interpreted as a fixed-portfolio return series.
