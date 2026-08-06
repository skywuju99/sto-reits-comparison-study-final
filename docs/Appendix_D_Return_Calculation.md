# Appendix D. Return and Price Calculation

## D.1 Scope

The empirical analysis distinguishes among:

1. Platform-data-based rental-yield and capital-return proxies
2. Swapcat–YAM observed capital returns
3. Market-price-reflected composite-return proxies
4. Official REIT total returns

These measures do not have identical definitions and are not interpreted as directly interchangeable performance measures.

## D.2 Year-end observed VWAP

The observed year-end price of asset $i$ in year $t$ is defined as the volume-weighted average price of valid trades executed during the final 90 days of that year.

$$
VWAP_{i,t}=\frac{\sum_j P_{i,t,j}Q_{i,t,j}}{\sum_j Q_{i,t,j}}
$$

where:

- $P_{i,t,j}$: observed transaction price
- $Q_{i,t,j}$: transaction quantity
- $j$: valid trade observation

Only USD-linked payment-token transactions that satisfy the minimum trade-value rule are included.

The observed VWAP does not imply that the entire outstanding token supply can be sold at that price.

## D.3 Observed capital return

Observed capital returns are calculated only for assets with valid year-end 90-day VWAPs in two consecutive periods.

$$
CR_{i,t}=\frac{VWAP_{i,t}-VWAP_{i,t-1}}{VWAP_{i,t-1}}
$$

The following summary measures are reported:

- Equal-weighted mean
- Median
- Trade-value-weighted mean
- Number of rising and declining assets

The measure is referred to as the Swapcat–YAM observed capital return rather than the return of the entire RealToken market.

## D.4 Market-price-reflected composite-return proxy

For the common-asset sample with available platform rental and investment data, the rental-yield proxy and observed capital return are combined as follows:

$$
MCR_t=RY_t+CR_t
$$

where:

- $RY_t$: rental-yield proxy based on annual net rent
- $CR_t$: observed capital return based on secondary-market VWAP
- $MCR_t$: market-price-reflected composite-return proxy

This measure is not a strict holding-period total return because the available dataset does not reconstruct investor-level cumulative distributions, distribution dates, transaction costs, or taxes.

## D.5 Platform-data-based composite-return proxy

The platform-data-based proxy combines:

- Annual net-rent-based rental-yield proxy
- Total-investment-value-based capital-return proxy

Changes in total investment value may reflect token-quantity changes or platform-data updates as well as changes in economic value. The measure is therefore treated as an exploratory proxy.

## D.6 Comparison with REIT returns

The official U.S. Residential REIT benchmark is an annual total-return measure that includes both price changes and distributions.

The STO observed capital-return measure excludes rental distributions. Therefore, their side-by-side presentation is used to examine differences in observed price adjustment and market structure, not to establish direct performance superiority.

The market-price-reflected composite-return proxy also differs from the official REIT total-return measure and is interpreted as a supplementary approximation.

## D.7 Current platform-price comparison

The platform-price comparison uses the RealT tokenPrice collected on May 24, 2026 as a common reference.

$$
Relative\ Difference=\left(\frac{Observed\ VWAP}{Current\ tokenPrice}-1\right)\times100
$$

Historical year-end platform-price snapshots were not available. The comparison is therefore non-contemporaneous and must not be interpreted as:

- A historical same-date pricing gap
- A definitive overvaluation estimate
- A liquidation-price estimate for the full outstanding supply

## D.8 Monthly analysis

Monthly VWAP is calculated using the actual block timestamp and transaction quantity.

Because the composition of traded assets changes from month to month, monthly aggregate VWAP is interpreted as a descriptive price-level indicator rather than a continuous market-return index.

## D.9 Partial-year 2026 analysis

The 2026 analysis uses transactions observed through July 6, 2026.

The 2025 year-end 90-day period and the most recent 90-day period ending July 6, 2026 are compared only for assets traded in both periods.

The result is a partial-year supplementary analysis and is not interpreted as a completed annual return.
