"""Independent csv/Decimal validation, input identity and table/file map."""
from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from statistics import median
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
checks=[]
for r in json.loads((ROOT/'inputs_manifest.json').read_text()):
 p=ROOT/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
checks.append('All input file hashes match the packaged manifest.')
groups=defaultdict(list)
for r in read(OUT/'combined_asset_details_2022_2025.csv'):groups[int(r['year'])].append(r)
expected=json.loads((OUT/'recalculation_manifest.json').read_text(encoding='utf-8'))
for result in expected['annual']:
 g=groups[result['year']];den=sum(D(r['investment_0']) for r in g)
 assert len(g)==result['n'] and len({r['address'] for r in g})==len(g)
 inc=sum(D(r['investment_0'])/den*D(r['rent_1'])/D(r['income_quantity'])/D(r['price_0']) for r in g)*100
 cap=sum(D(r['investment_0'])/den*(D(r['price_1'])/D(r['price_0'])-1) for r in g)*100
 assert abs(float(inc+cap)-result['combined_pct'])<1e-10
 checks.append(f"{result['year']}: N={len(g)}; independently summed income={inc:.10f}, price={cap:.10f}, combined={inc+cap:.10f}")
# Independent trade counters and last dates; source selection is identical by design.
year_trades=defaultdict(list);all_trade_dates=defaultdict(list)
for r in read(ROOT/'intermediate/normalized_trades_primary.csv'):
 if r['is_us_residential'].lower()!='true' or D(r['trade_value_usd'])<1 or D(r['realtoken_quantity'])<=0:continue
 dt=datetime.fromisoformat(r['datetime_utc']).replace(tzinfo=None)
 if dt>datetime(2026,7,6,20,28,20):raise AssertionError('after cutoff')
 year_trades[dt.year].append(r);all_trade_dates[r['realtoken_address'].lower()].append(dt)
first={r['address']:datetime.fromisoformat(r['first_record_utc']).replace(tzinfo=None) for r in read(OUT/'historical_address_universe.csv')}
activity={int(r['year']):r for r in read(OUT/'table_4_4_trading_activity.csv')}
for r in read(OUT/'trading_frequency_recency_summary.csv'):
 y=int(r['year']);en=datetime(2026,7,6,20,28,20) if y==2026 else datetime(y,12,31,23,59,59)
 known={a for a,dt in first.items() if dt<=en};counts=Counter(x['realtoken_address'].lower() for x in year_trades[y]);lasts=[];recent=set()
 for a in known:
  dates=[dt for dt in all_trade_dates[a] if dt<=en]
  if dates:
   last=max(dates);lasts.append((en.date()-last.date()).days)
   if last.date()>=en.date()-timedelta(days=89):recent.add(a)
 assert len(known-counts.keys())==int(r['year_unobserved_n'])
 assert len(known-recent)==int(r['last90_unobserved_n'])
 assert median(lasts)==float(r['last_trade_age_median_ever'])
 assert median(list(counts.values()))==float(r['trades_median_traded'])
 assert len(year_trades[y])==int(activity[y]['trades'])
 assert abs(float(sum(D(x['trade_value_usd']) for x in year_trades[y]))-float(activity[y]['value_usd']))<1e-6
 checks.append(f'{y}: activity, frequency, age and non-observation counts independently reproduced.')
for r in read(OUT/'table_4_7_fixed_sample_windows.csv'):
 y,d=int(r['year']),int(r['window_days'])
 rows=[z for z in read(OUT/'fixed_sample_window_details.csv') if int(z['year'])==y and int(z['window_days'])==d]
 assert len(rows)==int(r['common_n'])
 value=sum(D(z['fixed_weight'])*(D(z['price_1'])/D(z['price_0'])-1) for z in rows)*100
 assert abs(float(value)-float(r['fixed_weight_change_pct']))<1e-10
checks.append('All fifteen fixed-sample window results independently re-summed.')
tablemap=[
 ('표 4-2','table_4_2_platform_counts.csv','부분 갱신 이력을 누적한 연말 플랫폼 유효표본'),
 ('표 4-3','table_4_3_population_intersections.csv','집합별 개수 및 교집합; 하나의 탈락 흐름이 아님'),
 ('표 4-4','table_4_4_trading_activity.csv','미국 소재 선정 주소, 달러 연동 결제, 1달러 이상'),
 ('표 4-6','table_4_5_price_returns.csv','90일 양 시점 가격 공통표본; 기말 거래대금 가중'),
 ('표 4-7','연도별_수익률근사치_재계산.csv','Marloes 제외, 2023 S/D 수량 반영; 기초 총투자금 가중'),
 ('표 4-8','table_4_7_fixed_sample_windows.csv','30/90/180일 공통표본, 기말 90일 거래대금 가중 고정'),
 ('표 4-9','table_4_8_display_comparison.csv','보존된 표시가격과 시장가격 비교; 동시점 괴리 아님'),
 ('표 4-10','table_4_9_monthly_selected.csv','월별 전체 체결 VWAP; 고정구성 지수 아님'),
 ('표 4-5','trading_frequency_recency_summary.csv','연도 말까지 기록된 선정 주소 집합; 2026 부분연도'),
 ('그림 4-1','monthly_price_activity.csv','월별 관찰 거래가격; 월별 구성 변화, 2026년 7월은 부분월'),
 ('연도별 포함·제외','annual_inclusion_exclusion_summary.csv','가격 공통표본에서 임대 결합으로 연결되는 사유'),
 ('임대정보·수량 근거','income_quantity_scope_details.csv','필드·기록일·통화 메타데이터·수량범위; 실제 분배금 아님'),
 ('발행·소각 점검','address_supply_status_all_years.csv','선정 주소 전체의 Gnosis 수량기록; 법적 청산/체인이동 입증과 구분')]
with (ROOT/'docs/table_file_map.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['논문 위치','결과 파일','적용 기준','SHA256'])
 for label,file,meaning in tablemap:w.writerow([label,'results/'+file,meaning,hashlib.sha256((OUT/file).read_bytes()).hexdigest()])
report={'checks':checks,'passed':True,'scope':'Arithmetic and archive reproducibility; not proof of realized cash flow, legal redemption or historical cross-chain rights.'}
(OUT/'independent_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Independent checks passed:',len(checks))
