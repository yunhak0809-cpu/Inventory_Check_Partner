import argparse
from pathlib import Path
from datetime import date

import pandas as pd


def get_partner_name(file_path):
    name = Path(file_path).stem

    if "누적현황" in name:
        name = name.split("누적현황")[0].strip()

    name = name.rstrip("_").strip()

    return name


def parse_korean_date(value):
    if pd.isna(value):
        return pd.NaT

    # 이미 날짜형이면 그대로 사용
    if isinstance(value, (pd.Timestamp, date)):
        return pd.to_datetime(value)

    value = str(value).strip()

    if value == "" or value == "이전 자료 품목":
        return pd.NaT

    # 2024-03-20 00:00:00 같은 문자열 처리
    parsed = pd.to_datetime(value, errors="coerce")
    if not pd.isna(parsed):
        return parsed

    # 6월 24일 같은 문자열 처리
    value = value.replace(" ", "")

    try:
        return pd.to_datetime(
            f"{date.today().year}년{value}",
            format="%Y년%m월%d일"
        )
    except Exception:
        return pd.NaT


def check_unreturned(file_path):
    partner_name = get_partner_name(file_path)

    df = pd.read_excel(
        file_path,
        header=5,
        usecols="C:M"
    )

    df = df.dropna(axis=1, how="all")

    part_col = "TG 품번"
    out_date_col = "업체 출고일"
    in_date_col = "RMA 수리 후 입고 일"

    df["출고일변환"] = df[out_date_col].apply(parse_korean_date)
    df["입고일변환"] = df[in_date_col].apply(parse_korean_date)

    # 입고일이 없는 것만 미회수로 판단
    unreturned = df[df["입고일변환"].isna()].copy()

    # 품번이 비어 있는 행 제거
    unreturned = unreturned[unreturned[part_col].notna()].copy()

    today = pd.Timestamp(date.today())
    unreturned["경과일"] = (today - unreturned["출고일변환"]).dt.days

    print(f"\n{partner_name} 업체 출고 현황")
    print("=" * 60)
    print(f"{'TG 품번':<15}{'업체 출고일':<18}{'경과일'}")
    print("-" * 60)

    for _, row in unreturned.iterrows():
        tg_part = str(int(row[part_col]))

        if pd.isna(row["출고일변환"]):
            out_date = "이전 자료 품목"
            days = "-"
        else:
            out_date = row["출고일변환"].strftime("%Y-%m-%d")
            days = f"{int(row['경과일'])}일"

        print(
            f"{tg_part:<15}"
            f"{out_date:<18}"
            f"{days}"
    )


    print("=" *60)

    # ===========================
    # 품번별 집계
    # ===========================

    result = (
        unreturned
        .groupby(part_col)
        .size()
        .reset_index(name="미회수수량")
    )

    print("\n품번별 집계")
    print("-" * 35)

    for _, row in result.iterrows():

        tg_part = str(int(row[part_col]))

        print(
            f"{tg_part:<15}"
            f"{int(row['미회수수량'])} EA"
        )

    print("-" * 35)
    print(f"총 미회수 수량 : {result['미회수수량'].sum()} EA")

def main():
    print("업체별 미회수 재고 확인 프로그램을 실행합니다.")

    parser = argparse.ArgumentParser(
        description="업체별 출고 누적현황 파일에서 미회수 재고를 확인합니다."
    )

    parser.add_argument(
        "file",
        help="분석할 엑셀 파일 경로"
    )

    args = parser.parse_args()

    check_unreturned(args.file)


if __name__ == "__main__":
    main()