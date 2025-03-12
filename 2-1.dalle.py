import streamlit as st
# - 타이틀
st.title("그림 그리는 AI 서비스")
st.title("_Streamlit_ is :blue[cool] :sunglasses:")
# 이미지 표시
st.image("image/robot_painter.png", caption="Sunrise by the mountains")
# - 설명 텍스트 출력
st.write("원하는 그림을 말해주세요. 그리겠습니다.")
st.write("원하는 이미지의 설명을 영어로 적어보세요.")
# - textarea : 영어로 그림 그리기 설명 프폼프트 입력
text = st.text_area("")

# 2. 버튼 클릭했을 때, 사용자 이벤트
st.button("painting")
# gpt api key 로딩하고, open api 객체 생성 # 달리모델
# 객체 변수를 통해 그림 그려달라 요청
  # 모델, 프롬프트(시스템, 유저: textarea -> value), 
# - gpt로부터 받은 이미지를 화면에 출력