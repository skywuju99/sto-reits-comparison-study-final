# GitHub 최종 반영 순서

대상 저장소:

`https://github.com/skywuju99/sto-reits-comparison-study-final`

## 1. 현재 상태

현재 저장소의 기본 구조(code, data, docs, logs, results)와 v2.0.0 Release는 그대로 유지한다.

다만 다음 항목은 최종 논문과 다르므로 수정이 필요하다.

- README의 논문 제목이 이전 제목으로 되어 있음
- Global REIT가 본분석 지표로 적혀 있음
- 미국 주거용 REIT CSV가 없음
- Appendix F가 Global 지수를 main benchmark로 설명함
- `연말 시장가격`, `실제 시장 자본수익률`, `조정 총수익률` 등 수정 전 용어가 남아 있음
- README의 Release 항목이 `예정 자료`로 되어 있음

## 2. 이 압축파일에서 교체할 파일

다음 파일은 기존 파일을 열고 내용 전체를 교체한다.

```text
README.md
docs/Appendix_D_Return_Calculation.md
docs/Appendix_F_REITs_Benchmark.md
docs/Appendix_G_Data_Limitations.md
logs/reits_official_data_collection_log.txt
```

## 3. 이 압축파일에서 새로 추가할 파일

```text
data/reits/README.md
data/reits/ftse_nareit_us_residential_total_return_2022_2025_final.csv
results/thesis_tables/table_5_05_reit_benchmarks.csv
results/thesis_tables/table_5_08_secondary_market_summary.csv
results/thesis_tables/table_5_09_secondary_market_capital_returns.csv
results/thesis_tables/table_5_10_market_price_composite_return_proxy.csv
results/thesis_tables/table_5_11_platform_price_level_comparison.csv
results/thesis_tables/table_5_12_monthly_price_key_points.csv
results/thesis_tables/table_5_12_2026_common_asset_supplement.csv
results/thesis_tables/table_5_13_robustness.csv
```

## 4. 그대로 둘 파일과 폴더

```text
code/
data/metadata/
data/mint_burn/
data/realt/
data/secondary_market/
data/reits/ftse_epra_nareit_global_usd_total_return_2022_2025_final.csv
docs/Appendix_A_Data_Sources.md
docs/Appendix_B_Sample_Construction.md
docs/Appendix_C_YAM_Swapcat_Integration.md
docs/Appendix_E_Mint_Burn_Analysis.md
results/yam_swapcat_recalculation_summary.xlsx
requirements.txt
.gitignore
```

기존 v2.0.0 Release의 압축파일도 다시 올릴 필요가 없다.

## 5. 올리면 안 되는 파일

사용자 파일 보관함에 있던 다음 파일은 미국 주거용 REIT 연간 수익률이 `UNCONFIRMED`로 표시된 과거 수집 시도 파일이므로 최종 저장소에 올리지 않는다.

```text
ftse_nareit_us_residential_annual_returns_official.csv
```

최종 저장소에는 이 압축파일에 포함된 다음 파일을 사용한다.

```text
ftse_nareit_us_residential_total_return_2022_2025_final.csv
```

## 6. GitHub 웹에서 반영하는 방법

### 기존 파일 교체

1. 교체할 파일을 연다.
2. 우측 상단 연필 아이콘(Edit this file)을 누른다.
3. 기존 내용을 모두 삭제한다.
4. 압축파일 속 같은 경로의 파일 내용을 붙여 넣는다.
5. `Commit changes`를 누른다.

### 새 파일 추가

1. 파일을 넣을 상위 폴더로 이동한다.
2. `Add file` → `Upload files`를 누른다.
3. 압축을 해제한 뒤 해당 폴더의 파일을 끌어다 놓는다.
4. `Commit changes`를 누른다.

`results/thesis_tables` 폴더가 없다면 저장소의 `results` 폴더에서 `Add file` → `Create new file`을 누르고 파일명에 아래처럼 경로까지 입력하면 폴더가 생성된다.

```text
thesis_tables/table_5_05_reit_benchmarks.csv
```

나머지 CSV는 생성된 `results/thesis_tables` 폴더에 업로드한다.

## 7. 권장 커밋 메시지

```text
Align repository with final thesis benchmarks and results
```

설명:

```text
- Adopt U.S. Residential REIT total return as the primary benchmark
- Retain Global USD Total Return as a supplementary benchmark
- Align return terminology with the final thesis
- Add thesis table replication CSV files
- Clarify non-contemporaneous platform-price comparison
- Add partial-year 2026 and liquidity limitations
```

## 8. 마지막 확인

GitHub 첫 화면에서 아래 사항을 확인한다.

- 논문 제목이 최종 제목으로 표시됨
- 미국 주거용 REIT가 주 비교지표로 표시됨
- Global REIT는 보조지표로 표시됨
- `data/reits`에 미국 주거용 CSV가 추가됨
- `results/thesis_tables`에 8개 CSV가 보임
- Appendix F에서 U.S. Residential가 Primary benchmark로 표시됨
- Release가 `예정 자료`가 아니라 `제공 자료`로 표시됨
