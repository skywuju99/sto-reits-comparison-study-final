from pathlib import Path
import json,csv
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
annual=json.loads((R/'recalculation_manifest.json').read_text(encoding='utf-8'))
d=pd.read_csv(R/'trading_frequency_recency_summary.csv')
p=pd.read_csv(R/'table_4_3_population_intersections.csv')
s=pd.read_csv(R/'income_quantity_scope_summary.csv')
burn=pd.read_csv(R/'positive_to_zero_supply_cases.csv')
lines=['실증분석 계산 결과 — 교수님 추가 피드백 반영','버전: empirical-20261023-v1','',
 'U와 IPI 채점은 변경하지 않았다. 이 묶음은 실증분석 계산과 재현자료를 확정하기 위한 것이다.',
 '원시 YAM·Swapcat 거래자료 정규화 → 연말 상태 이월 → 수량 대조와 S/D 대응 → 임대정보 결합 → 관찰기간 비교 → 거래빈도/최근 거래 경과일/미관찰 비중 계산 → 독립 검산 순서로 실행하였다.',
 '이는 보존자료와 명시한 산식에 따른 계산의 완료를 뜻한다. 실제 분배금·전체 체인 이동·법적 청산 상태를 새로 입증했다는 뜻은 아니다.','',
 '1. 최종 임대정보 결합 결과',
 '연도 | 표본 수 | 시장가격 기준 임대정보(%) | 가격변화(%) | 합산 근사치(%) | 미국 주거용 리츠 총수익률(%)']
for r in annual['annual']:
 lines.append(f"{r['year']} | {r['n']} | {r['income_pct']:.2f} | {r['capital_pct']:.2f} | {r['combined_pct']:.2f} | {r['reit_total_return_pct']:.2f}")
lines+=['반올림 전 구성요소를 합산한다. 결합 가중치는 기초 플랫폼 총투자금 비중이다.',
 '2023년: 확인된 12개 S/D 사례를 포함하여 93개에서 105개로 변경했다. 동일 자산의 임대정보를 두 번 세지 않으며 D형 거래가격을 S형 가격에 합치지 않았다.',
 '2024·2025년: Marloes의 임대정보와 적용 수량 범위를 확정하지 못하여 임대정보 결합에서 제외했다. 각각 347개·381개이다. 해당 주소의 가격 거래기록은 가격 분석에 유지했다.',
 '표 4-5의 가격 분석 표본 44·105·348·382개와 거래대금 가중값 0.95·2.07·10.11·-15.15%는 유지된다.',
 '리츠 값은 원고에서 확인한 공식 지수 값을 비교 열로 유지한 것이다. 이 실행은 Nareit 원문을 다시 수집하는 절차를 포함하지 않는다.','',
 '2. 표본 집합의 관계',
 '연도 | 플랫폼 유효표본(전체) | 해당 연도 말까지 기록 확인된 분류주소 | 연중 거래 | 마지막90일 거래 | 양시점 가격 | 임대 결합']
for r in p.itertuples():
 lines.append(f'{r.year} | {r.platform_valid_all} | {r.historically_observed_classified_n} | {r.year_traded_n} | {r.last90_traded_n} | '+('-' if pd.isna(r.paired_prices_n) else str(int(r.paired_prices_n)))+' | '+('-' if pd.isna(r.final_combined_n) else str(int(r.final_combined_n))))
lines+=['2025년 플랫폼 유효표본 825개 중 기존 404개 분류집합에 속하는 것은 390개이고, 밖에 있는 것은 435개이다. 따라서 825→404를 같은 표본의 단순 탈락 과정으로 표시하지 않는다.',
 '404개는 보존된 분류자료에서 정한 주소 집합이다. 연도별로 최초 기록이 확인된 주소만 거래 미관찰 비중의 분모에 넣었다. 현재 상장·거래 가능 주소의 전수 명부가 아니며, 주소 수가 독립적인 부동산 수와 항상 같지는 않다.',
 '2025년 양시점 가격 382개와 임대 결합 381개의 차이는 Marloes 제외 1개이다.','',
 '3. 거래빈도·최근 거래 경과일·거래 미관찰 비중',
 '연도 | 해당 시점까지 기록된 주소 | 기간중 거래주소 | 거래주소당 건수 중위값 | 마지막90일 미관찰 수(비중) | 전체 역사적 거래주소의 마지막 거래 후 경과일 중위값']
