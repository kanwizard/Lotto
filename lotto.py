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
            return True
        else:
            st.error("비밀번호가 틀렸습니다.")
            return False
    return False  # 로그인 상태가 아닐 경우 계속 대기

# 동행복권 API를 이용하여 당첨 번호를 가져오는 함수
def get_lotto_numbers_by_draw(draw_number):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_number}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)

        # 상태 체크
        if response.status_code != 200:
            return []

        # 🔥 JSON 먼저 시도
        try:
            data = response.json()
        except:
            return []

        # 정상 응답 체크
        if not isinstance(data, dict):
            return []

        if data.get("returnValue") != "success":
            return []

        return [data.get(f"drwtNo{i}") for i in range(1, 7)]

    except Exception:
        return []

# 최근 4회차 로또 번호 가져오기
def get_recent_lotto_numbers(latest_draw):
    results = []

    for i in range(4):
        nums = get_lotto_numbers_by_draw(latest_draw - i)

        # ❗ 빈 데이터는 제외
        if nums and None not in nums:
            results.append(nums)
        else:
            st.warning(f"{latest_draw - i}회차 데이터 가져오기 실패")

    return results

# 로또 번호 생성 (1~39번 중에서 최근 당첨 번호 제외)
def generate_lotto_combinations(num_combinations, recent_numbers_flat):
    available_numbers = [num for num in range(1, 40) if num not in recent_numbers_flat]
    
    if len(available_numbers) < 6:
        st.error("선택 가능한 번호가 부족합니다. 조건을 다시 확인해주세요.")
        return []

    combinations = []
    while len(combinations) < num_combinations:
        combination = sorted(random.sample(available_numbers, 6))
        if combination not in combinations:
            combinations.append(combination)
    return combinations

st.set_page_config(page_title="로또 번호 생성", page_icon="🎰", layout="centered")

# 웹앱 시작
def main():
    # 로그인 상태 확인
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        if not login():
            st.stop()  # 로그인 상태가 아니라면 앱 종료
    
    st.title("🎰 로또 번호 생성")

    st.markdown("""
    <h3 style="font-size: 20px;">로또 번호 생성기</h3>
    <p style="font-size: 18px;">
        입력한 회차부터 이전 4회차 까지의 당첨 번호를 분석하여 생성함
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
            recent_numbers = get_recent_lotto_numbers(latest_draw)  # 최근 4회차 번호 가져오기
            
            # 최근 4회차 당첨 번호 출력
            st.subheader("📅 최근 4회차 당첨 번호")
            for i, numbers in enumerate(recent_numbers, 1):
                st.markdown(f"**{latest_draw - i + 1}회차:** {', '.join(map(str, numbers))}")
                        
	# 모든 최근 번호를 하나의 리스트로 평탄화
            recent_numbers_flat = [num for sublist in recent_numbers for num in sublist]

            # 조합 생성
            lotto_combinations = generate_lotto_combinations(num_combinations, recent_numbers_flat)

            st.subheader(f"🎯 {num_combinations}개의 랜덤 번호 조합:")
            for idx, combination in enumerate(lotto_combinations, 1):
                # 번호 조합을 굵은 글씨와 색상으로 출력 (파란색으로 표시)
                st.markdown(f"<b style='color:#1E90FF'>{idx}번째 조합</b>: <b style='color:#FF0000'>{', '.join(map(str, combination))}</b>", unsafe_allow_html=True)
        else:
            st.error("최신 회차 번호와 조합 개수는 1 이상의 정수여야 합니다.")

if __name__ == "__main__":
    main()
