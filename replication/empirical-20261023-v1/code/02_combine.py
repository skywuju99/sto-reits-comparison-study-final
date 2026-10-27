"""Rebuild combined proxies: exclude Marloes in all years; restore verified 2023 S/D cases.

Run from the conversation workspace. Inputs are read only; prior outputs are preserved.
Returns are proxies using recorded annualized income, never actual paid annual dividends.
"""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal
import csv, hashlib, json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'intermediate'
CHECK = ROOT / 'inputs'
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
HISTORY = ROOT/'inputs/tokenHistory.json'
META = ROOT/'inputs/token_metadata_20260410.json'
EVENTS = ROOT/'inputs/mint_burn.csv'
TRADES = BASE/'normalized_trades_primary.csv'
MAP = ROOT/'inputs/sd_mapping_2023.csv'
MAR = '0x7524d382373c1a091789978a8b2c1dc707d2b213'
JEF = '0xa29ae272bc89e5f315b2793925f700045f845d82'
sources = [HISTORY, META, EVENTS, TRADES, MAP]
hist = {x['uuid'].lower(): sorted(x['history'], key=lambda e: str(e['date']))
        for x in json.loads(HISTORY.read_text(encoding='utf-8-sig'))}
meta = {x['uuid'].lower(): x for x in json.loads(META.read_text(encoding='utf-8-sig'))}

def state(a, year):
    values, dates = {}, {}
    for e in hist[a]:
        if str(e['date']) > f'{year}1231':
            break
        values.update(e['values'])
        dates.update({k: str(e['date']) for k in e['values']})
    return values, dates

events = defaultdict(list)
seen = set()
for r in csv.DictReader(EVENTS.open(encoding='utf-8-sig')):
    a = r['token_address'].lower()
    key = a, r['transaction_hash'], r['log_index']
    if key in seen:
        continue
    seen.add(key)
    n = Decimal(r['amount_raw']) / Decimal(10) ** int(r['token_decimals'])
    events[a].append((r['datetime_utc'], n if r['event_type'] == 'mint' else -n))

def supply(a, next_year):
    return sum((n for t, n in events[a] if t < f'{next_year}-01-01'), Decimal(0))

mapping = pd.read_csv(MAP).set_index('address')
assert len(mapping) == 12 and mapping.index.is_unique
T = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
Z = '0x' + '0' * 64
sd_rows = []
for a, r in mapping.iterrows():
    d = r.d_address
    pages = sorted((CHECK / 'regd_logs').glob(f'regd_v2_{d}_*.json'))
    assert pages
    ds, dedup = [], set()
    for page in pages:
        sources.append(page)
        blob = json.loads(page.read_text(encoding='utf-8'))
        for e in blob['items']:
            if e['topics'][0] != T:
                continue
            key = e['block_number'], e['index']
            if key in dedup:
                continue
            dedup.add(key)
            sign = 1 if e['topics'][1] == Z else -1 if e['topics'][2] == Z else 0
            if sign:
                ds.append((e['block_timestamp'], Decimal(int(e['data'], 16)) / Decimal(10) ** 18 * sign))
    assert any(json.loads(p.read_text(encoding='utf-8'))['next_page_params'] is None for p in pages)
    d0 = sum((n for t, n in ds if t < '2023-01-01'), Decimal(0))
    d1 = sum((n for t, n in ds if t < '2024-01-01'), Decimal(0))
    n0, n1 = supply(a, 2023) + d0, supply(a, 2024) + d1
    s0, _ = state(a, 2022)
    dd0, _ = state(d, 2022)
    assert s0['netRentYear'] == dd0['netRentYear']
    assert s0['totalInvestment'] == dd0['totalInvestment']
    assert n0 == n1 and n0 > 0 and d1 == 0
    assert abs(float(s0['totalInvestment']) / float(n0) - float(s0['tokenPrice'])) <= .005 + 1e-12
    assert np.isclose(float(n0), r.s_d_sum_0)
    sd_rows.append(dict(address=a, d_address=d, name=meta[a]['fullName'],
                        s_quantity_0=float(supply(a, 2023)), d_quantity_0=float(d0),
                        combined_quantity_0=float(n0), s_quantity_1=float(supply(a, 2024)),
                        d_quantity_1=float(d1), combined_quantity_1=float(n1)))
