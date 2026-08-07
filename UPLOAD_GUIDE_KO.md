# GitHub 최종 수정 업로드 안내

## 1. 기존 파일 전체 교체

- `README.md`
- `docs/Appendix_D_Return_Calculation.md`
- `docs/Appendix_F_REITs_Benchmark.md`
- `docs/Appendix_G_Data_Limitations.md`
- `logs/reits_official_data_collection_log.txt`

## 2. 새로 추가

- `data/reits/README.md`
- `data/reits/ftse_nareit_us_residential_total_return_2022_2025_final.csv`
- `logs/data_snapshot_log.csv`
- `results/thesis_tables/` 전체

## 3. 기존 파일에 행을 병합

다음 패치 파일은 기존 메타데이터 파일을 통째로 덮어쓰는 용도가 아니다.

- `data/metadata/source_list_patch_rows.csv`
  - 내용을 기존 `data/metadata/source_list.csv`에 병합
- `data/metadata/data_dictionary_patch_rows.csv`
  - 내용을 기존 `data/metadata/data_dictionary.csv`에 병합

## 4. 그대로 유지

- `code/recalculate_yam_swapcat.py`
- `data/realt/`
- `data/secondary_market/`
- `data/mint_burn/`
- 기존 Global REIT CSV
- 기존 GitHub Release 원자료와 가공자료

## 5. 주의

- 존재하지 않는 분석코드를 새로 만든 것처럼 빈 파일로 올리지 않는다.
- 표 5-7의 `약 26개 토큰`, `약 7개 토큰`은 Smith and Baur(2025) 원문의 정확한 변수명과 단위를 확인하기 전까지 재현 CSV로 공개하지 않는다.
- 정확한 수집시각이나 cutoff block을 모르면 추정하지 않고 `not_recorded`로 둔다.
- 압축파일의 최상위 폴더 자체를 저장소 안에 올리지 말고, 내부의 `README.md`, `data`, `docs`, `logs`, `results`를 저장소 루트에 합친다.

## 6. Commit message

`Align replication repository with final thesis`

Commit description:

- Adopt U.S. Residential REITs as the primary benchmark
- Retain Global USD Total Return as a supplementary benchmark
- Align return terminology and 2026 partial-year treatment
- Add thesis-table replication outputs
- Clarify non-contemporaneous platform-price comparisons
- Update limitations, source metadata, and snapshot documentation
