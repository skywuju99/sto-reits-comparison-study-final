"""Annual activity, population intersections, window sensitivity and income provenance.
Historical-address universe is not a listing/actively tradable population.
"""
from pathlib import Path
from collections import defaultdict
from decimal import Decimal as D
import csv,json,hashlib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
def save(df,name): df.to_csv(OUT/name,index=False,encoding='utf-8-sig')
def frame(rows,name):
 df=pd.DataFrame(rows);save(df,name);return df
def pct(n,d):return n/d*100 if d else None
norm=pd.read_csv(ROOT/'intermediate/normalized_trades_primary.csv',low_memory=False)
norm['time']=pd.to_datetime(norm.datetime_utc,utc=True)
cut=pd.Timestamp('2026-07-06T20:28:20Z')
assert norm.time.max()<=cut
t=norm[norm.is_us_residential.astype(str).str.lower().eq('true') & norm.trade_value_usd.ge(1) & norm.realtoken_quantity.gt(0)].copy()
t['address']=t.realtoken_address.str.lower();t['day']=t.time.dt.floor('D');t['year']=t.time.dt.year
master=pd.read_csv(ROOT/'intermediate/asset_master_clean.csv')
master=master[master.is_us_residential.astype(str).str.lower().eq('true')].copy()
master['address']=master.token_address.str.lower();assert master.address.nunique()==404
universe=set(master.address);assert set(t.address)<=universe
names=master.set_index('address').realtoken_name.to_dict()
h=json.loads((ROOT/'inputs/tokenHistory.json').read_text(encoding='utf-8-sig'))
hist={a['uuid'].lower():sorted(a['history'],key=lambda e:str(e['date'])) for a in h}
meta={a['uuid'].lower():a for a in json.loads((ROOT/'inputs/token_metadata_20260410.json').read_text(encoding='utf-8-sig'))}
def state(a,y):
 s={};dt={}
 for e in hist.get(a,[]):
  if str(e['date'])>f'{y}1231':break
  s.update(e['values']);dt.update({k:str(e['date']) for k in e['values']})
 return s,dt
es=defaultdict(list);seen=set()
for r in csv.DictReader((ROOT/'inputs/mint_burn.csv').open(encoding='utf-8-sig')):
 a=r['token_address'].lower();key=a,r['transaction_hash'],r['log_index']
 if key in seen:continue
 seen.add(key);n=D(r['amount_raw'])/(D(10)**int(r['token_decimals']))
 es[a].append((pd.Timestamp(r['datetime_utc'],tz='UTC'),n if r['event_type']=='mint' else -n,r['event_type']))
for a in es:es[a].sort()
def qty(a,end):return sum((n for ts,n,_ in es[a] if ts<=end),D(0))
def end(y):return cut if y==2026 else pd.Timestamp(f'{y}-12-31T23:59:59Z')
first={};first_src={}
for a in universe:
 dates=[]
 if hist.get(a):dates.append((pd.to_datetime(str(hist[a][0]['date']),format='%Y%m%d',utc=True),'platform_history'))
 if es[a]:dates.append((min(e[0] for e in es[a]),'mint_burn'))
 ar=t.loc[t.address.eq(a),'time']
 if len(ar):dates.append((ar.min(),'eligible_trade'))
 if dates:first[a],first_src[a]=min(dates)
 else:first[a],first_src[a]=pd.NaT,'unobserved'
frame([dict(address=a,name=names[a],first_record_utc=first[a],first_record_source=first_src[a]) for a in sorted(universe)],'historical_address_universe.csv')

