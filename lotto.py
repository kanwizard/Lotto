import requests
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 로또 번호 가져오기 (안정)
def get_lotto_numbers(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=5)

        if res.status_code != 200:
            return []

        data = res.json()

        if "drwtNo1" in data:
            return [data[f"drwtNo{i}"] for i in range(1, 7)]

    except:
        return []

    return []


# 최근 3회차
def get_recent_3(latest):
    results = []

    for i in range(3):
        nums = get_lotto_numbers(latest - i)
        if nums:
            print(f"{latest - i}회: {nums}")
            results.append(nums)
        else:
            print(f"{latest - i}회 실패")

    return results


# 번호 생성
def generate_numbers(recent_draws):
    all_numbers = set(range(1, 40))
    used = set(n for draw in recent_draws for n in draw)

    available = sorted(list(all_numbers - used))

    print("\n사용 가능:", available)

    if len(available) < 6:
        print("❌ 숫자 부족")
        return

    print("🎯 추천:", sorted(random.sample(available, 6)))


# 실행
if __name__ == "__main__":
    latest = int(input("최신 회차 입력: "))

    recent = get_recent_3(latest)

    if not recent:
        print("❌ 데이터 못 가져옴")
    else:
        generate_numbers(recent)
