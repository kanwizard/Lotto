import streamlit as st
import requests
import random

# 로그인 기능
def login():
    st.title("🔐 로그인")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    
    if st.button("확인"):
        if password == "860716":
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            return True
        else:
            st.error("비밀번호가 틀렸습니다.")
    return False


# 최신 회차 자동 가져오기
def get_latest_draw():
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1"
    res = requests.get(url)
    
    if res.status_code == 200:
        data = res.json()
        return data.get("drwNo", 0)
    return 0


# 로또 번호 가져오기 (수정된 부분 ⭐)
def get_lotto_numbers_by_draw(draw_number):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_number}

    try:
        res = requests.get(url, params=params, timeout=5)

        if res.status_code != 200:
            return []

        data = res.json()

        # 핵심 수정: returnValue 체크 제거하고 키 존재로 판단
        if "drwtNo1" in data:
            return [data[f"drwtNo{i}"] for i in range(1, 7)]
        else:
            return []

    except Exception as e:
        st.error(f"{draw_number}회차 오류: {e}")
        return []


# 최근 4회차
def get_recent_lotto_numbers(latest_draw):
    results = []
    for i in range(4):
        nums = get_lotto_numbers_by_draw(latest_draw - i)
        if nums:
            results.append(nums)
    return results


# 번호 생성
def generate_lotto_combinations(num_combinations, recent_numbers_flat):
    available_numbers = [n for n in range(1, 40) if n not in recent_numbers_flat]

    if len(available_numbers) < 6:
        st.error("선택 가능한 번호가 부족합니다.")
        return []

    combinations = []
    while len(combinations) < num_combinations:
        combo = sorted(random.sample(available_numbers, 6))
        if combo not in combinations:
            combinations.append(combo)

    return combinations


st.set_page_config(page_title="로또 번호 생성", page_icon="🎰")

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if not login():
            st.stop()

    st.title("🎰 로또 번호 생성기")

    # 최신 회차 자동 표시
    latest_auto = get_latest_draw()
    st.caption(f"📡 자동 감지 최신 회차: {latest_auto}")

    latest_draw = st.number_input("🔢 최신 회차 입력", min_value=1, value=latest_auto)
    num_combinations = st.number_input("🔢 조합 갯수", min_value=1, value=5)

    if st.button("🚀 번호 생성"):
        recent_numbers = get_recent_lotto_numbers(latest_draw)

        if not recent_numbers:
            st.error("데이터를 가져오지 못했습니다.")
            return

        st.subheader("📅 최근 4회차 당첨 번호")
        for i, nums in enumerate(recent_numbers):
            st.write(f"{latest_draw - i}회차: {nums}")

        # 평탄화
        flat = [n for sub in recent_numbers for n in sub]

        combos = generate_lotto_combinations(num_combinations, flat)

        st.subheader("🎯 추천 번호")
        for i, c in enumerate(combos, 1):
            st.markdown(
                f"<b style='color:#1E90FF'>{i}번</b> 👉 "
                f"<b style='color:#FF0000'>{', '.join(map(str, c))}</b>",
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
