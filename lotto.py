import requests
from bs4 import BeautifulSoup
import random
import re
from collections import Counter

BASE_URL = "https://dhlottery.co.kr/gameResult.do?method=byWin"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 최신 회차 가져오기
def get_latest_draw_no():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.select_one("h4 strong").text
    return int(re.search(r"\d+", title).group())


# 회차별 번호 가져오기
def get_lotto_numbers(draw_no):
    url = f"{BASE_URL}&drwNo={draw_no}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    return [int(soup.select_one(f"#drwtNo{i}").text) for i in range(1, 7)]


# 가중치 생성 (콜드 번호 우대)
def calculate_weights(recent_draws, number_range):
    counter = Counter(n for draw in recent_draws for n in draw)

    weights = {}
    for n in number_range:
        freq = counter.get(n, 0)
        # 등장 적을수록 높은 가중치 (1 / (freq + 1))
        weights[n] = 1 / (freq + 1)

    return weights


# 가중 랜덤 추출 (중복 없이)
def weighted_sample(numbers, weights, k=6):
    selected = []
    pool = numbers[:]

    for _ in range(k):
        total = sum(weights[n] for n in pool)
        r = random.uniform(0, total)

        upto = 0
        for n in pool:
            upto += weights[n]
            if upto >= r:
                selected.append(n)
                pool.remove(n)
                break

    return sorted(selected)


def generate_lotto_sets(set_count=5):
    latest = get_latest_draw_no()
    print(f"최신 회차: {latest}")

    # 최근 4회차 수집
    recent_draws = []
    for i in range(4):
        nums = get_lotto_numbers(latest - i)
        recent_draws.append(nums)
        print(f"{latest - i}회: {nums}")

    number_range = list(range(1, 46))  # 로또는 1~45
    weights = calculate_weights(recent_draws, number_range)

    print("\n추천 번호:")

    for i in range(set_count):
        # 70%는 가중 랜덤, 30%는 완전 랜덤 섞기
        if random.random() < 0.7:
            result = weighted_sample(number_range, weights, 6)
        else:
            result = sorted(random.sample(number_range, 6))

        print(f"{i+1}번 조합:", result)


if __name__ == "__main__":
    # 생성할 조합 개수 설정
    generate_lotto_sets(set_count=5)
