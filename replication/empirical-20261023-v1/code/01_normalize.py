import csv, os, math, statistics, zipfile, json
from collections import defaultdict, Counter
from datetime import datetime, timezone, date, timedelta

# Portable paths; normalization rules retained from the archived research code.
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=str(ROOT/'intermediate');os.makedirs(OUT,exist_ok=True)
YAM=str(ROOT/'inputs/raw/yam_offeraccepted_raw.csv')
SWAP=str(ROOT/'inputs/raw/swapcat_realtoken_trades.csv')
YAM_META=str(ROOT/'inputs/metadata/yam_token_metadata.csv')
MASTER=str(ROOT/'inputs/metadata/asset_master_match.csv')
# Direct USD-equivalent tokens used as the primary sample.
DIRECT_USD={
 '0xddafbb505ad214d7b80b1f830fccc89b60fb7a83', # USDC 6d
 '0xe91d153e0b41518a2ce8dd3d7944fa863463a97d', # WXDAI 18d
 '0xd10cc63531a514bba7789682e487add1f15a51e2', # old USDC 18d (Swapcat)
 '0x4ecaba5870353805a9f068101a40e0f32ed605c6', # USDT 6d (Swapcat)
}
# Broad USD-like robustness sample: direct stablecoins + RMM receipt tokens + REUSD.
BROAD_USD=DIRECT_USD | {
 '0xed56f76e9cbc6a64b821e9c016eafbd3db5436d1', # armmv3USDC 6d
 '0x0ca4f5554dd9da6217d62d8df2816c82bba4157b', # armmv3WXDAI 18d
 '0x7349c9eaa538e118725a6130e0f8341509b9f8a0', # armmWXDAI 18d
 '0x3390742ac0dce14ea6fcbd5ae02e2303c5d62ad9', # REUSD 18d
}

# Load and deduplicate asset master.
# The source file can contain duplicate rows and conflicting True/False flags
# for the same token address. A token is treated as a source US-residential
# candidate if at least one source row is marked True.
#
# Final classification additionally requires a recognizable U.S. state code
# in the asset name and excludes loans, factoring/profit-share instruments,
# foreign assets, and ecosystem/governance tokens.

import re

asset_rows = defaultdict(list)