# Platform states are separately counted; not the top rung of a market funnel.
platform_sets={};platform_counts=[];state_rows=[]
for y in range(2021,2026):
 valid=set()
 for a in hist:
  s,dt=state(a,y)
  ok=s.get('totalInvestment') is not None and s['totalInvestment']>0 and s.get('netRentYear') is not None
  if ok:valid.add(a)
  if s:state_rows.append(dict(address=a,year=y,valid=ok,totalInvestment=s.get('totalInvestment'),netRentYear=s.get('netRentYear'),tokenPrice=s.get('tokenPrice'),rent_record_date=dt.get('netRentYear'),investment_record_date=dt.get('totalInvestment'),price_record_date=dt.get('tokenPrice')))
 platform_sets[y]=valid;platform_counts.append(dict(year=y,platform_valid_n=len(valid)))
assert [r['platform_valid_n'] for r in platform_counts]==[208,319,463,689,825]
frame(platform_counts,'table_4_2_platform_counts.csv');frame(state_rows,'platform_year_end_states.csv')

windows={};pairs={};price_rows=[];window_detail=[]
for y in range(2021,2027):
 for d in (30,90,180):
  start=end(y).floor('D')-pd.Timedelta(days=d-1)
  z=t[t.time.between(start,end(y))]
  g=z.groupby('address').agg(value=('trade_value_usd','sum'),quantity=('realtoken_quantity','sum'),trades=('time','size'))
  g['price']=g.value/g.quantity;windows[y,d]=g
  for a,r in g.iterrows():window_detail.append(dict(year=y,window_days=d,start_utc=start,end_utc=end(y),address=a,**r.to_dict()))
  if y>=2022:
   p=windows[y-1,d].join(g,how='inner',lsuffix='_0',rsuffix='_1');p['change']=p.price_1/p.price_0-1;pairs[y,d]=p
   if d==90:price_rows.append(dict(year=y,n=len(p),mean_pct=p.change.mean()*100,median_pct=p.change.median()*100,weighted_pct=np.average(p.change,weights=p.value_1)*100,up_n=int(p.change.gt(0).sum()),down_n=int(p.change.lt(0).sum()),flat_n=int(p.change.eq(0).sum())))
frame(price_rows,'table_4_5_price_returns.csv');frame(window_detail,'asset_window_prices.csv')
sens=[];sens_detail=[]
for y in range(2022,2027):
 common=sorted(set.intersection(*(set(pairs[y,d].index) for d in (30,90,180))))
 for d in (30,90,180):
  allg=pairs[y,d];g=allg.loc[common];w=pairs[y,90].loc[common].value_1;w=w/w.sum()
  sens.append(dict(year=y,window_days=d,common_n=len(common),fixed_weight_change_pct=float((w*g.change).sum()*100),available_n=len(allg),available_weight_change_pct=float(np.average(allg.change,weights=allg.value_1)*100)))
  for a in common:sens_detail.append(dict(year=y,window_days=d,address=a,fixed_weight=w[a],price_0=g.loc[a,'price_0'],price_1=g.loc[a,'price_1'],change=g.loc[a,'change'],weighted_contribution_pp=w[a]*g.loc[a,'change']*100))
frame(sens,'table_4_7_fixed_sample_windows.csv');frame(sens_detail,'fixed_sample_window_details.csv')

