import requests
from bs4 import BeautifulSoup
import random
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://dhlottery.co.kr/gameResult.do?method=byWin"


# 최신 회차 가져오기
def get_latest_draw():
    try:
        res = requests.get(BASE_URL, headers=HEADERS, timeout=5)

        if res.status_code != 200:
            return 0

        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.select_one("h4 strong")
        if not title:
            return 0

        match = re.search(r"\d+", title.text)
        return int(match.group()) if match else 0

    except:
        return 0


# 특정 회차 번호 크롤링
def get_draw_numbers(draw_no):
    try:
        url = f"{BASE_URL}&drwNo={draw_no}"
        res = requests.get(url, headers=HEADERS, timeout=5)

        if res.status_code != 200:
            return []

        soup = BeautifulSoup(res.text, "html.parser")

        numbers = []
        for i in range(1, 7):
            tag = soup.select_one(f"#drwtNo{i}")
            if not tag:
                return []
            numbers.append(int(tag.text))

        return numbers

    except:
        return []


# 최근 3회차 가져오기
def get_recent_3():
    latest = get_latest_draw()

    if latest == 0:
        print("❌ 최신 회차 가져오기 실패")
        return []

    print(f"📌 최신 회차: {latest}")

    results = []

    for i in range(3):
        draw_no = latest - i
        nums = get_draw_numbers(draw_no)

        if nums:
            print(f"{draw_no}회: {nums}")
            results.append(nums)
        else:
            print(f"{draw_no}회 크롤링 실패")

        time.sleep(0.5)  # 서버 부담 방지

    return results


# 번호 생성
def generate_numbers(recent_draws):
    all_numbers = set(range(1, 40))
    used_numbers = set(n for draw in recent_draws for n in draw)

    available = sorted(list(all_numbers - used_numbers))

    print("\n🚫 최근 3회차 사용된 번호:", sorted(used_numbers))
    print("✅ 사용 가능한 번호:", available)

    if len(available) < 6:
        print("❌ 가능한 숫자 부족")
        return

    result = sorted(random.sample(available, 6))
    print("🎯 추천 번호:", result)


# 실행
if __name__ == "__main__":
    recent = get_recent_3()

    if not recent:
        print("❌ 데이터 수집 실패 (네트워크 or 차단)")
    else:
        generate_numbers(recent)
