# Appendix C. Integration of YAM and Swapcat Trades

## C.1 Market treatment

YAM and Swapcat are two secondary-market venues in which RealTokens have been traded.

Trades from both venues are combined using the RealToken contract address. The integration does not treat the two venues as separate investment products.

## C.2 Standardization

The processing procedure applies the following standardization steps:

1. convert token and payment-token addresses to lowercase;
2. use blockchain block timestamps and convert them to UTC;
3. apply RealToken and payment-token decimals;
4. calculate economic token quantity and payment amount;
5. derive the transaction price per RealToken;
6. identify the source venue as YAM or Swapcat; and
7. remove duplicate records using transaction hash and log index where applicable.

## C.3 Payment-token treatment

USD-linked payment tokens are converted using their on-chain decimal structure.

RealToken-to-RealToken swaps and unidentified payment assets are separated from the primary USD-denominated sample unless a defensible dollar value can be established.

## C.4 Trade filters

The primary analysis excludes extremely small economic transactions using a minimum trade-value threshold.

A higher minimum-value threshold is used as a robustness check.

## C.5 Output files

- `platform_year_summary_us_residential.csv`
- `asset_year_price_summary_us_residential.csv`
- `common_asset_return_detail_us_residential.csv`
- `common_asset_returns_us_residential.csv`
- `common_asset_returns_robustness.csv`
