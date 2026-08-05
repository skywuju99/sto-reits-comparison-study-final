# Appendix D. Return Calculation

## D.1 Year-end secondary-market price

For each token and calendar year, the year-end market price is calculated as the volume-weighted average price of valid trades executed during the final 90 days of that year.

\[
VWAP_{i,t} =
\frac{\sum_j P_{i,t,j}Q_{i,t,j}}
{\sum_j Q_{i,t,j}}
\]

where \(P_{i,t,j}\) is the execution price and \(Q_{i,t,j}\) is the traded RealToken quantity.

## D.2 Capital return

Capital return is calculated for token \(i\) between adjacent years as:

\[
CR_{i,t} =
\frac{VWAP_{i,t}-VWAP_{i,t-1}}
{VWAP_{i,t-1}}
\]

Only tokens with valid year-end VWAP observations in both adjacent years are included.

## D.3 Rental yield

The rental-yield measure is obtained from the RealT asset-year dataset.

It is a platform-provided annual yield measure and is not a reconstruction of each investor's actual cash-flow sequence.

## D.4 Adjusted total return

The study combines rental yield and secondary-market capital return as:

\[
ATR_{i,t} = RY_{i,t} + CR_{i,t}
\]

This measure is described as a **secondary-market-price-adjusted total return** rather than a strict holding-period return.

## D.5 Aggregation and robustness

The analysis reports:

- equal-weighted mean capital return;
- median capital return;
- transaction-value-weighted capital return;
- results excluding observations with absolute capital returns above 50%; and
- results using alternative minimum trade-value thresholds.

## D.6 REIT comparison

The REIT benchmark uses annual USD total returns from the FTSE EPRA Nareit Global Real Estate Index Series for complete calendar years 2022–2025.
