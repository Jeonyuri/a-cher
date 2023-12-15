import streamlit as st
from streamlit_chat import message
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import base64

# SentenceTransformer 모델을 캐시하는 함수 정의
@st.cache(allow_output_mutation=True)
def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

# 데이터셋을 로드하고 'embedding' 열을 JSON에서 Python 객체로 변환하는 함수 정의
@st.cache(allow_output_mutation=True)
def get_dataset():
    df = pd.read_excel("C:\\Users\\박채은\\Downloads\\500question.xlsx")
    df['embedding'] = df['embedding'].apply(json.loads)
    return df

# 모델과 데이터셋 로드
model = cached_model()
df = get_dataset()

# 사이드바: 날짜 선택
st.sidebar.header('상담 기록 조회')
selected_date = st.sidebar.date_input('날짜', pd.Timestamp.now().date(), min_value=pd.Timestamp.now().date())

# 대화 상단 부분: 챗봇 소개
st.header('심리상담 챗봇')
st.markdown("오픈소스 기초설계 프로젝트")

# 대화 기록 저장을 위한 session_state 초기화
if 'generated' not in st.session_state:
    st.session_state['generated'] = {}

if 'past' not in st.session_state:
    st.session_state['past'] = {}

# 사용자 입력과 전송 버튼을 가진 폼 생성
form = st.form('form', clear_on_submit=True)
user_input = form.text_input('당신: ', '')
submitted = form.form_submit_button('전송')

# 사용자가 입력하고 전송한 경우
if submitted and user_input:
    # 입력 문장을 임베딩하여 가장 유사한 답변을 찾음
    embedding = model.encode(user_input)

    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]

    # 선택한 날짜에 대화 기록이 없을 경우 초기화
    if selected_date not in st.session_state['past']:
        st.session_state['past'][selected_date] = []
        st.session_state['generated'][selected_date] = []

    # 대화 기록에 사용자 입력과 챗봇 답변 추가
    st.session_state['past'][selected_date].append(user_input)
    st.session_state['generated'][selected_date].append(answer['챗봇'])

# 상담 기록 페이지: 상담 내용 다운로드
if st.sidebar.button('상담 기록 다운로드'):
    if selected_date in st.session_state['past']:
        # 선택된 날짜의 상담 내용을 파일로 다운로드
        download_filename = f"conversation_{selected_date}.txt"
        download_text = "상담 내용 요약\n"
        for i in range(len(st.session_state['past'][selected_date])):
            download_text += f"사용자: {st.session_state['past'][selected_date][i]}\n"
            if len(st.session_state['generated'][selected_date]) > i:
                download_text += f"챗봇: {st.session_state['generated'][selected_date][i]}\n"
        
        st.markdown("---")
        st.markdown("### 상담 내용 다운로드")
        st.markdown("아래 버튼을 클릭하여 상담 내용을 다운로드하세요.")
        st.markdown(f'<a href="data:file/txt;base64,{base64.b64encode(download_text.encode()).decode()}" download="{download_filename}">상담 내용 다운로드</a>', unsafe_allow_html=True)
    else:
        st.warning(f"선택한 날짜 {selected_date}에 대한 상담 기록이 없습니다.")

# 대화 내용 표시: 선택한 날짜의 상담 내용
if selected_date in st.session_state['past']:
    st.title(f"{selected_date} 상담 내용")
    for i in range(len(st.session_state['past'][selected_date])):
        message(st.session_state['past'][selected_date][i], is_user=True, key=f"{selected_date}_main_{i}_user")
        if len(st.session_state['generated'][selected_date]) > i:
            message(st.session_state['generated'][selected_date][i], key=f"{selected_date}_main_{i}_bot")
else:
    st.warning(f"선택한 날짜 {selected_date}에 대한 상담 내용이 없습니다.")




