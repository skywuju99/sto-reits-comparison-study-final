# Appendix G. Data Limitations

## G.1 Single-platform case study

The analysis focuses on RealT. The findings cannot be generalized directly to the entire real estate STO market.

## G.2 Geographic and property concentration

The main sample consists of U.S. residential rental properties and is concentrated in particular local markets.

## G.3 Missing investor-level cash flows

The available platform data do not provide complete investor-level cumulative distributions, distribution dates, transaction costs, or tax information.

Annual net rent is therefore used to construct a rental-yield proxy.

## G.4 Total-investment-value limitation

Changes in total investment value may reflect:

- Changes in token price
- Changes in token quantity
- New issuance or redemption
- Platform-data updates

The platform-data-based capital-return measure is therefore treated as an exploratory proxy.

## G.5 Low-liquidity price observations

The observed secondary-market price is based only on executed trades.

It does not imply that:

- All outstanding tokens can be sold at the observed price
- A large sell order can be executed without price impact
- Assets without trades have unchanged market value

## G.6 Common-asset selection

Capital returns are calculated only for assets traded in both adjacent periods.

Assets without valid trades in either period are excluded, creating potential selection bias.

## G.7 Year-end 90-day VWAP

The final 90-day VWAP reduces reliance on a single last trade but may still be affected by:

- A small number of transactions
- Concentrated transaction volume
- Low-value trades
- Stale trading activity
- Differences in the composition of traded assets

## G.8 Monthly aggregate VWAP

Monthly aggregate VWAP is affected by the composition of assets traded in each month.

It is therefore interpreted as a descriptive price-level indicator rather than a continuous market-return index.

## G.9 Non-contemporaneous platform-price comparison

The RealT tokenPrice was collected on May 24, 2026.

The observed secondary-market prices were calculated using:

- Historical year-end 90-day periods
- The recent 90-day period ending July 6, 2026

The platform and transaction-price observations do not share the same measurement date.

The reported -72.6% value must not be interpreted as:

- A same-date historical pricing gap
- A definitive platform-price overvaluation estimate
- A liquidation-price discount applicable to the entire outstanding supply

## G.10 Partial-year 2026 analysis

The 2026 analysis ends on July 6, 2026 and is not a completed annual observation.

It is not compared directly with a completed annual REIT return.

## G.11 Mint and burn events

Mint and burn events are identified through ERC-20 Transfer events involving the zero address.

A burn event alone does not reveal whether the economic cause was:

- Property sale
- Redemption
- Liquidation
- Token migration
- Technical restructuring

## G.12 Token migration

An official and complete mapping between old and new RealToken contract addresses was not available.

No manual migration link was imposed where a verified mapping could not be established.

## G.13 REIT comparison

The STO observed capital-return measure excludes rental distributions, whereas the official REIT total-return measure includes distributions.

The two measures are presented together only as a descriptive comparison of price-adjustment patterns.

## G.14 Official index source files

Nareit provides annual investment-sector and property-sector/subsector return workbooks on its official annual returns page.

The repository provides the annual observations used in the final thesis together with source links and a collection log. Use and redistribution of the official source materials remain subject to the provider's terms.
