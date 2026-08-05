# Appendix G. Data Limitations

## G.1 Token migration

A complete official mapping between old and new token contract addresses was not available.

No verified duplicate token contracts for the same normalized property were identified in the integrated trading sample. Potential unverified migrations are therefore not manually linked.

## G.2 Property sale and redemption

A complete asset-level dataset containing sale reasons, sale prices, redemption dates, and redemption amounts per token was not available.

On-chain burn events cannot independently establish the economic reason for token destruction.

## G.3 Trading inactivity

Tokens without valid secondary-market trades cannot be assigned an observable market price.

The return sample therefore represents assets with sufficient year-end trading activity and is not identical to the full universe of RealT offerings.

## G.4 Rental-yield measure

The RealT rental-yield field is a platform-provided annual measure.

It may differ from an investor-specific realized cash yield because of ownership dates, payment timing, fees, withholding, vacancies, or other asset-level events.

## G.5 Market-price measurement

Year-end prices are estimated from a 90-day VWAP because many tokens do not trade continuously.

The estimate can still be affected by thin liquidity, concentrated transactions, abnormal prices, and changes in token structure.

## G.6 Official REIT source files

The official annual REIT returns are documented, but a complete LSEG Datastream daily machine-readable source file was not obtained.

## G.7 Incomplete 2026 observations

The year 2026 is not included in the main annual-return comparison because it is incomplete and the underlying datasets use different cutoff dates.
