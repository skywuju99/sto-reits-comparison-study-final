# 부동산 STO와 REITs 비교 연구

## 1. 연구 개요

이 저장소는 석사학위논문  
**「부동산 STO와 리츠(REITs)의 구조적 차이와 투자자 보호체계 비교 및 수익률·위험 특성 분석」**  
의 데이터, 분석코드, 검증자료 및 부록을 정리한 재현 저장소이다.

본 연구는 RealT 기반 부동산 토큰을 부동산 STO의 분석대상으로 사용하고, 실제 2차시장인 YAM과 Swapcat의 체결자료를 통합하여 자본수익률과 유동성을 분석한다. REITs 비교에는 FTSE EPRA Nareit Global Real Estate Index Series의 USD 기준 총수익률을 사용한다.

---

## 2. 본분석 범위

- 본분석 기간: **2022~2025년 완결연도**
- STO 분석대상: 미국 소재 주거용 임대부동산 RealToken
- 2차시장: YAM 및 Swapcat
- REITs 기준: Global, USD, Total Return
- 2026년: 완결연도가 아니므로 연간 총수익률 본분석에서 제외

YAM과 Swapcat은 별개의 STO 상품이 아니라 동일한 RealToken이 거래되는 두 개의 2차시장으로 처리한다. 두 시장의 거래자료는 RealToken 컨트랙트 주소를 기준으로 통합한다.

---

## 3. 주요 데이터

### 3.1 RealT 자산자료

`data/realt/realt_asset_year_source.xlsx`

주요 항목:

- RealToken 컨트랙트 주소
- 자산명과 토큰 심볼
- 연도별 총투자금액
- 연 순임대료
- 연 임대수익률
- RealT 플랫폼 제시 tokenPrice
- 상품유형과 업데이트 시점

RealT 임대수익률은 플랫폼 제공 연간 수익률이며, 개별 투자자의 실제 현금흐름을 재구성한 값은 아니다.

### 3.2 YAM·Swapcat 통합 2차시장 자료

`data/secondary_market/`

주요 결과:

- 시장·연도별 거래건수와 거래금액
- 자산·연도별 거래가격
- 연말 30일·60일·90일 VWAP
- 인접연도 공통자산 자본수익률
- 동일가중·중앙값·거래대금가중 수익률
- 최소 거래금액 및 이상치 제외 강건성 분석
- 연도별 표본 진단과 제외 결과

대용량 거래단위 원자료와 전체 정규화 거래자료는 GitHub Release에서 별도로 제공한다.

### 3.3 발행·소각 자료

`data/mint_burn/`

발행과 소각은 ERC-20 Transfer 이벤트의 영주소 이동을 기준으로 판별한다.

- 영주소 → 일반 주소: 발행
- 일반 주소 → 영주소: 소각

최종 통합자료는 791개 주소를 수집대상으로 하며, 부동산 RealToken 분석에 필요한 주소의 발행·소각 이벤트를 포함한다.

주의할 점은 소각 이벤트만으로 자산 매각, 상환, 청산, 마이그레이션 또는 기술적 재구성의 원인을 확정할 수 없다는 것이다.

### 3.4 REITs 비교자료

`data/reits/ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv`

본분석 지수:

- FTSE EPRA Nareit Global Real Estate Index Series
- Geographic scope: Global
- Currency: USD
- Return type: Total Return

| 연도 | 연간 총수익률 |
|---:|---:|
| 2022 | -23.58% |
| 2023 | 9.78% |
| 2024 | 1.57% |
| 2025 | 11.04% |

공식 출처는 Nareit Global Returns 문서이며, ETF 자료는 공식 지수를 대체하지 않는다.

---

## 4. 표본 선정

본분석은 다음 조건을 충족하는 RealToken을 대상으로 한다.

1. RealT 자산과 토큰주소를 연결할 수 있을 것
2. 미국 소재 자산일 것
3. 주거용 임대부동산일 것
4. 유효한 YAM 또는 Swapcat 체결자료가 존재할 것
5. 해당 연도의 연말 90일 VWAP를 산정할 수 있을 것
6. 인접연도에 동일한 토큰주소가 관측될 것

다음 항목은 본표본에서 제외한다.

- 결제토큰과 스테이블코인
- 거버넌스·생태계 토큰
- 대출형 상품
- 매출채권 및 수익참가형 상품
- 미국 외 자산
- 비주거용 자산
- 잘못된 decimals 또는 비경제적 거래
- 연말가격을 산정할 수 없는 자산

상세 기준은 `docs/Appendix_B_Sample_Construction.md`에 제시한다.

---

## 5. 수익률 산정

### 5.1 연말 시장가격

각 자산의 연말 시장가격은 해당 연도 마지막 90일 동안 체결된 유효 거래의 VWAP로 산정한다.

\[
VWAP_{i,t}
=
\frac{\sum_j P_{i,t,j}Q_{i,t,j}}
{\sum_j Q_{i,t,j}}
\]

### 5.2 자본수익률

\[
CR_{i,t}
=
\frac{VWAP_{i,t}-VWAP_{i,t-1}}
{VWAP_{i,t-1}}
\]

인접연도 모두 연말 90일 VWAP가 존재하는 공통자산만 포함한다.

### 5.3 2차시장 가격 반영 조정 총수익률

\[
ATR_{i,t}=RY_{i,t}+CR_{i,t}
\]

- \(RY\): RealT 연간 임대수익률
- \(CR\): 실제 2차시장 체결가격 기준 자본수익률

이 값은 실제 투자자의 배당 수령 시점과 보유기간 전체 현금흐름을 재구성한 엄밀한 보유기간수익률이 아니므로, 본 연구에서는 **2차시장 가격 반영 조정 총수익률**로 해석한다.

