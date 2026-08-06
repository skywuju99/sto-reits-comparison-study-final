# 부동산 STO와 리츠(REITs)의 수익률·위험 특성 비교와 투자자 보호체계 연구

## 1. 연구 개요

이 저장소는 석사학위논문  
「부동산 STO와 리츠(REITs)의 수익률·위험 특성 비교와 투자자 보호체계 연구」의 데이터, 분석코드, 검증자료 및 재현성 부록을 정리한 저장소이다.

본 연구는 미국 소재 주거용 RealToken을 부동산 STO의 사례로 활용하고, Swapcat과 YAM에서 관찰된 2차시장 체결자료를 통합하여 수익률, 유동성 및 가격형성 구조를 분석한다.

REIT의 주 비교지표로는 FTSE Nareit U.S. Real Estate Index Series의 Residential 부문 연간 총수익률을 사용한다. FTSE EPRA Nareit Global Real Estate Index Series의 Global·USD·Total Return은 글로벌 상장 부동산 시장의 흐름을 확인하기 위한 보조지표로 구분한다.

---

## 2. 분석 범위

- 본분석 기간: 2022~2025년 완결연도
- STO 분석대상: 미국 소재 주거용 임대부동산 RealToken
- 2차시장: Swapcat 및 YAM
- REIT 주 비교지표: FTSE Nareit U.S. Real Estate Index Series Residential 부문 연간 총수익률
- REIT 보조지표: FTSE EPRA Nareit Global Real Estate Index Series Global·USD·Total Return
- 2026년 기준일: 2026년 7월 6일
- 2026년 자료: 부분연도 가격 및 유동성 보조분석에만 활용
- 2026년 자료는 연간 REIT 수익률과 직접 비교하지 않음

Swapcat과 YAM은 별개의 STO 상품이 아니라 동일한 RealToken이 거래되는 두 개의 2차시장으로 처리한다. 두 시장의 거래자료는 RealToken 컨트랙트 주소를 기준으로 통합한다.

---

## 3. 주요 데이터

### 3.1 RealT 자산자료

경로:

```text
data/realt/realt_asset_year_source.xlsx
```

주요 변수:

- RealToken 컨트랙트 주소
- 자산명 및 토큰 심볼
- 연도별 총투자금
- 연 순임대료
- 임대수익률
- 플랫폼 표시가격(tokenPrice)
- 상품유형
- 자료 업데이트 시점

RealT의 연 순임대료와 임대수익률은 개별 투자자의 실제 누계 분배금과 완전히 동일한 자료라고 보기 어렵다. 따라서 본 연구에서는 임대수익률 근사치로 해석한다.

### 3.2 Swapcat·YAM 통합 2차시장 자료

경로:

```text
data/secondary_market/
```

주요 분석항목:

- 시장·연도별 거래건수
- 거래자산 수
- 거래금액
- 자산·연도별 거래가격
- 연말 30일·60일·90일 VWAP
- 인접연도 공통자산 자본수익률
- 동일가중 평균
- 중위값
- 거래대금가중 수익률
- 최소 거래금액 및 이상치 제외 강건성
- 연도별 표본진단과 제외결과

대용량 거래단위 원자료와 전체 정규화 거래자료는 GitHub Release에서 제공한다.

### 3.3 발행·소각 자료

경로:

```text
data/mint_burn/
```

발행·소각은 ERC-20 Transfer 이벤트의 영주소 이동을 기준으로 판별한다.

- 영주소 → 일반주소: 발행
- 일반주소 → 영주소: 소각

수집대상 주소는 총 791개이며, 이 중 785개 주소에서 발행 또는 소각 이벤트가 확인되었다. 다만 소각 이벤트만으로 자산 매각, 상환, 청산, 마이그레이션 또는 기술적 재구성의 원인을 확정할 수 없다.

### 3.4 REIT 비교자료

#### 주 비교지표

경로:

```text
data/reits/ftse_nareit_us_residential_total_return_2022_2025_final.csv
```

