# Appendix D. Return and Price Calculation

## D.1 Scope

The empirical analysis distinguishes among:

1. Platform-data-based rental-yield and capital-return proxies
2. Platform-data-based exploratory composite-return proxies
3. Swapcat–YAM observed capital returns
4. Market-price-reflected composite-return proxies
5. Official REIT total returns

These measures do not have identical definitions and are not interpreted as directly interchangeable performance measures.

## D.2 Matched asset sets

For each comparison period, the matched set \(M(t)\) consists of assets observed in both \(t-1\) and \(t\). Platform-based rental-yield and capital-return proxies use the same matched set and the same beginning-period total-investment-value basis.

## D.3 Year-end observed VWAP

The observed year-end price of asset \(i\) in year \(t\) is the volume-weighted average price of valid USD-linked transactions during the final 90 days of that year.

\[
VWAP_{i,t}
=
\frac{\sum_j P_{i,t,j}Q_{i,t,j}}
{\sum_j Q_{i,t,j}}
\]

The observed VWAP does not imply that the entire outstanding token supply can be sold at that price.

## D.4 Observed capital return

\[
CR_{i,t}
=
\frac{VWAP_{i,t}-VWAP_{i,t-1}}
{VWAP_{i,t-1}}
\]

Observed capital returns are summarized using the equal-weighted mean, median, and trade-value-weighted mean.

## D.5 Platform-data-based exploratory composite-return proxy

The platform-data-based proxy combines annual-net-rent-based rental-yield proxies with total-investment-value-based capital-return proxies using the same matched set and beginning-period basis.

Changes in total investment value may reflect token-quantity changes or platform-data updates as well as economic value changes. The measure is not a strict holding-period total return.

## D.6 Market-price-reflected composite-return proxy

\[
MCR_t = RY_t + CR_t
\]

This proxy combines a platform annual-net-rent-based rental-yield proxy with a Swapcat–YAM observed capital return. It does not reconstruct investor-level cumulative distributions, distribution dates, transaction costs, or taxes.

## D.7 Comparison with REIT returns

The official U.S. Residential REIT benchmark is an annual total-return measure including price changes and distributions. STO observed capital returns exclude rental distributions. The comparison is descriptive and does not establish direct performance superiority.

## D.8 Current platform-price comparison

The platform-price comparison uses RealT tokenPrice collected on May 24, 2026 as a common reference.

\[
Relative\ Difference
=
\left(
\frac{Observed\ VWAP}
{Current\ tokenPrice}
-1
\right)
\times 100
\]

Historical same-date platform-price snapshots were not available. Year-specific asset samples also differ. Therefore, changes across years must not be interpreted as a continuous same-asset pricing-gap series.

## D.9 Monthly and 2026 analysis

Monthly aggregate VWAP is a descriptive price-level indicator because the composition of traded assets changes across months.

The 2026 analysis is a partial-year supplementary analysis ending July 6, 2026 and is not interpreted as a completed annual return.
