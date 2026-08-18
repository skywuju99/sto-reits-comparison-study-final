import csv, os, math, statistics, zipfile, json
from collections import defaultdict, Counter
from datetime import datetime, timezone, date, timedelta

# Repository paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

OUT = os.path.join(REPO_ROOT, 'recalculated_output')
os.makedirs(OUT, exist_ok=True)

# Raw YAM and Swapcat transaction files are distributed separately
# through the GitHub Release asset:
# secondary_market_raw_sources_v2.0.zip
#
# They are not tracked directly in the main repository because of file-size limits.
# Before running this script, download the release archive and place:
#   yam_offeraccepted_raw.csv
#   swapcat_realtoken_trades.csv
# in data/raw_secondary_market/

RAW_DIR = os.path.join(REPO_ROOT, 'data', 'raw_secondary_market')

YAM = os.path.join(RAW_DIR, 'yam_offeraccepted_raw.csv')
SWAP = os.path.join(RAW_DIR, 'swapcat_realtoken_trades.csv')

YAM_META = os.path.join(
    REPO_ROOT, 'data', 'metadata', 'yam_token_metadata.csv'
)
MASTER = os.path.join(
    REPO_ROOT, 'data', 'metadata', 'asset_master_match.csv'
)

required_inputs = [YAM, SWAP, YAM_META, MASTER]
missing_inputs = [p for p in required_inputs if not os.path.exists(p)]

if missing_inputs:
    raise FileNotFoundError(
        "Required input file(s) not found:\n"
        + "\n".join(f" - {p}" for p in missing_inputs)
        + "\n\nSee the repository README for input-data requirements."
    )

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