- Index series: FTSE Nareit U.S. Real Estate Index Series
- Property sector: Residential
- Currency: U.S. Dollars
- Return type: Annual Total Return
- 활용 구분: 주 비교지표

| 연도 | 미국 주거용 REIT 총수익률 |
|---|---:|
| 2022 | -31.34% |
| 2023 | +7.66% |
| 2024 | +12.83% |
| 2025 | -7.43% |

#### 보조지표

경로:

```text
data/reits/ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv
```

- Index series: FTSE EPRA Nareit Global Real Estate Index Series
- Geographic scope: Global
- Currency: USD
- Return type: Total Return
- 활용 구분: 글로벌 시장 보조지표

| 연도 | Global·USD·Total Return |
|---|---:|
| 2022 | -23.58% |
| 2023 | +9.78% |
| 2024 | +1.57% |
| 2025 | +11.04% |

ETF 조정주가 자료는 공식 지수 관측치가 아니므로 본분석에 사용하지 않는다.

### 3.5 논문 표 재현자료

경로:

```text
results/thesis_tables/
```

포함 자료:

- 표 5-5: 미국 주거용 및 글로벌 REIT 수익률
- 표 5-8: Swapcat·YAM 통합 거래현황
- 표 5-9: STO 2차시장 관찰 자본수익률
- 표 5-10: 시장가격 반영 복합수익률 근사치
- 표 5-11: 현행 플랫폼 표시가격과 2차시장 가격 수준
- 표 5-12: 월별 체결가격 주요 시점
- 2026년 공통자산 부분연도 보조분석
- 표 5-13: 강건성 결과

---

## 4. 표본 선정

본분석은 다음 조건을 충족하는 RealToken을 대상으로 한다.

1. RealT 자산과 토큰 컨트랙트 주소를 연결할 수 있을 것
2. 미국 소재 자산일 것
3. 주거용 임대부동산일 것
4. 유효한 Swapcat 또는 YAM 체결자료가 존재할 것
5. USD 연동 결제토큰을 이용한 거래일 것
6. 거래금액이 1달러 이상일 것
7. 해당 연도의 연말 90일 관찰 VWAP를 산정할 수 있을 것
8. 자본수익률 분석에서는 인접연도에 동일한 주소가 관측될 것

다음 항목은 본표본에서 제외한다.

- 결제토큰 및 스테이블코인
- 거버넌스·생태계 토큰
- 대출형 상품
- 매출채권 및 수익참가형 상품
- 미국 외 자산
- 비주거용 자산
- 잘못된 decimals가 적용된 거래
- 비경제적 거래
- 연말 관찰가격을 산정할 수 없는 자산

상세 표본선정 기준은 다음 문서에 제시한다.

```text
docs/Appendix_B_Sample_Construction.md
```

---

## 5. 수익률과 가격지표의 산정

### 5.1 연말 90일 관찰 VWAP

각 자산의 연말 관찰가격은 해당 연도 마지막 90일 동안 발생한 유효 체결의 거래량가중평균가격(VWAP)으로 산정한다.

$$
VWAP_{i,t}=\frac{\sum_j P_{i,t,j}Q_{i,t,j}}{\sum_j Q_{i,t,j}}
$$

여기서 $P$는 체결가격, $Q$는 체결수량이다.

연말 90일 VWAP는 관찰된 체결가격의 평균수준이며, 해당 가격에서 모든 보유물량을 즉시 매도할 수 있음을 의미하지 않는다.

### 5.2 Swapcat·YAM 관찰 자본수익률

인접한 두 연도에 모두 연말 90일 VWAP가 확인되는 공통자산을 대상으로 자본수익률을 산출한다.

$$
CR_{i,t}=\frac{VWAP_{i,t}-VWAP_{i,t-1}}{VWAP_{i,t-1}}
$$

대표지표는 다음과 같이 구분한다.

- 동일가중 평균
- 중위값
- 해당 연도 거래대금가중 평균

이 지표는 Swapcat과 YAM에서 관찰된 가격변화를 의미하며, 전체 RealToken 시장의 확정적인 시장수익률을 의미하지 않는다.