for r in d.itertuples():
 lines.append(f"{r.year}{'(~7.6)' if r.year==2026 else ''} | {r.historically_observed_addresses} | {r.year_traded_n} | {r.trades_median_traded:g} | {r.last90_unobserved_n}({r.last90_unobserved_pct:.2f}%) | {r.last_trade_age_median_ever:g}일")
lines+=['거래건수 중위값은 해당 연도/부분연도에 1회 이상 거래된 주소를 대상으로 한다. 최근 거래 경과일 중위값은 분석 종료일까지 과거 적격 거래가 한 번이라도 관찰된 주소를 대상으로 한다. 날짜 차이로 산출하며 과거 거래 자체가 없으면 경과일을 0으로 넣지 않는다.',
 '2025년 전체 404개 중 연중 거래 미관찰은 15개(3.71%), 마지막 90일 미관찰은 18개(4.46%)이다. 2026년 7월 6일 기준 마지막 90일 미관찰은 121개(29.95%)이다.',
 '2025년 전체 404개에서 최근 거래 경과일 중위값은 8일, 2026년은 53일이다. 해당 기간 거래주소만으로 좁히면 각각 7일과 50.5일이다. 본문에 어느 집합을 썼는지 반드시 표시한다.',
 '2026년 연중 거래건수는 부분연도이므로 완결연도 2025년과 거래 빈도의 연간 수준으로 직접 비교하지 않는다. 마지막 90일은 길이가 같지만 거래 가능 상태·종료 주소 등이 통제된 활성시장 표본은 아니다.',
 '이 지표들은 거래 빈도와 거래 공백을 나타낸다. 스프레드·시장 깊이·실제 매도 소요기간을 측정한 것은 아니다.','',
 '4. 관찰기간 비교',
 '2022~2026년 모두 30·90·180일에 공통으로 들어오는 주소를 사용하고 기말 90일 거래대금 비중을 고정했다.',
 '동일표본 수: 2022년32, 2023년103, 2024년310, 2025년315, 2026년154.',
 '2022년 -0.17/-0.19/+3.88%, 2023년 +0.36/+2.07/-1.38%로 부호가 달라진다.',
 '2025년 -17.43/-15.29/-10.83%, 2026년 -79.77/-71.19/-63.58%로 하락 방향은 유지되지만 폭은 다르다. 2026년 30일-90일 하락폭 차이는 8.58%p이다.',
 '2023년 동일표본 103개 기초가격의 90일 거래는 371건, 중위값2건, 단일 체결주소37개이며 180일에는 3,327건이다. 거래기록의 포함 범위에 따른 기준가격 변화 가능성을 보여주며 초기 가격 변동의 유일한 원인이라고 주장하지 않는다.',
 '이 검토는 가격변화율에 관한 것이며 임대정보 결합 근사치 전체의 강건성을 검증한 것은 아니다.','',
 '5. 발행·소각 및 임대정보의 수량 범위']
for r in burn.itertuples():
 lines.append(f"{r.year}: {r.name}; 기초 {r.quantity_start} → 기말 {r.quantity_end}. 가격 공통표본 포함={r.price_pair_included}, 임대 결합 포함={r.combined_included}.")