activity=[];frequency=[];diag=[];members=[];sets=[]
combined=pd.read_csv(OUT/'combined_asset_details_2022_2025.csv')
for y in range(2021,2027):
 en=end(y);begin=pd.Timestamp(f'{y}-01-01',tz='UTC');z=t[t.time.between(begin,en)]
 known={a for a in universe if pd.notna(first[a]) and first[a]<=en}
 traded=set(z.address);last90=set(windows[y,90].index);prior=t[t.time.le(en)]
 assert traded<=known and last90<=known
 counts=z.groupby('address').size();last=prior.groupby('address').time.max()
 p90=windows[y,90].trades;days=z.groupby('address').day.nunique()
 active_freq=[];known_freq=[];age_ever=[];age_active=[];arows=[]
 for a in sorted(known):
  n=int(counts.get(a,0));last_t=last.get(a,pd.NaT)
  age=(en.floor('D')-last_t.floor('D')).days if pd.notna(last_t) else None
  known_freq.append(n)
  if n:active_freq.append(n);age_active.append(age)
  if age is not None:age_ever.append(age)
  row=dict(year=y,end_utc=en,address=a,name=names[a],year_trade_count=n,year_trade_days=int(days.get(a,0)),last_90d_trade_count=int(p90.get(a,0)),last_trade_utc=last_t,days_since_last_trade=age,year_no_trade=n==0,last90_no_trade=a not in last90,never_observed_trade=pd.isna(last_t),historical_first_record_utc=first[a])
  frequency.append(row);arows.append(row)
 ag=np.array(active_freq);eg=np.array(age_ever)
 diag.append(dict(year=y,end_utc=en,historically_observed_addresses=len(known),year_traded_n=len(traded),year_unobserved_n=len(known-traded),year_unobserved_pct=pct(len(known-traded),len(known)),last90_traded_n=len(last90),last90_unobserved_n=len(known-last90),last90_unobserved_pct=pct(len(known-last90),len(known)),trades_median_traded=float(np.median(ag)),trades_q25_traded=float(np.quantile(ag,.25)),trades_q75_traded=float(np.quantile(ag,.75)),trades_median_all_known=float(np.median(known_freq)),single_trade_addresses=int(sum(ag==1)),never_observed_trade_n=len(known)-len(eg),last_trade_age_median_ever=float(np.median(eg)),last_trade_age_p75_ever=float(np.quantile(eg,.75)),last_trade_age_median_year_traded=float(np.median(age_active)),last_trade_age_over90_ever_n=int(sum(eg>=90))))
 activity.append(dict(year=y,trades=len(z),traded_addresses=len(traded),value_usd=z.trade_value_usd.sum(),swapcat_trades=int(z.platform.eq('Swapcat').sum()),yam_trades=int(z.platform.eq('YAM').sum()),value_per_trade_usd=z.trade_value_usd.sum()/len(z)))
 if y<=2025:
  c=set(combined.loc[combined.year.eq(y),'address']);price=set(pairs[y,90].index) if y>=2022 else set()
  ps=platform_sets[y];p_prev=platform_sets.get(y-1,set())
  sets.append(dict(year=y,platform_valid_all=len(ps),classification_universe_all_dates=len(universe),historically_observed_classified_n=len(known),platform_valid_and_historical_classified_n=len(ps&known),platform_valid_outside_classified_n=len(ps-universe),year_traded_n=len(traded),last90_traded_n=len(last90),paired_prices_n=len(price) if y>=2022 else None,paired_prices_and_both_platform_valid_n=len(price&ps&p_prev) if y>=2022 else None,final_combined_n=len(c) if y>=2022 else None))
  for a in sorted(universe|ps):members.append(dict(year=y,address=a,platform_valid=a in ps,classified=a in universe,historically_observed=a in known,year_traded=a in traded,last90_price=a in last90,paired_prices=a in price,combined=a in c))
frame(activity,'table_4_4_trading_activity.csv');frame(diag,'trading_frequency_recency_summary.csv');frame(frequency,'asset_frequency_recency_details.csv');frame(sets,'table_4_3_population_intersections.csv');frame(members,'population_membership_details.csv')
assert activity[4]['trades']==46563 and activity[5]['trades']==11231
assert diag[4]['historically_observed_addresses']==404 and diag[4]['year_unobserved_n']==15 and diag[4]['last90_unobserved_n']==18

