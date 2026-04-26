import requests
import random

# 공통 헤더 (차단 방지)
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 회차별 로또 번호 가져오기
def get_lotto_numbers(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=5)

        if res.status_code != 200:
            return []

        try:
            data = res.json()
        except:
            return []

        if "drwtNo1" in data:
            return [data[f"drwtNo{i}"] for i in range(1, 7)]
        else:
            return []

    except:
        return []


# 최근 3회차 가져오기 (직접 최신 회차 입력 방식)
def get_recent_3(draw_no):
    results = []
    for i in range(3):
        nums = get_lotto_numbers(draw_no - i)
        if nums:
            results.append(nums)
    return results


# 번호 생성
def generate_numbers(recent_draws):
    # 1~39
    all_numbers = set(range(1, 40))

    # 최근 3회차 번호 합치기
    used_numbers = set(n for draw in recent_draws for n in draw)

    # 미출현 번호
    available = sorted(list(all_numbers - used_numbers))

    print("최근 3회차 번호:", recent_draws)
    print("사용된 번호:", sorted(used_numbers))
    print("사용 가능한 번호:", available)

    if len(available) < 6:
        print("❌ 가능한 숫자가 부족합니다.")
        return

    result = sorted(random.sample(available, 6))
    print("🎯 추천 번호:", result)


# 실행
if __name__ == "__main__":
    latest_draw = int(input("최신 회차를 입력하세요: "))
    recent = get_recent_3(latest_draw)
    generate_numbers(recent)
