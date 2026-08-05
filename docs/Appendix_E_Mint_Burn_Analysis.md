# Appendix E. RealToken Mint and Burn Analysis

## E.1 Identification rule

Mint and burn events are identified from RealToken Transfer events:

- zero address to a non-zero address: mint;
- non-zero address to the zero address: burn.

Ordinary wallet-to-wallet transfers are not classified as mint or burn events.

## E.2 Coverage

The collection universe combines token addresses observed in:

- YAM metadata;
- YAM trading records; and
- Swapcat trading records.

The final address union contains 791 token addresses.

Mint or burn events are available for 785 addresses. The remaining six addresses are payment, stablecoin, governance, or ecosystem tokens rather than property RealTokens and are excluded from the property-token analysis.

## E.3 Event records

The complete event file contains:

- 20,687 mint and burn events;
- 6,731 mint events; and
- 13,956 burn events.

These event counts should not be interpreted directly as the number of separate property offerings or exits. A single asset may generate multiple investor-level burn transactions.

## E.4 Analytical use

The analysis distinguishes:

- initial mint;
- additional mint;
- partial burn; and
- full burn.

A burn event alone does not establish whether the cause was a property sale, redemption, liquidation, migration, or technical restructuring.

## E.5 Repository files

- `data/mint_burn/realtoken_mint_burn_history_complete.csv`
- `data/mint_burn/mint_burn_token_coverage.csv`
- `logs/mint_burn_missing_token_log.txt`