# Per-year inclusion and exclusion reasons, all 90-day price pairs.
exclusions=[];sd=pd.read_csv(OUT/'2023_S_D_quantity_reconciliation.csv').set_index('address')
for y in range(2022,2026):
 included=set(combined.loc[combined.year.eq(y),'address'])
 for a in pairs[y,90].index:
  s0,_=state(a,y-1);s1,_=state(a,y);n0=float(qty(a,end(y-1)))
  diff=abs(s0['totalInvestment']/n0-s0['tokenPrice']) if n0>0 and s0.get('totalInvestment') is not None and s0.get('tokenPrice') is not None else None
  reason='included'
  if a=='0x7524d382373c1a091789978a8b2c1dc707d2b213':reason='excluded_Marloes_income_scope_unconfirmed'
  elif y==2023 and a in sd.index:reason='included_after_S_D_quantity_reconciliation'
  elif a not in included:reason='excluded_platform_or_quantity_requirement'
  exclusions.append(dict(year=y,address=a,name=names.get(a,''),price_analysis_included=True,rental_combination_included=a in included,reason=reason,single_address_quantity=n0,single_address_V_over_N_price_difference=diff))
ex=frame(exclusions,'annual_inclusion_exclusion_details.csv')
save(ex.groupby(['year','reason']).size().rename('addresses').reset_index(),'annual_inclusion_exclusion_summary.csv')

# Income and quantity scope audit on the selected final combined sample.
rent_rows=[]
for r in combined.itertuples():
 a=r.address;y=r.year;start=end(y-1);en=end(y);s0,d0=state(a,y-1);s1,d1=state(a,y)
 md=meta.get(a,{});year_events=[e for e in es[a] if start<e[0]<=en]
 record_day=pd.to_datetime(str(d1['netRentYear']),format='%Y%m%d',utc=True)
 rent_rows.append(dict(year=y,address=a,name=r.name,currency_metadata=md.get('currency'),currency_metadata_source='token_metadata_20260410.json',income_field='netRentYear',income_value=s1.get('netRentYear'),income_record_date=d1.get('netRentYear'),income_record_age_days=(en.floor('D')-record_day).days,carried_from_prior_year=record_day.year<y,period_definition='annualized value in last recorded update; not actual calendar-year distributions',income_quantity=r.income_quantity,quantity_basis=r.quantity_basis,gnosis_quantity_start=r.quantity_0,gnosis_quantity_end=r.quantity_1,mint_events=len([e for e in year_events if e[2]=='mint']),burn_events=len([e for e in year_events if e[2]=='burn']),ethereum_contract=md.get('ethereumContract'),gnosis_contract=md.get('gnosisContract'),metadata_last_update=str(md.get('lastUpdate')),end_implied_quantity=s1.get('totalInvestment',np.nan)/s1.get('tokenPrice',np.nan) if s1.get('tokenPrice',0)>0 else np.nan))
rr=frame(rent_rows,'income_quantity_scope_details.csv')
rent_summary=[]
for y,g in rr.groupby('year'):
 rent_summary.append(dict(year=int(y),n=len(g),zero_income_n=int(g.income_value.eq(0).sum()),carried_income_n=int(g.carried_from_prior_year.sum()),currency_USD_n=int(g.currency_metadata.eq('USD').sum()),mint_or_burn_addresses_n=int((g.mint_events+g.burn_events).gt(0).sum()),record_age_days_median=g.income_record_age_days.median(),record_age_days_max=int(g.income_record_age_days.max())))
frame(rent_summary,'income_quantity_scope_summary.csv')

# Full-burn evidence is a chain supply observation, not proof of legal liquidation.
status=[]
for y in range(2022,2027):
 for a in sorted({a for a in universe if pd.notna(first[a]) and first[a]<=end(y)}):
  q0=qty(a,end(y-1));q1=qty(a,end(y));ye=[e for e in es[a] if end(y-1)<e[0]<=end(y)]
  n_mint=sum(e[2]=='mint' for e in ye);n_burn=sum(e[2]=='burn' for e in ye)
  st='positive_supply' if q1>D('0.00000001') else 'zero_or_dust_supply' if es[a] else 'no_supply_events_in_archive'
  last_a=t.loc[t.address.eq(a)&t.time.le(end(y)),'time']
  status.append(dict(year=y,address=a,name=names.get(a,''),quantity_start=str(q0),quantity_end=str(q1),mint_events=n_mint,burn_events=n_burn,end_supply_status=st,positive_start_to_zero_end=q0>D('0.00000001') and q1<=D('0.00000001'),price_pair_included=a in pairs[y,90].index,combined_included=bool(((combined.year==y)&(combined.address==a)).any()),last_eligible_trade_utc=last_a.max() if len(last_a) else None,ethereum_metadata=meta.get(a,{}).get('ethereumContract'),gnosis_metadata=meta.get(a,{}).get('gnosisContract'),cross_chain_transfer_confirmed='not_inferred_from_multiple_contract_fields',legal_redemption_status='not_determined_by_supply_alone'))
