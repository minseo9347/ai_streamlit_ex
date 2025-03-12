import base64
import io
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from PIL import Image
# openai 키값 로딩 환경변수 .env 저장
# openai key 값 프린트 해보기


# gpt api key 로딩하고, open api 객체 생성 # 달리모델
# 객체 변수를 통해 그림 그려달라 요청
  # 모델, 프롬프트(시스템, 유저: textarea -> value), 
# - gpt로부터 받은 이미지를 화면에 출력.



# .env 파일 환경변수 메모리에 로딩
load_dotenv(override=True)
# os.environ.get("env에 정의된 변수")
k = os.environ.get("OPENAI_API_KEY")
# print(api_key)

client = OpenAI(api_key=k)

# - 타이틀
st.title("그림 그리는 AI 서비스")
st.title("최고의 AI화가 :blue[CMS] :sunglasses:")
# 이미지 표시
st.image("image/robot_painter.png", width = 200, caption="Sunrise by the mountains")
# - 설명 텍스트 출력
st.write("원하는 그림을 말해주세요. 그리겠습니다.")
# - textarea : 영어로 그림 그리기 설명 프폼프트 입력
user_prompt = st.text_area("Please enter the description of the picture you want in English", height=200)

def get_image(user_prompt):
      response = client.images.generate(
          model="dall-e-3",
          prompt=user_prompt,
          size="1024x1024",
          quality="standard",
          response_format='b64_json',
          n=1,
      )
      response = response.data[0].b64_json # DALLE로부터 Base64, json 형태의 이미지를 얻음.
      image_data = base64.b64decode(response) # Base64, json으로 쓰여진 데이터를 이미지 형태로 변환
      image = Image.open(io.BytesIO(image_data)) # '파일처럼' 만들어진 이미지 데이터를 컴퓨터에서 볼 수 있도록 Open
      return image
# 2. 버튼 클릭했을 때, 사용자 이벤트
if st.button("painting"): # 버튼을 누른다면
   # print("버튼클릭 후")
    # 텍스트 값을 받눈다. (text) - 값이 있는지 체크 조건문
    if user_prompt:
        # 프롬프트 값 정상
        # openai에 그림그리기 메세지 보내기, 함수 호출
        # 그림그리기 메세지 보내기
        image = get_image(user_prompt)
        st.image(image, width = 300, caption="로봇 화가")
    else:
        st.write('텍스트 박스에 그림을 그릴 설명을 입력하세요')
        # 다시요청
        pass