### 5.3 시장가격 반영 복합수익률 근사치

동일 공통자산 표본에서 임대수익률 근사치와 관찰 자본수익률을 결합한다.

$$
MCR_t=RY_t+CR_t
$$

- $RY_t$: 플랫폼 연 순임대료를 이용한 임대수익률 근사치
- $CR_t$: Swapcat·YAM 관찰 자본수익률
- $MCR_t$: 시장가격 반영 복합수익률 근사치

이 값은 개별 투자자의 실제 누계 분배금, 분배시점, 거래비용 및 세금을 모두 반영한 엄밀한 보유기간 총수익률이 아니다.

### 5.4 REIT와의 비교

STO 관찰 자본수익률은 분배수익을 포함하지 않지만, 공식 REIT 총수익률은 가격변화와 분배수익을 모두 포함한다.

따라서 두 지표의 병렬 제시는 가격반영 양상의 차이를 검토하기 위한 기술적 비교이며, 직접적인 성과 우열을 의미하지 않는다.

시장가격 반영 복합수익률 근사치도 공식 REIT 총수익률과 산정방식이 다르므로 직접적인 우열 비교에 사용하지 않는다.

### 5.5 현행 플랫폼 표시가격과의 보조 비교

플랫폼 가격 비교에서는 2026년 5월 24일 수집한 RealT tokenPrice를 공통 기준으로 사용한다.

$$
Relative\ Difference=\left(\frac{Observed\ VWAP}{Current\ tokenPrice}-1\right)\times100
$$

과거 연도의 정확한 동시점 플랫폼 표시가격 스냅샷을 확보하지 못했으므로 이 값은 역사적 동시점 가격괴리가 아니다.

2026년 -72.6%는 다음을 의미하지 않는다.

- 플랫폼 표시가격의 확정적인 과대평가 규모
- 모든 보유물량의 회수 가능 가격 차이
- 전체 RealToken의 시장수익률

### 5.6 월별 가격추이

월별 VWAP는 해당 월의 USD 연동 결제 체결가격을 체결수량으로 가중하여 산출한다.

월별로 실제 거래된 자산의 구성이 달라질 수 있으므로 월별 전체 VWAP는 동일자산의 연속적인 시장수익률이 아니라 가격형성 추세를 보여주는 기술통계로 해석한다.

---

## 6. 저장소 구조

```text
sto-reits-comparison-study-final/
├── README.md
├── requirements.txt
├── code/
│   └── recalculate_yam_swapcat.py
├── data/
│   ├── metadata/
│   ├── mint_burn/
│   ├── realt/
│   │   └── realt_asset_year_source.xlsx
│   ├── reits/
│   │   ├── README.md
│   │   ├── ftse_nareit_us_residential_total_return_2022_2025_final.csv
│   │   └── ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv
│   └── secondary_market/
├── docs/
│   ├── Appendix_A_Data_Sources.md
│   ├── Appendix_B_Sample_Construction.md
│   ├── Appendix_C_YAM_Swapcat_Integration.md
│   ├── Appendix_D_Return_Calculation.md
│   ├── Appendix_E_Mint_Burn_Analysis.md
│   ├── Appendix_F_REITs_Benchmark.md
│   └── Appendix_G_Data_Limitations.md
├── logs/
│   ├── mint_burn_missing_token_log.txt
│   └── reits_official_data_collection_log.txt
└── results/
    ├── thesis_tables/
    └── yam_swapcat_recalculation_summary.xlsx
```

---

## 7. 분석 재현 방법

### 7.1 준비

Python 3.10 이상을 권장한다.

GitHub Release에서 대용량 원자료를 내려받은 뒤 다음 경로에 배치한다.

```text
data/raw/secondary_market/yam_offeraccepted_raw.csv
data/raw/secondary_market/swapcat_realtoken_trades.csv
```

필요한 메타데이터:

```text
data/metadata/yam_token_metadata.csv
data/metadata/asset_master_match.csv
data/metadata/payment_token_decimals.csv
```

### 7.2 실행

저장소 루트에서 다음 명령을 실행한다.