with open(MASTER, encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        asset_rows[r['token_address'].lower()].append(r)

US_STATE_CODES = set(
    'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS '
    'MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV '
    'WI WY DC'.split()
)

EXCLUDE_ASSET_WORDS = (
    'LOAN',
    'FACTORING',
    'PROFIT SHARE',
    'RWA HOLDINGS',
    'SUISSE',
    'PANAMA',
    'COLOMBIA',
    'MEXICO',
    'ECOSYSTEM',
    'GOVERNANCE',
)

state_pattern = re.compile(
    r'(?:,|\s)('
    + '|'.join(sorted(US_STATE_CODES))
    + r')(?:\s+\d{5}(?:-\d{4})?)?\s*$'
)

asset_master = {}

for addr, rows in asset_rows.items():
    names = [
        r.get('trade_name', '')
        for r in rows
        if r.get('trade_name')
    ]

    # Resolve duplicate/conflicting source flags:
    # one or more True rows make the address a source candidate.
    source_true = any(
        str(r.get('is_us_residential', '')).strip().lower() == 'true'
        for r in rows
    )

    joined_names = ' | '.join(names).upper()

    excluded = any(
        word in joined_names
        for word in EXCLUDE_ASSET_WORDS
    )

    state_match = any(
        state_pattern.search(n.upper().strip())
        for n in names
    )

    if not source_true:
        is_us = False
        reason = 'source_flag_false'
    elif excluded:
        is_us = False
        reason = 'excluded_instrument_or_foreign'
    elif not state_match:
        is_us = False
        reason = 'no_us_state_match'
    else:
        is_us = True
        reason = 'us_state_in_name'

    # Prefer the on-chain RealToken name over address-style labels.
    name = next(
        (n for n in names if n.lower().startswith('realtoken')),
        names[0] if names else addr
    )

    asset_master[addr] = {
        'name': name,
        'is_us_residential': is_us,
        'classification_reason': reason,
    }

asset_addrs = set(asset_master)

us_res_addrs = {
    a for a, v in asset_master.items()
    if v['is_us_residential']
}

# Reproducibility guard for the archived asset-matching source used in this study.
EXPECTED_US_RESIDENTIAL_ADDRESSES = 404
if len(us_res_addrs) != EXPECTED_US_RESIDENTIAL_ADDRESSES:
    raise ValueError(
        f"Unexpected U.S. residential classification count: {len(us_res_addrs)} "
        f"(expected {EXPECTED_US_RESIDENTIAL_ADDRESSES}). "
        "Check asset_master_match.csv and the classification rules."
    )

# Metadata map.
meta={}
with open(YAM_META,encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        meta[r['address'].lower()]=r

# Determine a common 2026 cutoff from source coverage.
def max_source_dates():
    yam_max=None
    with open(YAM,encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            s=r.get('datetime_utc','')
            if s and (yam_max is None or s>yam_max): yam_max=s
    swap_max=None
    with open(SWAP,encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            ts=int(r['timestamp'])
            dt=datetime.fromtimestamp(ts,tz=timezone.utc).replace(tzinfo=None)
            if swap_max is None or dt>swap_max: swap_max=dt
    yam_dt=datetime.fromisoformat(yam_max)
    return yam_dt, swap_max, min(yam_dt,swap_max)
YAM_MAX, SWAP_MAX, COMMON_CUTOFF=max_source_dates()
COMMON_CUTOFF_DATE=COMMON_CUTOFF.date()

norm_path=os.path.join(OUT,'normalized_trades_primary.csv')
fields=['platform','block_number','datetime_utc','date','year','transaction_hash','log_index',
        'realtoken_address','realtoken_name','is_us_residential','trade_direction',
        'payment_address','payment_name','payment_symbol','payment_decimals',
        'realtoken_quantity','payment_quantity','unit_price_usd','trade_value_usd',
        'usd_class','source_price_raw','source_amount_raw']

# Store primary and broad normalized trades in memory for aggregation.
primary=[]
broad=[]
raw_stats=Counter()

# Helper to add normalized record.
def append_trade(rec, payment_addr):
    broad.append(rec)
    if payment_addr in DIRECT_USD:
        primary.append(rec)

# YAM: event raw_data encodes [offerToken, buyerToken, price, amount].
# In the uploaded CSV, offer_token_amount_raw is the event price word and
# buyer_token_amount_raw is the event amount word; price_raw is always zero.
# Duplicate event rows, if any, are removed by transaction hash + log index.
yam_seen_events=set()
with open(YAM,encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        raw_stats['yam_rows']+=1
        yam_event_key=(r['transaction_hash'].lower(), int(r['log_index']))
        if yam_event_key in yam_seen_events:
            continue
        yam_seen_events.add(yam_event_key)
        dt=datetime.fromisoformat(r['datetime_utc'])
        if dt.year==2026 and dt>COMMON_CUTOFF:
            raw_stats['yam_after_common_cutoff']+=1
            continue
        offer=r['offer_token'].lower(); buyer=r['buyer_token'].lower()
        offer_is_asset=offer in asset_addrs
        buyer_is_asset=buyer in asset_addrs
        offer_is_usd=offer in BROAD_USD
        buyer_is_usd=buyer in BROAD_USD
        if offer_is_asset and buyer_is_usd:
            asset=offer; payment=buyer; direction='realtoken_sold'
            offer_dec=int(r['offer_token_decimals']); buyer_dec=int(r['buyer_token_decimals'])
            event_price_raw=int(r['offer_token_amount_raw'])
            event_amount_raw=int(r['buyer_token_amount_raw'])
            rt_qty=event_amount_raw/(10**offer_dec)
            unit_price=event_price_raw/(10**buyer_dec)
            pay_qty=rt_qty*unit_price
        elif buyer_is_asset and offer_is_usd:
            asset=buyer; payment=offer; direction='realtoken_bought'
            offer_dec=int(r['offer_token_decimals']); buyer_dec=int(r['buyer_token_decimals'])
            event_price_raw=int(r['offer_token_amount_raw'])
            event_amount_raw=int(r['buyer_token_amount_raw'])
            pay_qty=event_amount_raw/(10**offer_dec)
            rt_per_pay=event_price_raw/(10**buyer_dec)
            rt_qty=pay_qty*rt_per_pay
            unit_price=(pay_qty/rt_qty) if rt_qty else math.nan
        else:
            raw_stats['yam_non_asset_usd_pair']+=1
            continue
        if not (rt_qty>0 and pay_qty>0 and math.isfinite(unit_price) and unit_price>0):
            raw_stats['yam_invalid_numeric']+=1
            continue
        pm=meta.get(payment,{})
        rec={
            'platform':'YAM','block_number':int(r['block_number']),'datetime_utc':dt.isoformat(),
            'date':dt.date().isoformat(),'year':dt.year,'transaction_hash':r['transaction_hash'].lower(),
            'log_index':int(r['log_index']),'realtoken_address':asset,
            'realtoken_name':asset_master[asset]['name'],'is_us_residential':asset_master[asset]['is_us_residential'],
            'trade_direction':direction,'payment_address':payment,
            'payment_name':pm.get('name',''),'payment_symbol':pm.get('symbol',''),
            'payment_decimals':int(pm.get('decimals') or (r['buyer_token_decimals'] if buyer_is_usd else r['offer_token_decimals'])),
            'realtoken_quantity':rt_qty,'payment_quantity':pay_qty,'unit_price_usd':unit_price,
            'trade_value_usd':pay_qty,'usd_class':'direct' if payment in DIRECT_USD else 'broad_only',
            'source_price_raw':event_price_raw,'source_amount_raw':event_amount_raw,
        }
        append_trade(rec,payment)
        raw_stats['yam_asset_usd_broad']+=1
        if payment in DIRECT_USD: raw_stats['yam_asset_usd_direct']+=1
        if direction=='realtoken_bought': raw_stats['yam_reverse_direction']+=1

# Swapcat: raw RealToken and payment amounts are directly supplied.
# Exact duplicate trade rows, if any, are removed using a transaction-level composite key.
swapcat_seen_trades=set()
with open(SWAP,encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        raw_stats['swapcat_rows']+=1
        swapcat_trade_key=(
            r['tx_hash'].lower(), r['block'], r['realtoken_addr'].lower(),
            r['payment_addr'].lower(), r['realtoken_amount'], r['payment_amount']
        )
        if swapcat_trade_key in swapcat_seen_trades:
            continue
        swapcat_seen_trades.add(swapcat_trade_key)
        asset=r['realtoken_addr'].lower(); payment=r['payment_addr'].lower()
        if asset not in asset_addrs:
            raw_stats['swapcat_asset_not_in_master']+=1
            continue
        if payment not in BROAD_USD:
            raw_stats['swapcat_non_usd_payment']+=1
            continue
        dt=datetime.fromtimestamp(int(r['timestamp']),tz=timezone.utc).replace(tzinfo=None)
        if dt.year==2026 and dt>COMMON_CUTOFF:
            raw_stats['swapcat_after_common_cutoff']+=1
            continue
        rt_qty=int(r['realtoken_amount'])/(10**int(r['realtoken_decimals']))
        pay_qty=int(r['payment_amount'])/(10**int(r['payment_decimals']))
        if not (rt_qty>0 and pay_qty>0):
            raw_stats['swapcat_invalid_numeric']+=1
            continue
        unit_price=pay_qty/rt_qty
        rec={
            'platform':'Swapcat','block_number':int(r['block']),'datetime_utc':dt.isoformat(),
            'date':dt.date().isoformat(),'year':dt.year,'transaction_hash':r['tx_hash'].lower(),
            'log_index':'','realtoken_address':asset,'realtoken_name':asset_master[asset]['name'],
            'is_us_residential':asset_master[asset]['is_us_residential'],'trade_direction':'realtoken_sold',
            'payment_address':payment,'payment_name':r['payment_name'],'payment_symbol':r['payment_symbol'],
            'payment_decimals':int(r['payment_decimals']),'realtoken_quantity':rt_qty,
            'payment_quantity':pay_qty,'unit_price_usd':unit_price,'trade_value_usd':pay_qty,
            'usd_class':'direct' if payment in DIRECT_USD else 'broad_only',
            'source_price_raw':'','source_amount_raw':r['realtoken_amount'],
        }
        append_trade(rec,payment)
        raw_stats['swapcat_asset_usd_broad']+=1
        if payment in DIRECT_USD: raw_stats['swapcat_asset_usd_direct']+=1

# Stable ordering and primary normalized output.
primary.sort(key=lambda x:(x['datetime_utc'],x['platform'],x['transaction_hash'],str(x['log_index'])))
broad.sort(key=lambda x:(x['datetime_utc'],x['platform'],x['transaction_hash'],str(x['log_index'])))
with open(norm_path,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for r in primary:
        out=r.copy()
        for k in ['realtoken_quantity','payment_quantity','unit_price_usd','trade_value_usd']:
            out[k]=f"{out[k]:.12g}"
        w.writerow(out)

# Cleaned asset master.
clean_master_path=os.path.join(OUT,'asset_master_clean.csv')
with open(clean_master_path,'w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(['token_address','realtoken_name','is_us_residential','classification_reason'])
    for a in sorted(asset_master): w.writerow([a,asset_master[a]['name'],asset_master[a]['is_us_residential'],asset_master[a]['classification_reason']])


with open(os.path.join(OUT,'normalization_audit.json'),'w',encoding='utf-8') as f:
 json.dump({'raw_stats':dict(raw_stats),'cutoff':COMMON_CUTOFF.isoformat(),'yam_max':YAM_MAX.isoformat(),'swapcat_max':SWAP_MAX.isoformat(),'normalized_primary_n':len(primary)},f,ensure_ascii=False,indent=2)
print('Raw normalization completed',len(primary),COMMON_CUTOFF.isoformat())
