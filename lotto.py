import streamlit as st
import requests
import random

# 로그인 기능 추가
def login():
    st.title("🔐 로그인")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    
    # 비밀번호 확인 버튼
    if st.button("확인"):
        if password == "860716":  # 원하는 비밀번호로 변경 가능
            st.success("로그인 성공!")
            st.session_state.logged_in = True  # 로그인 상태 저장
            st.session_state.login_success = True  # 로그인 성공 상태 저장
            return True
        else:
            st.error("비밀번호가 틀렸습니다.")
            return False
    return False  # 로그인 상태가 아닐 경우 계속 대기

# 동행복권 API를 이용하여 당첨 번호를 가져오는 함수
def get_lotto_numbers_by_draw(draw_number):
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber'
    params = {'drwNo': draw_number}
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get('returnValue') == 'success':
        return [data[f'drwtNo{i}'] for i in range(1, 7)]
    else:
        st.error(f"Error retrieving data for draw number {draw_number}")
        return []

# 최근 5회차 로또 번호 가져오기
def get_recent_lotto_numbers(latest_draw):
    return [get_lotto_numbers_by_draw(latest_draw - i) for i in range(5)]

# 번호 출현 빈도 계산
def calculate_frequency(recent_numbers):
    frequency = {i: 0 for i in range(1, 46)}  # 1부터 45까지 번호의 출현 빈도
    for numbers in recent_numbers:
        for number in numbers:
            frequency[number] += 1
    return frequency

# 번호 추첨: 확률 기반으로 랜덤 번호 생성
def generate_lotto_numbers(frequency, num_combinations=5):
    # 번호와 해당 번호의 가중치 계산
    weighted_numbers = []
    for number, freq in frequency.items():
        # 출현한 번호일수록 가중치가 낮고, 출현하지 않은 번호는 가중치가 높아짐
        weight = 1 / (freq + 1)  # 출현 횟수가 많을수록 가중치가 낮아짐
        weighted_numbers.append((number, weight))  # 번호와 가중치를 튜플로 저장
    
    # 번호들을 가중치 기반으로 확률적으로 고르기 위한 리스트로 변환
    population = []
    for number, weight in weighted_numbers:
        # 가중치에 따라 번호를 추가 (가중치가 낮은 번호는 적게 추가)
        population.extend([number] * int(weight * 100))  # 가중치를 기반으로 확장

    # 중복 없이 지정된 개수만큼 번호 추첨
    combinations = []
    while len(combinations) < num_combinations:
        selected_numbers = set()
        while len(selected_numbers) < 6:  # 하나의 조합에서 6개의 번호를 추첨
            selected_numbers.add(random.choice(population))  # 가중치 기반 번호 추출
        combinations.append(sorted(list(selected_numbers)))  # 번호는 오름차순으로 정렬하여 추가
    
    return combinations

st.set_page_config(page_title="로또 번호 생성", page_icon="🎰", layout="centered")

# 웹앱 시작
def main():
    # 로그인 상태 확인
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # 초기 로그인 상태 설정
    if 'login_success' not in st.session_state:
        st.session_state.login_success = False  # 로그인 성공 여부 초기화

    # 로그인 상태가 아니라면 로그인 화면 표시
    if not st.session_state.logged_in:
        if not login():
            st.stop()  # 로그인 상태가 아니라면 앱 종료
    
    # 로그인 성공 후 로그인 화면 숨기기
    if st.session_state.login_success:
        st.session_state.logged_in = True  # 로그인 상태로 변경
        st.session_state.login_success = False  # 로그인 성공 플래그 초기화

    st.title("🎰 로또 번호 생성")

    st.markdown("""
    <h3 style="font-size: 20px;">로또 번호 생성기</h3>
    <p style="font-size: 18px;">
        입력한 회차부터 이전 5회차 까지의 당첨 번호를 분석하여 생성함
    </p>
    """, unsafe_allow_html=True)
        
    # 최신 회차 번호를 입력받기
    latest_draw = st.number_input("🔢 최신 회차 입력", min_value=1, step=1)

    # 출력할 번호 조합의 개수 입력 받기
    num_combinations = st.number_input("🔢 조합 갯수 입력", min_value=1, step=1, value=5)
    
    # 번호 생성 버튼
    generate_button = st.button("🚀 번호 생성")
    
    if generate_button:
        if latest_draw > 0 and num_combinations > 0:
            # 최신 회차 번호를 가져옵니다.
            recent_numbers = get_recent_lotto_numbers(latest_draw)  # 최근 5회차 번호 가져오기
            
            # 최근 5회차 당첨 번호 출력
            st.subheader("📅 최근 5회차 당첨 번호")
            for i, numbers in enumerate(recent_numbers, 1):
                st.markdown(f"**{latest_draw - i + 1}회차:** {', '.join(map(str, numbers))}")
            
            # 출현 빈도 계산
            frequency = calculate_frequency(recent_numbers)

            # 가중치 기반 번호 추첨
            lotto_combinations = generate_lotto_numbers(frequency, num_combinations)
            
            st.subheader(f"🎯 {num_combinations}개의 랜덤 번호 조합:")
            for idx, combination in enumerate(lotto_combinations, 1):
                # 번호 조합을 굵은 글씨와 색상으로 출력 (파란색으로 표시)
                st.markdown(f"<b style='color:#1E90FF'>{idx}번째 조합</b>: <b style='color:#FF0000'>{', '.join(map(str, combination))}</b>", unsafe_allow_html=True)
        else:
            st.error("최신 회차 번호와 조합 개수는 1 이상의 정수여야 합니다.")

if __name__ == "__main__":
    main()
