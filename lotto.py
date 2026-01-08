import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# 로그인
def login():
    st.title("🔐 로그인")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("확인"):
        if password == "860716":
            st.success("로그인 성공!")
            st.session_state.logged_in = True
            return True
        else:
            st.error("비밀번호가 틀렸습니다.")
            return False
    return False

def get_lotto_numbers_html(draw_number):
    # 당첨 결과 HTML 페이지
    url = f"https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={draw_number}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 당첨번호 DOM 파싱
    numbers = []
    elems = soup.select(".nums .num")  # 당첨번호 CSS 선택자
    for e in elems:
        try:
            num = int(e.get_text().strip())
            numbers.append(num)
        except:
            pass
    return numbers

def get_recent_lotto_numbers(latest_draw):
    data = []
    for i in range(latest_draw, latest_draw-5, -1):
        nums = get_lotto_numbers_html(i)
        if nums:
            data.append(nums)
    return data

def calculate_frequency(recent_numbers):
    freq = {i: 0 for i in range(1, 46)}
    for nums in recent_numbers:
        for n in nums:
            freq[n] += 1
    return freq

def generate_lotto_numbers(frequency, num_combinations=5):
    population = []
    for num, freq in frequency.items():
        weight = 1/(freq+1)
        population.extend([num] * int(weight*100))

    combinations = []
    while len(combinations) < num_combinations:
        selected = set()
        while len(selected) < 6:
            selected.add(random.choice(population))
        combinations.append(sorted(list(selected)))
    return combinations

st.set_page_config(page_title="로또 번호 생성", page_icon="🎰")

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if not login():
            st.stop()

    st.title("🎰 로또 번호 생성기 (HTML 크롤링)")

    latest_draw = st.number_input("🔢 최신 회차 입력", value=1100, min_value=1, step=1)
    num_combinations = st.number_input("🔢 조합 갯수 입력", value=5, min_value=1, step=1)
    if st.button("🚀 번호 생성"):
        recent_numbers = get_recent_lotto_numbers(latest_draw)
        st.write("📅 최근 5회차 번호:", recent_numbers)

        freq = calculate_frequency(recent_numbers)
        lotto_combinations = generate_lotto_numbers(freq, num_combinations)
        for i, comb in enumerate(lotto_combinations, 1):
            st.markdown(f"**{i}번 조합:** {comb}")

if __name__ == "__main__":
    main()