```bash
python code/recalculate_yam_swapcat.py
```

실행 옵션 확인:

```bash
python code/recalculate_yam_swapcat.py --help
```

### 7.3 코드 처리범위

분석코드는 다음 작업을 수행한다.

1. YAM과 Swapcat 원자료 로드
2. 토큰주소 표준화
3. 결제토큰 decimals 반영
4. USD 연동 결제거래 식별
5. 체결가격·수량·거래금액 계산
6. 미국 주거용 RealToken 표본 분류
7. 연도별 거래활동 집계
8. 연말 90일 VWAP 산정
9. 인접연도 공통자산 자본수익률 산출
10. 이상치 및 거래금액 기준 강건성 검토
11. 표본진단과 결과파일 생성

---

## 8. 핵심 결과파일

```text
data/secondary_market/common_asset_returns_us_residential.csv
```

연도별 공통자산의 동일가중·중위·거래대금가중 관찰 자본수익률

```text
data/secondary_market/common_asset_return_detail_us_residential.csv
```

자산별 연말 90일 VWAP와 자본수익률 상세자료

```text
data/secondary_market/common_asset_returns_robustness.csv
```

대체 거래금액 기준 및 이상치 제외 결과

```text
data/secondary_market/asset_year_price_summary_us_residential.csv
```

자산·연도별 가격, 거래량 및 연말 90일 VWAP

```text
data/secondary_market/platform_year_summary_us_residential.csv
```

Swapcat·YAM 시장별 거래활동

```text
results/thesis_tables/
```

최종 논문 표와 직접 연결되는 요약 CSV

---

## 9. GitHub Release

대용량 자료는 일반 저장소에 직접 포함하지 않고 Releases 페이지에서 제공한다.

### Final Replication Data v2.0.0

포함 자료:

- `secondary_market_raw_sources_v2.0.zip`
  - YAM OfferAccepted 원자료
  - Swapcat RealToken 거래원자료
  - 재계산에 필요한 보조 원자료

- `secondary_market_processed_results_v2.0.zip`
  - YAM·Swapcat 통합 정규화 거래자료
  - 자산·연도별 가격요약
  - 공통자산 자본수익률
  - 표본진단 및 강건성 결과

---

## 10. 자료의 한계

- RealT 단일 플랫폼 사례이므로 전체 부동산 STO 시장으로 일반화하기 어렵다.
- 거래가 없는 토큰은 관찰 시장가격을 산정할 수 없다.
- 연말 90일 VWAP는 일부 거래의 영향을 받을 수 있다.
- 관찰 체결가격은 해당 가격에서 모든 보유물량을 즉시 처분할 수 있음을 의미하지 않는다.
- 양 기간 모두 거래된 공통자산만 포함하므로 선택편향이 존재할 수 있다.
- 개별 투자자의 실제 누계 분배금과 완전한 현금흐름을 확보하지 못하였다.
- 총투자금 변동에는 토큰 수량변화가 포함될 수 있다.
- 과거 각 연도의 정확한 플랫폼 표시가격 스냅샷을 확보하지 못하였다.
- 2026년 플랫폼 표시가격과 체결가격의 기준시점이 일치하지 않는다.
- 토큰 소각만으로 매각·상환·청산·마이그레이션 사유를 확정할 수 없다.
- 공식적인 구주소·신주소 마이그레이션 연결표를 확보하지 못하였다.
- 2026년은 부분연도 자료이므로 확정적인 연간 성과로 해석하지 않는다.
- STO 자본수익률과 REIT 총수익률은 분배수익 포함 여부가 다르다.

상세 내용은 다음 문서를 참조한다.

```text
docs/Appendix_G_Data_Limitations.md
```

---

## 11. 이용 및 인용

본 저장소는 학술연구의 검증과 재현을 목적으로 제공한다.

RealT, Nareit, FTSE Russell 및 블록체인 원자료의 권리와 이용조건은 각 제공기관의 정책을 따른다. 저장소의 가공자료와 분석코드를 사용할 경우 연구명과 저장소 주소를 함께 표시하는 것을 권장한다.