sd = pd.DataFrame(sd_rows).set_index('address')

# Rebuild 90-day VWAP from the preserved normalized trade-level file.
t = pd.read_csv(TRADES, low_memory=False)
t['date'] = pd.to_datetime(t.date)
t = t[t.is_us_residential.astype(str).str.lower().eq('true') & t.trade_value_usd.ge(1) & t.realtoken_quantity.gt(0)].copy()
# The inherited flag is an inclusion flag, not newly verified property-use evidence.
t['address'] = t.realtoken_address.str.lower()
windows = {}
for y in range(2021, 2026):
    end = pd.Timestamp(f'{y}-12-31')
    q = t[t.date.between(end - pd.Timedelta(days=89), end)]
    q = q.groupby('address').agg(value=('trade_value_usd', 'sum'), quantity=('realtoken_quantity', 'sum'))
    q['price'] = q.value / q.quantity
    windows[y] = q

def metrics(g):
    w = g.investment_0 / g.investment_0.sum()
    inc = g.rent_1 / g.income_quantity / g.price_0
    cap = g.price_1 / g.price_0 - 1
    res = dict(n=len(g), income_pct=float((w*inc).sum()*100), capital_pct=float((w*cap).sum()*100),
               combined_pct=float((w*(inc+cap)).sum()*100),
               platform_income_pct=float(g.rent_1.sum()/g.investment_0.sum()*100),
               weight_sum=float(w.sum()), investment_total=float(g.investment_0.sum()))
    assert abs(res['combined_pct'] - res['income_pct'] - res['capital_pct']) < 1e-11
    # Independent Decimal sum using the same unrounded source fields.
    den = sum(Decimal(str(z)) for z in g.investment_0)
    independent = sum(Decimal(str(r.investment_0)) *
                      (Decimal(str(r.rent_1))/Decimal(str(r.income_quantity))/Decimal(str(r.price_0))
                       + Decimal(str(r.price_1))/Decimal(str(r.price_0))-1)
                      for r in g.itertuples())/den*100
    assert abs(float(independent)-res['combined_pct']) < 1e-10
    return res

