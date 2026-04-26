import requests
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 안전한 요청 함수
def safe_request(url, params):
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=3)

        if res.status_code != 200:
            return None

        # JSON 파싱 안전 처리
        try:
            return res.json()
        except:
            return None

    except requests.exceptions.Timeout:
        print("⏱️ 요청 시간 초과")
        return None
    except requests.exceptions.RequestException:
        print("❌ 요청 실패")
        return None


# 로또 번호 가져오기
def get_lotto_numbers(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    data = safe_request(url, params)

    if not data:
        print(f"{draw_no}회차 데이터 없음")
        return []

    if "drwtNo1" in data:
        return [data[f"drwtNo{i}"] for i in range(1, 7)]

    return []


# 최근 3회차
def get_recent_3(draw_no):
    results = []

    for i in range(3):
        nums = get_lotto_numbers(draw_no - i)

        if nums:
            results.append(nums)
        else:
            print(f"{draw_no - i}회차 스킵")

    return results


# 번호 생성
def generate_numbers(recent_draws):
    all_numbers = set(range(1, 40))
    used = set(n for draw in recent_draws for n in draw)
    available = sorted(list(all_numbers - used))

    print("\n최근 3회차:", recent_draws)
    print("가능 번호:", available)

    if len(available) < 6:
        print("❌ 숫자 부족")
        return

    result = sorted(random.sample(available, 6))
    print("🎯 추천:", result)


# 실행
if __name__ == "__main__":
    latest = int(input("최신 회차 입력: "))

    recent = get_recent_3(latest)

    if not recent:
        print("❌ 데이터를 가져오지 못했습니다. (네트워크 or 차단 문제)")
    else:
        generate_numbers(recent)