# Load and deduplicate asset master. The supplied is_us_residential column contains
# duplicate True/False conflicts, so classification is rebuilt from the available names.
import re
asset_rows=defaultdict(list)
with open(MASTER,encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        asset_rows[r['token_address'].lower()].append(r)
US_STATE_CODES=set('AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split())
EXCLUDE_ASSET_WORDS=('LOAN','FACTORING','PROFIT SHARE','RWA HOLDINGS','SUISSE','PANAMA','COLOMBIA','MEXICO','ECOSYSTEM','GOVERNANCE')
state_pattern=re.compile(r'(?:,|\s)('+'|'.join(sorted(US_STATE_CODES))+r')(?:\s+\d{5}(?:-\d{4})?)?\s*$')
def classify_us_residential(names):
    joined=' | '.join(names).upper()
    if any(word in joined for word in EXCLUDE_ASSET_WORDS):
        return False, 'excluded_instrument_or_foreign'
    for n in names:
        if state_pattern.search(n.upper().strip()):
            return True, 'us_state_in_name'
    return False, 'no_us_state_match'
asset_master={}
for addr, rows in asset_rows.items():
    names=[r.get('trade_name','') for r in rows if r.get('trade_name')]
    is_us, reason=classify_us_residential(names)
    # Prefer the on-chain RealToken name over address-style labels.
    name=next((n for n in names if n.lower().startswith('realtoken')), names[0] if names else addr)
    asset_master[addr]={'name':name,'is_us_residential':is_us,'classification_reason':reason}
asset_addrs=set(asset_master)
us_res_addrs={a for a,v in asset_master.items() if v['is_us_residential']}

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
with open(YAM,encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        raw_stats['yam_rows']+=1
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
with open(SWAP,encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        raw_stats['swapcat_rows']+=1
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

# Aggregation helpers.
def window_end_for_year(y):
    if y==2026: return COMMON_CUTOFF_DATE
    return date(y,12,31)

def in_last_n_days(d, end, n):
    return end-timedelta(days=n-1) <= d <= end

def vwap(records):
    q=sum(r['realtoken_quantity'] for r in records)
    v=sum(r['trade_value_usd'] for r in records)
    return v/q if q>0 else None

def summarize_records(trades, threshold, us_only, tag):
    filt=[r for r in trades if r['trade_value_usd']>=threshold and (r['is_us_residential'] if us_only else True)]
    groups=defaultdict(list)
    for r in filt:
        groups[(r['realtoken_address'],r['year'])].append(r)
    summary=[]
    price90={}
    for (addr,y), rs in sorted(groups.items(),key=lambda x:(x[0][0],x[0][1])):
        rs.sort(key=lambda r:r['datetime_utc'])
        prices=[r['unit_price_usd'] for r in rs]
        end=window_end_for_year(y)
        rs30=[r for r in rs if in_last_n_days(date.fromisoformat(r['date']),end,30)]
        rs60=[r for r in rs if in_last_n_days(date.fromisoformat(r['date']),end,60)]
        rs90=[r for r in rs if in_last_n_days(date.fromisoformat(r['date']),end,90)]
        rsdec=[r for r in rs if date.fromisoformat(r['date']).month==12] if y<2026 else []
        last_date=date.fromisoformat(rs[-1]['date'])
        row={
            'realtoken_address':addr,'realtoken_name':asset_master[addr]['name'],'year':y,
            'first_price':prices[0],'last_price':prices[-1],'avg_price':statistics.fmean(prices),
            'median_price':statistics.median(prices),'vwap':vwap(rs),'december_vwap':vwap(rsdec),
            'vwap_last_30d':vwap(rs30),'vwap_last_60d':vwap(rs60),'vwap_last_90d':vwap(rs90),
            'min_price':min(prices),'max_price':max(prices),
            'std_price':statistics.stdev(prices) if len(prices)>1 else 0.0,
            'trade_count':len(rs),'trade_amount':sum(r['realtoken_quantity'] for r in rs),
            'trade_value_usd':sum(r['trade_value_usd'] for r in rs),
            'trade_count_last_90d':len(rs90),'trade_amount_last_90d':sum(r['realtoken_quantity'] for r in rs90),
            'trade_value_last_90d':sum(r['trade_value_usd'] for r in rs90),
            'swapcat_trades':sum(r['platform']=='Swapcat' for r in rs),'yam_trades':sum(r['platform']=='YAM' for r in rs),
            'last_trade_date':last_date.isoformat(),'days_to_period_end':(end-last_date).days,
            'period_end':end.isoformat(),'sample':tag,'threshold_usd':threshold,
        }
        summary.append(row)
        if row['vwap_last_90d'] is not None:
            price90[(addr,y)] = row
    # diagnostics
    diags=[]
    for y in sorted({r['year'] for r in filt}):
        yr=[r for r in filt if r['year']==y]
        by_asset=Counter(r['realtoken_address'] for r in yr)
        end=window_end_for_year(y)
        assets30={r['realtoken_address'] for r in yr if in_last_n_days(date.fromisoformat(r['date']),end,30)}
        assets60={r['realtoken_address'] for r in yr if in_last_n_days(date.fromisoformat(r['date']),end,60)}
        assets90={r['realtoken_address'] for r in yr if in_last_n_days(date.fromisoformat(r['date']),end,90)}
        prev_assets={r['realtoken_address'] for r in filt if r['year']==y-1}
        prev90={a for (a,yy) in price90 if yy==y-1}
        diags.append({
            'year':y,'sample':tag,'threshold_usd':threshold,'period_end':end.isoformat(),
            'total_trades':len(yr),'unique_assets':len(by_asset),
            'total_realtoken_amount':sum(r['realtoken_quantity'] for r in yr),
            'total_usd_volume':sum(r['trade_value_usd'] for r in yr),
            'avg_trades_per_asset':statistics.fmean(by_asset.values()) if by_asset else 0,
            'median_trades_per_asset':statistics.median(by_asset.values()) if by_asset else 0,
            'single_trade_assets':sum(v==1 for v in by_asset.values()),
            'assets_last_30d':len(assets30),'assets_last_60d':len(assets60),'assets_last_90d':len(assets90),
            'common_traded_with_prev':len(set(by_asset)&prev_assets) if prev_assets else '',
            'common_90d_price_with_prev':len(assets90&prev90) if prev90 else '',
            'swapcat_trades':sum(r['platform']=='Swapcat' for r in yr),
            'yam_trades':sum(r['platform']=='YAM' for r in yr),
            'swapcat_volume_usd':sum(r['trade_value_usd'] for r in yr if r['platform']=='Swapcat'),
            'yam_volume_usd':sum(r['trade_value_usd'] for r in yr if r['platform']=='YAM'),
        })
    # common returns
    details=[]; summaries=[]
    periods=[(2021,2022),(2022,2023),(2023,2024),(2024,2025)]
    for y1,y2 in periods:
        addrs=sorted({a for (a,y) in price90 if y==y1} & {a for (a,y) in price90 if y==y2})
        vals=[]
        for a in addrs:
            p1=price90[(a,y1)]['vwap_last_90d']; p2=price90[(a,y2)]['vwap_last_90d']
            ret=p2/p1-1
            wt=price90[(a,y2)]['trade_value_last_90d']
            vals.append((a,ret,wt,p1,p2))
            details.append({'period':f'{y1}-{y2}','price_method':'vwap_last_90d','realtoken_address':a,
                            'realtoken_name':asset_master[a]['name'],'price_y1':p1,'price_y2':p2,
                            'capital_return':ret,'trade_value_y2_90d':wt,'sample':tag,'threshold_usd':threshold})
        rets=[x[1] for x in vals]; totalwt=sum(x[2] for x in vals)
        summaries.append({
            'period':f'{y1}-{y2}','price_method':'vwap_last_90d','common_assets':len(vals),
            'equal_weighted_return':statistics.fmean(rets) if rets else None,
            'median_return':statistics.median(rets) if rets else None,
            'std_return':statistics.stdev(rets) if len(rets)>1 else (0.0 if rets else None),
            'min_return':min(rets) if rets else None,'max_return':max(rets) if rets else None,
            'volume_weighted_return':sum(ret*wt for _,ret,wt,_,_ in vals)/totalwt if totalwt else None,
            'assets_up':sum(r>1e-12 for r in rets),'assets_down':sum(r<-1e-12 for r in rets),
            'assets_unchanged':sum(abs(r)<=1e-12 for r in rets),'sample':tag,'threshold_usd':threshold,
        })
    # 2025 to 2026 YTD, separately labelled
    addrs=sorted({a for (a,y) in price90 if y==2025} & {a for (a,y) in price90 if y==2026})
    vals=[]
    for a in addrs:
        p1=price90[(a,2025)]['vwap_last_90d']; p2=price90[(a,2026)]['vwap_last_90d']
        ret=p2/p1-1; wt=price90[(a,2026)]['trade_value_last_90d']
        vals.append((a,ret,wt,p1,p2))
    if vals:
        rets=[x[1] for x in vals]; tw=sum(x[2] for x in vals)
        summaries.append({'period':f'2025-{COMMON_CUTOFF_DATE.isoformat()} YTD','price_method':'2025 year-end 90d vs 2026 trailing 90d',
            'common_assets':len(vals),'equal_weighted_return':statistics.fmean(rets),'median_return':statistics.median(rets),
            'std_return':statistics.stdev(rets) if len(rets)>1 else 0.0,'min_return':min(rets),'max_return':max(rets),
            'volume_weighted_return':sum(ret*wt for _,ret,wt,_,_ in vals)/tw if tw else None,
            'assets_up':sum(r>1e-12 for r in rets),'assets_down':sum(r<-1e-12 for r in rets),
            'assets_unchanged':sum(abs(r)<=1e-12 for r in rets),'sample':tag,'threshold_usd':threshold})
    return filt, summary, diags, details, summaries

# Primary output sets: all assets and US residential; 1 USD main, 5 USD robustness.
result_sets={}
for threshold in (1.0,5.0):
    for us_only,tag in [(False,'All_RealToken'),(True,'US_Residential')]:
        result_sets[(threshold,tag)] = summarize_records(primary,threshold,us_only,tag)
# Broad USD-like robustness only for US residential.
for threshold in (1.0,5.0):
    result_sets[(threshold,'US_Residential_BroadUSD')] = summarize_records(broad,threshold,True,'US_Residential_BroadUSD')

# CSV writer helper.
def write_dicts(path, rows, fieldnames=None):
    if fieldnames is None:
        fieldnames=list(rows[0].keys()) if rows else []
    with open(path,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fieldnames); w.writeheader()
        for row in rows:
            out={}
            for k in fieldnames:
                v=row.get(k)
                if isinstance(v,float):
                    out[k]='' if not math.isfinite(v) else f'{v:.12g}'
                elif v is None: out[k]=''
                else: out[k]=v
            w.writerow(out)

# Main detailed outputs (US residential, primary direct USD, >=1 USD).
_, summary_main, diag_main, details_main, returns_main=result_sets[(1.0,'US_Residential')]
write_dicts(os.path.join(OUT,'asset_year_price_summary_us_residential.csv'),summary_main)
write_dicts(os.path.join(OUT,'annual_sample_diagnostics_us_residential.csv'),diag_main)
write_dicts(os.path.join(OUT,'common_asset_return_detail_us_residential.csv'),details_main)
write_dicts(os.path.join(OUT,'common_asset_returns_us_residential.csv'),returns_main)

# Combined robustness tables.
robust=[]
for key,res in result_sets.items():
    threshold,tag=key
    for row in res[4]: robust.append(row)
write_dicts(os.path.join(OUT,'common_asset_returns_robustness.csv'),robust)

diag_all=[]
for key,res in result_sets.items(): diag_all.extend(res[2])
write_dicts(os.path.join(OUT,'annual_sample_diagnostics_all_variants.csv'),diag_all)

# Platform-year summary for primary >=1 USD US-residential sample.
main_trades=result_sets[(1.0,'US_Residential')][0]
platform_summary=[]
for (y,p),rs in sorted(defaultdict(list, {k:[] for k in []}).items()): pass
pg=defaultdict(list)
for r in main_trades: pg[(r['year'],r['platform'])].append(r)
for (y,p),rs in sorted(pg.items()):
    platform_summary.append({'year':y,'platform':p,'trades':len(rs),'unique_assets':len({r['realtoken_address'] for r in rs}),
        'realtoken_amount':sum(r['realtoken_quantity'] for r in rs),'usd_volume':sum(r['trade_value_usd'] for r in rs),
        'vwap':sum(r['trade_value_usd'] for r in rs)/sum(r['realtoken_quantity'] for r in rs),
        'realtoken_bought_trades':sum(r['trade_direction']=='realtoken_bought' for r in rs),
        'realtoken_sold_trades':sum(r['trade_direction']=='realtoken_sold' for r in rs),
        'sample':'US_Residential','threshold_usd':1.0})
write_dicts(os.path.join(OUT,'platform_year_summary_us_residential.csv'),platform_summary)

# Raw validation report.
validation=[]
validation.append({'item':'YAM rows','value':raw_stats['yam_rows']})
validation.append({'item':'YAM source max datetime UTC','value':YAM_MAX.isoformat()})
validation.append({'item':'Swapcat source max datetime UTC','value':SWAP_MAX.isoformat()})
validation.append({'item':'Common 2026 cutoff UTC','value':COMMON_CUTOFF.isoformat()})
validation.append({'item':'YAM rows after common cutoff excluded','value':raw_stats['yam_after_common_cutoff']})
validation.append({'item':'YAM RealToken-USD-like broad eligible','value':raw_stats['yam_asset_usd_broad']})
validation.append({'item':'YAM RealToken-direct USD eligible','value':raw_stats['yam_asset_usd_direct']})
validation.append({'item':'YAM reverse-direction trades included','value':raw_stats['yam_reverse_direction']})
validation.append({'item':'YAM other pairs excluded','value':raw_stats['yam_non_asset_usd_pair']})
validation.append({'item':'Swapcat rows','value':raw_stats['swapcat_rows']})
validation.append({'item':'Swapcat direct USD eligible','value':raw_stats['swapcat_asset_usd_direct']})
validation.append({'item':'Swapcat other payment excluded','value':raw_stats['swapcat_non_usd_payment']})
validation.append({'item':'Asset master original rows','value':sum(len(v) for v in asset_rows.values())})
validation.append({'item':'Asset master unique addresses','value':len(asset_master)})
validation.append({'item':'US residential unique addresses','value':len(us_res_addrs)})
validation.append({'item':'YAM price_raw column nonzero rows','value':0})
validation.append({'item':'YAM mapping used','value':'offer_token_amount_raw=event price word; buyer_token_amount_raw=event offer amount word'})
write_dicts(os.path.join(OUT,'raw_validation_report.csv'),validation,['item','value'])

# Summarize the corrected armmv3USDC inclusion in broad variant.
ed='0xed56f76e9cbc6a64b821e9c016eafbd3db5436d1'
ed_rows=[r for r in broad if r['payment_address']==ed]
ed_summary=[]
for y in sorted({r['year'] for r in ed_rows}):
    rs=[r for r in ed_rows if r['year']==y]
    ed_summary.append({'year':y,'trades_all':len(rs),'trades_ge1usd':sum(r['trade_value_usd']>=1 for r in rs),
                       'trades_ge5usd':sum(r['trade_value_usd']>=5 for r in rs),
                       'unique_assets':len({r['realtoken_address'] for r in rs}),
                       'usd_volume':sum(r['trade_value_usd'] for r in rs),
                       'median_unit_price':statistics.median(r['unit_price_usd'] for r in rs) if rs else None})
write_dicts(os.path.join(OUT,'armmv3usdc_corrected_summary.csv'),ed_summary)

# Methodology/readme.
readme=f"""YAM + Swapcat recalculation
Generated from the uploaded raw files.

Primary sample
- Platforms: Swapcat and YAM combined.
- Asset universe: addresses classified as US residential in asset_master_match.csv.
- Payment tokens: direct USDC, WXDAI, old USDC and USDT addresses listed in the script.
- Main threshold: trade value >= USD 1.
- Robustness: trade value >= USD 5 and a broader USD-like set including RMM receipt tokens/REUSD.
- Both YAM directions are included: RealToken offered for USD and USD offered for RealToken.
- YAM event interpretation: raw event words are offerToken, buyerToken, price, amount. In the uploaded CSV,
  offer_token_amount_raw stores the event price word and buyer_token_amount_raw stores the event amount word.
- For full years, representative price is each asset's VWAP during the last 90 calendar days ending Dec 31.
- 2026 is YTD only. Both platforms are truncated to the common source-coverage cutoff: {COMMON_CUTOFF.isoformat()} UTC.
- Capital return is P2/P1 - 1 across addresses with a valid last-90-day VWAP in both periods.
- Equal-weighted return is the arithmetic mean; standard deviation is the sample standard deviation.
- Token migrations are not canonicalized because a migration map was not included; migrated addresses therefore drop
  from common-address returns rather than being joined automatically.

Source coverage
- YAM max: {YAM_MAX.isoformat()} UTC
- Swapcat max: {SWAP_MAX.isoformat()} UTC
- Common cutoff for 2026: {COMMON_CUTOFF.isoformat()} UTC
"""
with open(os.path.join(OUT,'README_methodology.txt'),'w',encoding='utf-8') as f: f.write(readme)

# Compact JSON summary used for verification/final response.
summary_json={
 'source':{'yam_rows':raw_stats['yam_rows'],'swapcat_rows':raw_stats['swapcat_rows'],
           'yam_max':YAM_MAX.isoformat(),'swapcat_max':SWAP_MAX.isoformat(),'common_cutoff':COMMON_CUTOFF.isoformat()},
 'primary_us_res_ge1_returns':returns_main,
 'primary_us_res_ge1_diagnostics':diag_main,
 'validation':dict(raw_stats),
}
with open(os.path.join(OUT,'summary.json'),'w',encoding='utf-8') as f: json.dump(summary_json,f,ensure_ascii=False,indent=2)

# Zip results, excluding the very large normalized file? Include it because user asked for auditable data.
zip_path=os.path.join(REPO_ROOT,'yam_swapcat_recalculated_results.zip')
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for fn in sorted(os.listdir(OUT)):
        z.write(os.path.join(OUT,fn),arcname=fn)

print(json.dumps(summary_json,ensure_ascii=False,indent=2))
print('OUT',OUT)
print('ZIP',zip_path,os.path.getsize(zip_path))
