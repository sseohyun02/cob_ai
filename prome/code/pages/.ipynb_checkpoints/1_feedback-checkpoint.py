import streamlit as st
from common import request_chat_completion, print_streaming_response

st.set_page_config(
    page_title='chatGPT API 서비스 개발',
    page_icon='🧠'
)
st.title('직장인 맞춤 대화 피드백')
st.subheader('현재 상황과 보내고 싶은 메세지를 입력하세요.\n당신이 보낸 메세지에 대한 피드백이 제공됩니다')

##예시 데이터로 채워주는 기능
auto_complete = st.toggle('예시로 채우기')
##예시데이터 제공
example = {
    'company_name': '네이버',
    'company_sit': '상사와의 의견 차이로 갈등이 있는 상황',
    'company_desc': '제 생각에는 기획안 A에서 필요하지 않은 과정들을 제외시키는 것이 좋을  것 같습니다.',
    'keywords': ['감사', '실례', '존중']
}
prompt_template = """
직장 상사에게 메세지를 보내기 위한 텍스트를 {num}개 생성해주세요.
예의 바르고 상대를 배려하며 공식적인 말투로 작성해주세요.
회사에서 사용하는 단어를 이용하여 작성해주세요
상황에 맞게 작성해주세요.
반드시 {max_length} 단어 이내로 작성해주세요
키워드가 주어질 경우 키워드 중 하나는 반드시 포함해주세요.
---
회사명: {company_name}
상황: {company_sit} 
메세지: {company_desc}
키워드: {keywords}
---
""".strip()

##화면 구상
with st.form('form'):
    ##col: 공간 낭비를 막기 위해 한 행에 표시하려고
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input(
            '회사명',
            # placeholder=example['company_name'],
            value = example['company_name'] if auto_complete else ''
        )
    with col2:
        max_length = st.number_input(
            label='최대 단어 수',
            min_value=5,
            max_value=20,
            step=1,
            value=10
        )
    with col3:
        num = st.number_input(
            label='생성할 스크립트 수',
            min_value=1,
            max_value=10,
            step=1,
            value=5
        )
    company_sit = st.text_input(
        '상황',
        value = example['company_sit'] if auto_complete else ''
    )
    company_desc = st.text_input(
        '메세지',
        value = example['company_desc'] if auto_complete else ''
    )

    st.text('반드시 하나는 포함해야 할 키워드를 최대 3개까지 입력해주세요')
    col1, col2, col3 = st.columns(3)
    with col1:
        keyword_1 = st.text_input(
            label='keyword 1',
            ##placeholder: 칸 안에 그림자처럼 표시
            placeholder='키워드 1',
            value = example['keywords'][0] if auto_complete else ''
        )
    with col2:
        keyword_2 = st.text_input(
            label='keyword 2',
            placeholder='키워드 2',
            value=example['keywords'][1] if auto_complete else ''
        )
    with col3:
        keyword_3 = st.text_input(
            label='keyword 3',
            placeholder='키워드 3',
            value=example['keywords'][2] if auto_complete else ''
        )
    submit = st.form_submit_button('submit')

##제출시 예외상황 처리 및 출력
if submit:
    if not company_name:
        st.error('회사 명을 추가해주세요')
    elif not company_sit:
        st.error('상황을 추가해주세요')
    elif not company_desc:
        st.error('메세지를 추가해주세요')
    else:
        keywords = [keyword_1, keyword_2, keyword_3]
        keywords = [x for x in keywords if x]
        prompt = prompt_template.format(
            company_name=company_name,
            company_sit=company_sit,
            company_desc=company_desc,
            max_length=max_length,
            num=num,
            keywords=keywords
        )
        system_role='당신은 나의 메세지를 피드백 해주는 도우미입니다.'
        with st.spinner('피드백을 제공 중입니다'):
            response = request_chat_completion(
                prompt=prompt,
                system_role=system_role,
                stream=True
            )
        # generated_text = response['choices'][0]['message']['content']
        # st.text(response)
        # st.success('피드백을 제공할 수 있습니다.')
        print_streaming_response(response)

# print('click_submit')