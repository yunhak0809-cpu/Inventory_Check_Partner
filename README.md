# Inventory Check Partner

Python 기반 RMA 미회수 재고 자동 분석 프로그램

## 프로젝트 배경

실제 RMA 물류 업무에서는 업체별 출고된 제품의 회수 여부를
엑셀로 수작업 확인해야 했습니다.

반복적인 확인 업무를 줄이기 위해 Python으로 자동화 프로그램을 제작했습니다.

---

## 주요 기능

- 업체명 자동 추출
- 미회수 제품 자동 탐색
- 출고 후 경과일 계산
- 품번별 미회수 수량 집계
- 콘솔 보고서 출력

---

## 기술 스택

- Python
- pandas
- openpyxl

---

## 실행 방법

```bash
py main.py "sample_inventory.xlsx"

## 실행 결과

Test_Result.PNG 참고
