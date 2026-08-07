# Appendix G. Data Limitations

## G.1 Single-platform case study

The analysis focuses on RealT and cannot be generalized directly to the entire real estate STO market.

## G.2 Missing investor-level cash flows

Complete investor-level cumulative distributions, distribution dates, transaction costs, and taxes were not available.

## G.3 Total-investment-value limitation

Changes in total investment value may reflect token-price changes, token-quantity changes, issuance or redemption, and platform-data updates.

## G.4 Low-liquidity observations

Observed transaction prices are based only on executed trades and do not imply that the entire outstanding token supply can be sold at the observed price.

## G.5 Common-asset selection

Capital returns are calculated only for assets traded in both adjacent periods, creating potential selection bias.

## G.6 Year-end 90-day VWAP

The final 90-day VWAP may be affected by a small number of transactions, concentrated volume, stale trading activity, and differences in traded-asset composition.

## G.7 Monthly aggregate VWAP

Monthly aggregate VWAP is affected by changes in traded-asset composition and is interpreted as a descriptive price-level indicator rather than a continuous market-return index.

## G.8 Non-contemporaneous platform-price comparison

RealT tokenPrice was collected on May 24, 2026. Historical year-end 90-day VWAPs and the recent 90-day period ending July 6, 2026 do not share the same measurement date.

Year-specific asset samples are not identical. Relative differences across years must not be interpreted as a continuous same-asset pricing-gap series.

## G.9 Snapshot time limitation

The RealT collection date is known. If the exact collection time and timezone were not recorded, they must be reported as not recorded rather than inferred.

Blockchain transactions are processed using block timestamps; the exact cutoff timestamp and block should be reported where available.

## G.10 Partial-year 2026 analysis

The 2026 analysis ends on July 6, 2026 and is not a completed annual observation.

## G.11 Mint, burn, sale, redemption, and migration

Mint and burn events are identified through ERC-20 Transfer events involving the zero address. A burn event alone does not reveal whether the economic cause was a property sale, redemption, liquidation, token migration, or technical restructuring.

Complete token-supply histories, economic reasons for mint and burn events, sale or redemption reasons, token-level redemption amounts, and an official migration mapping were not available.

## G.12 REIT comparison

STO observed capital returns exclude rental distributions, whereas official REIT total returns include distributions.

## G.13 Official index raw files

The full machine-readable LSEG Datastream historical dataset was not available. The study uses documented official annual return observations.