---

## 6. 저장소 구조

```text
sto-reits-comparison-study-final/
├── README.md
├── code/
│   └── recalculate_yam_swapcat.py
├── data/
│   ├── metadata/
│   │   ├── asset_master_clean.csv
│   │   ├── asset_master_match.csv
│   │   ├── data_dictionary.csv
│   │   ├── exclusion_report.csv
│   │   ├── payment_token_decimals.csv
│   │   ├── raw_validation_report.csv
│   │   ├── source_list.csv
│   │   └── yam_token_metadata.csv
│   ├── mint_burn/
│   │   ├── mint_burn_token_coverage.csv
│   │   └── realtoken_mint_burn_history_complete.csv
│   ├── realt/
│   │   └── realt_asset_year_source.xlsx
│   ├── reits/
│   │   └── ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv
│   └── secondary_market/
│       ├── annual_sample_diagnostics_all_variants.csv
│       ├── annual_sample_diagnostics_us_residential.csv
│       ├── asset_year_price_summary_us_residential.csv
│       ├── common_asset_return_detail_us_residential.csv
│       ├── common_asset_returns_robustness.csv
│       ├── common_asset_returns_us_residential.csv
│       └── platform_year_summary_us_residential.csv
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
    └── yam_swapcat_recalculation_summary.xlsx
```

---

## 7. 분석 재현 방법

### 7.1 준비

Python 3.10 이상을 권장한다.

대용량 원자료는 저장소의 **Releases** 페이지에서 내려받은 뒤 다음 경로에 배치한다.

```text
data/raw/secondary_market/yam_offeraccepted_raw.csv
data/raw/secondary_market/swapcat_realtoken_trades.csv
```

분석에 필요한 메타데이터는 일반 저장소의 다음 파일을 사용한다.

```text
data/metadata/yam_token_metadata.csv
data/metadata/asset_master_match.csv
```

### 7.2 실행

저장소 루트에서 다음 명령을 실행한다.

```bash
python code/recalculate_yam_swapcat.py
```

기본 출력경로:

```text
results/recalculated/
results/yam_swapcat_recalculated_results.zip
```

입력 또는 출력경로를 변경하려면 다음 명령으로 옵션을 확인한다.

```bash
python code/recalculate_yam_swapcat.py --help
```

### 7.3 코드 실행 범위

`recalculate_yam_swapcat.py`는 다음 작업을 수행한다.

1. YAM과 Swapcat 원자료 로드
2. 토큰주소 및 decimals 표준화
3. USD 유사 결제토큰 판별
4. 거래가격·수량·거래금액 계산
5. 미국 주거용 RealToken 표본 분류
6. 연도별 가격과 연말 90일 VWAP 산정
7. 인접연도 공통자산 자본수익률 계산
8. 거래금액 기준과 이상치 제외 강건성 분석
9. 표본 진단 및 결과파일 생성

---

## 8. 결과파일 안내

### 핵심 분석결과

- `common_asset_returns_us_residential.csv`  
  연도별 공통자산 대표 자본수익률

- `common_asset_return_detail_us_residential.csv`  
  자산별 가격과 자본수익률 상세자료

- `common_asset_returns_robustness.csv`  
  대체 거래금액 기준과 이상치 제외 결과

- `asset_year_price_summary_us_residential.csv`  
  자산·연도별 가격, 거래량, 연말 90일 VWAP

- `platform_year_summary_us_residential.csv`  
  YAM·Swapcat 시장별 거래활동

- `yam_swapcat_recalculation_summary.xlsx`  
  주요 결과를 정리한 확인용 Excel 파일

### 자료 설명

- `data/metadata/data_dictionary.csv`  
  변수명, 자료형, 단위, 계산방법 및 분석용도

- `data/metadata/source_list.csv`  
  자료별 제공기관, 수집범위, URL 및 저장위치

---

## 9. GitHub Release

대용량 자료는 일반 저장소에 직접 포함하지 않고 Releases 페이지에서 제공한다.

예정 자료:

- YAM 원본 OfferAccepted 이벤트
- Swapcat 원본 RealToken 거래자료
- 통합 정규화 거래자료
- 전체 재계산 결과 압축파일

Releases:

`https://github.com/skywuju99/sto-reits-comparison-study-final/releases`

---

## 10. 자료의 한계

- 공식적인 구주소·신주소 토큰 마이그레이션 연결표를 확보하지 못했다.
- 개별 자산의 매각·상환 사유와 토큰당 상환금액을 완전하게 확보하지 못했다.
- 거래가 없는 토큰은 실제 시장가격을 산정할 수 없다.
- 소각 이벤트만으로 소각의 경제적 사유를 확정할 수 없다.
- RealT 임대수익률은 투자자별 실제 현금흐름과 다를 수 있다.
- 연말가격은 유동성이 낮은 자산에서 일부 거래의 영향을 받을 수 있다.
- LSEG Datastream의 전체 날짜별 기계판독 원시파일은 확보하지 못했다.
- 2026년은 자료별 기준일이 일치하지 않아 연간 총수익률 본분석에서 제외했다.

세부 내용은 `docs/Appendix_G_Data_Limitations.md`를 참조한다.

---

## 11. 이용 및 인용

본 저장소는 학술연구의 검증과 재현을 목적으로 제공한다.

RealT, Nareit, FTSE Russell 및 블록체인 원자료의 저작권과 이용조건은 각 제공기관의 정책을 따른다. 저장소의 가공자료와 분석코드를 사용할 경우 연구명과 저장소 주소를 함께 표시하는 것을 권장한다.