st=frame(status,'address_supply_status_all_years.csv')
save(st[st.positive_start_to_zero_end],'positive_to_zero_supply_cases.csv')

# Display comparison uses the latest tokenPrice from the preserved history,
# not a separately obtained current quote or each historical year end.
latest={a:state(a,2099)[0].get('tokenPrice') for a in hist}
display_rows=[];display_details=[]
for y in range(2021,2027):
 g=windows[y,90].copy();g['display']=g.index.map(latest)
 g=g[g.display.gt(0)]
 w=g.value/g.value.sum();rel=g.price/g.display-1
 display_rows.append(dict(year=y,n=len(g),market_price_value_weighted=float((w*g.price).sum()),display_price_value_weighted=float((w*g.display).sum()),relative_difference_pct=float((w*rel).sum()*100)))
 for a,r in g.iterrows():display_details.append(dict(year=y,address=a,price=r.price,display=r.display,weight=w[a],relative_difference_pct=rel[a]*100))
frame(display_rows,'table_4_8_display_comparison.csv');frame(display_details,'display_comparison_details.csv')
t['month']=t.time.dt.strftime('%Y-%m');monthly=[]
for mo,g in t.groupby('month'):
 monthly.append(dict(month=mo,vwap=g.trade_value_usd.sum()/g.realtoken_quantity.sum(),median_trade_price=g.unit_price_usd.median(),traded_addresses=g.address.nunique(),trades=len(g),value_usd=g.trade_value_usd.sum(),quantity=g.realtoken_quantity.sum()))
frame(monthly,'monthly_price_activity.csv')
selected=['2024-12','2025-06','2025-09','2025-12','2026-01','2026-02','2026-04','2026-06']
frame([r for r in monthly if r['month'] in selected],'table_4_9_monthly_selected.csv')

early_ids=set.intersection(*(set(pairs[2023,d].index) for d in (30,90,180)))
early=[]
for d in (30,90,180):
 g=windows[2022,d].loc[sorted(early_ids)]
 early.append(dict(analysis_year=2023,base_price_year=2022,window_days=d,n=len(g),trades=int(g.trades.sum()),trades_median=float(g.trades.median()),single_trade_n=int(g.trades.eq(1).sum())))
assert early[1]['trades']==371 and early[1]['single_trade_n']==37 and early[2]['trades']==3327
frame(early,'early_2023_base_price_trade_counts.csv')

validations={'price_n':[r['n'] for r in price_rows],'fixed_window_n':[next(r['common_n'] for r in sens if r['year']==y) for y in range(2022,2027)],'platform_counts':[r['platform_valid_n'] for r in platform_counts],'normalized_primary_n':len(norm),'eligible_trades':len(t),'cutoff':str(cut),'2025_frequency':diag[4],'2026_frequency':diag[5],'income_summary':rent_summary}
assert validations['price_n']==[44,105,348,382,283]
assert validations['fixed_window_n']==[32,103,310,315,154]
assert [round(r['fixed_weight_change_pct'],2) for r in sens if r['year']==2026]==[-79.77,-71.19,-63.58]
assert round(display_rows[-1]['relative_difference_pct'],1)==-72.5
(OUT/'diagnostic_validation.json').write_text(json.dumps(validations,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps(validations,ensure_ascii=False,indent=2,default=str))