old_expected = [(44,13.783678535), (93,8.261677499), (348,20.426595786), (382,-6.694425022)]
annual, details, changes, prices, groups = [], [], [], [], {}
for y in range(2022,2026):
    pair = windows[y-1].join(windows[y], how='inner', lsuffix='_0', rsuffix='_1')
    rows = []
    for a, p in pair.iterrows():
        if a not in hist:
            continue
        s0, d0 = state(a,y-1); s1,d1 = state(a,y)
        row = dict(address=a,year=y,name=meta.get(a,{}).get('fullName',''),
                   investment_0=s0.get('totalInvestment'),investment_1=s1.get('totalInvestment'),
                   rent_0=s0.get('netRentYear'),rent_1=s1.get('netRentYear'),
                   display_0=s0.get('tokenPrice'),income_record_date=d1.get('netRentYear'),
                   quantity_0=float(supply(a,y)),quantity_1=float(supply(a,y+1)),
                   price_0=p.price_0,price_1=p.price_1,value_1=p.value_1)
        rows.append(row)
    g = pd.DataFrame(rows).set_index('address')
    valid = g.investment_0.gt(0)&g.investment_1.gt(0)&g.rent_0.notna()&g.rent_1.notna()&g.quantity_0.gt(0)
    eligible = valid & (g.investment_0/g.quantity_0-g.display_0).abs().le(.005+1e-12)
    old = g[eligible].copy(); old['income_quantity']=old.quantity_0
    previous = metrics(old)
    exn, exvalue = old_expected[y-2022]
    assert len(old)==exn and abs(previous['combined_pct']-exvalue)<1e-8
    oldids = set(old.index)
    assert set(old.index)==oldids
    new = old.copy(); new['quantity_basis']='기존 순발행량'; new['d_address']=''
    if y==2023:
        assert not set(sd.index)&set(old.index)
        assert set(sd.index)<=set(g.index)
        add = g.loc[sd.index].copy()
        assert valid.loc[add.index].all()
        add['income_quantity']=sd.combined_quantity_1
        add['quantity_basis']='확인된 S형·D형 합산 수량'
        add['d_address']=sd.d_address
        new=pd.concat([new,add])
    if MAR in new.index:
        new=new.drop(MAR)
    assert new.index.is_unique and MAR not in new.index
    new=new.sort_index()
    result=metrics(new)
    new['weight']=new.investment_0/new.investment_0.sum()
    new['income_proxy']=new.rent_1/new.income_quantity/new.price_0
    new['capital_change']=new.price_1/new.price_0-1
    new['combined_proxy']=new.income_proxy+new.capital_change
    new['weighted_income']=new.weight*new.income_proxy
    new['weighted_capital']=new.weight*new.capital_change
    new['weighted_combined']=new.weight*new.combined_proxy
    details.append(new.reset_index()); groups[y]=new
    annual.append(dict(year=y,**result,reit_total_return_pct={2022:-31.34,2023:7.66,2024:12.83,2025:-7.43}[y]))
    changes.append(dict(year=y,old_n=previous['n'],new_n=result['n'],
                        added_addresses=sorted(set(new.index)-oldids),removed_addresses=sorted(oldids-set(new.index)),
                        old_combined_pct=previous['combined_pct'],new_combined_pct=result['combined_pct']))
    change=pair.price_1/pair.price_0-1
    prices.append(dict(year=y,n=len(pair),weighted_price_change_pct=float(np.average(change,weights=pair.value_1)*100)))

assert [r['n'] for r in annual] == [44,105,347,381]
assert [r['n'] for r in prices] == [44,105,348,382]
assert [round(r['weighted_price_change_pct'],2) for r in prices] == [.95,2.07,10.11,-15.15]
sensitivity = {'2025_without_Marloes':metrics(groups[2025]),
               '2025_without_Marloes_and_Jefferson':metrics(groups[2025].drop(JEF))}
pd.concat(details,ignore_index=True).to_csv(OUT/'combined_asset_details_2022_2025.csv',index=False,encoding='utf-8-sig',lineterminator='\r\n')
sd.reset_index().to_csv(OUT/'2023_S_D_quantity_reconciliation.csv',index=False,encoding='utf-8-sig',lineterminator='\r\n')
table=pd.DataFrame(annual)
table[['year','n','income_pct','capital_pct','combined_pct','reit_total_return_pct']].rename(columns={
    'year':'연도','n':'결합표본 수','income_pct':'시장가격 기준 임대수익률 근사치(%)',
    'capital_pct':'가격변화율(%)','combined_pct':'시장가격 기준 수익률 근사치(%)',
    'reit_total_return_pct':'미국 주거용 리츠 총수익률(%)'}).to_csv(OUT/'연도별_수익률근사치_재계산.csv',index=False,encoding='utf-8-sig',lineterminator='\r\n')
report=dict(scope='Marloes excluded in all combined-analysis years; verified twelve S/D cases restored in 2023. Price-only population unchanged.',
            annual=annual,changes=changes,price_only=prices,sensitivity=sensitivity,
            checks='Original four annual results reproduced before changes; S/D quantities rebuilt from cached raw logs; revised sums checked independently with Decimal.',
            source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            limitations='These calculations do not establish actual paid annual rent, remove carried-forward income uncertainty, or complete all professor feedback. S/D cases count each underlying income record once; D-class prices are not merged into S-class prices.')
(OUT/'recalculation_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['annual','changes','price_only','sensitivity','checks']},ensure_ascii=False,indent=2))
