# lib 설치 ###########
# pip install openai
# pip install streamlit
# pip install python-dotenv
# pip install pillow
# 실행 ###############
# streamlit run 2-2.docent_img_url.py
######################

from openai import OpenAI 
# openai의 모델을 가져와 사용하기 위한 aip 라이브러리
import streamlit as st 
# 웹 어플리케이션을 만들기 위한 프레임워크
# 웹 서비스에서의 프레임워크
# 웹 어플리케이션(api, 웹사이트)를 개발할 때 필요한 기본 골격과 라이브러리, 필요한 도구를 제공하여 개발을 좀 더 편리하게 할 수 있도록 한다.
from dotenv import load_dotenv
# .env파일에서 환경변수(api키 등)를 로드할 수 있도록 한다.
import os
# 환경변수를 가져올 때 사용
from PIL import Image
# 이미지 처리 라이브러리
from io import BytesIO
# 이미지 데이터를 포함한 바이너리 데이터를 파일처럼 다루되 디스크에 저장하지 않고 메모리에서 처리할 수 있게 해주는 도구다.
import base64 # 바이너리 데이터 (이미지, 오디오 파일)을 텍스트 형태로 변환한다.
              # 바이너리 데이터는 0과 1사이로 이루어졌지만 base64sms dlfmf a-z, A-Z, 0-9, 같은 64개의 문자로 표현한다.

# .env 파일 경로 지정 
load_dotenv(override=True)
# .env 파일에 저장된 환경 변수를 파이썬 프로그램에서 읽어서 os.GETENV에 로드해줍니다.
# Open AI API 키 설정하기
api_key = os.getenv('OPENAI_API_KEY')

# OpenAI 객체 생성
client = OpenAI(api_key = api_key)

# 1. 껍데기 판들기

# 웹 사이트 상단에 노출될 웹 사이트 제목설정
st.title("AI 도슨트: 이미지를 설명해드려요!")

tab1, tab2 = st.tabs(["이미지 URL 입력", "이미지 파일 업로드"])

# tab1: 사용자가 이미지 URL을 입력할 수 있는 공간
# tab2: 사용자가 이미지를 직접 업로드할 수 있는 공간

with tab1:
    # st.text_area()는 사용자의 입력을 받는 커다란 텍스트 칸을 만든다. height는 이 텍스트 칸의 높이.
    input_url = st.text_area("이미지 URL을 입력하세요.", height=70)
    # 주어진 이미지 주소로부터 GPT4V의 설명을 얻는 함수.
    def ai_describe(image_url):
        # gpt에 요청하였을 때는 print와 같은 출력행위를 하면 안됨
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
                # ai에게 사용자가 보내는 인터페이스
                {"type": "image_url",
                #  OpenAI가 해당 URL의 이미지를 분석하도록 설정
                    "image_url": {"url": image_url,},
                },
            ],
            }
        ],
        max_tokens=1024, # 최대 1024개의 토큰을 사용하여 설명을 생성
        )
        result = response.choices[0].message.content
        print("결과 >> ", result)
        return result
        # st.button()을 클릭하는 순간 st.button()의 값은 True가 되면서 if문 실행
    if st.button("해설", key="explanation_button_1"):

        # st.text_area()의 값이 존재하면 input_url의 값이 True가 되면서 if문 실행
        if input_url:
            try:
                # st.image()는 기본적으로 이미지 주소로부터 이미지를 웹 사이트 화면에 생성됨
                st.image(input_url, width=300)
                
                # describe() 함수는 GPT4V의 출력 결과를 반환함
                result = ai_describe(input_url)

                # st.success()는 텍스트를 웹 사이트 화면에 출력하되, 초록색 배경에 출력
                st.success(result)
            except:
                st.error("요청 오류가 발생했습니다!")
        else:
            st.warning("텍스트를 입력하세요!") # 화면 상으로 노란색 배경으로 출력

with tab2:
    # 이미지를 Base64로 변환하는 함수 #url일 때는 바이너리 파일이 아니기 때문이다.
    # url은 서버에서 처리되기 때문에 변환할 필요없음.
    # Base64 인코딩은 바이너리 데이터를 ASCII 문자열로 변환하는 표준 방식
    def encode_image(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")  # PNG 형식으로 변환
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 이미지 파일을 분석하여 설명을 반환하는 함수
    def ai_describe(image):
        try:
            base64_image = encode_image(image)  
            # gpt가 인식할 수 있도록 이미지를 Base64로 변환하고 넘겼다. 
            # gpt는 바이너리 파일(사진, 오디오)는 인식할 수 없다.
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "이 이미지에 대해서 자세하게 설명해 주세요."},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                        ],
                    }
                ],
                max_tokens=1024,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"오류 발생: {str(e)}"
        
        # 웹 앱 UI 설정

    # 파일 업로드 위젯
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 업로드된 이미지 표시
        st.image(uploaded_file, width=300)
        
        # 이미지 설명 요청 버튼
        if st.button("해설", key="explanation_button_2"):
            image = Image.open(uploaded_file)  # PIL 이미지 열기
            
            # GPT-4V를 이용한 이미지 분석 수행
            result = ai_describe(image)
            st.success(result)