lines+=['2023년 Alcoy의 잔량 0 전환은 해당 연도 가격 공통표본·임대 결합표본에 들어 있지 않아 수익률 결과에 영향을 주지 않는다.',
 '2025년 Jefferson은 임대정보가 0인 소각 사례이다. Marloes를 제외한 381개에서 Jefferson까지 제외한 380개의 합산 근사치는 -6.88%이다. 가격 표본에서 Jefferson만 제외한 거래대금 가중 가격변화율은 기존 확인값 -15.23%이다.',
 '공급량 감소·잔량 0은 체인 기록상 사실이다. 계약상 상환 지급이나 법적 청산 완료와 동일시하지 않는다. 여러 체인 계약주소가 메타데이터에 있다고 해서 체인 이동 또는 이중 발행이라고 판단하지 않는다.','',
 '6. 임대정보 원자료와 이월 기록',
 '사용 필드: tokenHistory의 netRentYear(임대정보), totalInvestment(플랫폼 총투자금), tokenPrice(표시가격). 각 필드별 마지막 기록일을 따로 추적했다.',
 '통화: 2026년 4월 10일 보존 메타데이터의 currency=USD와 대조했다. 이 메타데이터는 각 과거 연말에 직접 관측한 통화 기록과 구분한다.',
 '기록 대상: 연말까지 확보된 마지막 연환산 임대정보이다. 원자료에는 해당 값이 실제로 지급된 연간 분배금임을 입증하는 지급내역이 없으며, 마지막 갱신일이 경제적 수취기간을 뜻하는 것도 아니다.',
 '분모: 일반 사례는 직전 연도 말 Gnosis 누적 순발행량. 확인된 2023년 12개 S/D 사례는 동일 임대정보의 자산 단위 범위에 맞춰 합산 수량을 적용했다. S+D 기초/기말 합계와 플랫폼 금액·표시가격의 수치적 일관성을 확인했다.',
 '수치적 일치만으로 모든 클래스의 법적 권리 동일성·실제 지급액을 입증하지 않는다. 따라서 명칭은 시장가격 기준 수익률 근사치로 유지한다.',
 '연도 | 최종 결합표본 | 전년 이전 임대정보 이월 | 순임대정보0 | 평균 아닌 기록 경과일 중위값']
for r in s.itertuples():lines.append(f'{r.year} | {r.n} | {r.carried_income_n} | {r.zero_income_n} | {r.record_age_days_median:g}일')
lines+=['2025년 381개 중 131개는 이전 연도 임대정보를 이월했다. 갱신이 없다는 사실은 임대료 수취가 지속됐다는 증거가 아니다.','',
 '7. 계산 검증과 원고 반영 구분',
 '원시 거래자료에서부터 실행되는 run_all.py와 입력 해시, 자산별 결과, 독립 검산 결과를 함께 보존했다. 표별 대응파일은 docs/table_file_map.csv에 있다.',
 '이 계산자료는 최신 원고의 표·결론·초록과 대응한다. archive/v2.0.0은 과거 분석 보존본이다. 기존 N93/348/382, 8.26/20.43/-6.69와 최신 N105/347/381, 8.37/20.72/-6.80을 혼용하지 않아야 한다.',
 '계산으로 해결한 것: 누락 표본 수량 대조, Marloes 제외, 연도별 재계산, 표본 집합관계, 거래빈도·경과일·미관찰 비중, 관찰기간별 결과, 보존자료에 대한 공급량 점검.',
 '계산만으로 확정하지 않은 것: 실제 분배금, 전 체인의 법적 권리·자산 이전, 법적 청산/상환 완료, 모든 과거 시점의 임대정보 경제적 범위. 보존자료의 한계로 명시하고 근사치로 해석한다.']
(ROOT/'계산결과_요약과논문반영사항.txt').write_text('\n'.join(lines),encoding='utf-8-sig')
# Korean-labelled compact tables for manuscript transfer, without rounding source data.
k=d[['year','historically_observed_addresses','year_traded_n','trades_median_traded','last90_unobserved_n','last90_unobserved_pct','last_trade_age_median_ever']].rename(columns={'year':'연도','historically_observed_addresses':'시점까지 기록된 분류주소 수','year_traded_n':'기간중 거래주소 수','trades_median_traded':'거래주소당 거래건수 중위값','last90_unobserved_n':'마지막90일 거래 미관찰 주소 수','last90_unobserved_pct':'마지막90일 미관찰 비중(%)','last_trade_age_median_ever':'과거 거래주소의 최근 거래 후 경과일 중위값(일)'})
k.to_csv(R/'거래빈도_경과일_미관찰비중.csv',index=False,encoding='utf-8-sig',lineterminator='\r\n')
print('Summary and Korean tables prepared.')
