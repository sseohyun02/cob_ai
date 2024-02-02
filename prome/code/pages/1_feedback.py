import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title='chatGPT API 서비스 개발',
    page_icon='🧠'
)
st.title('직장인 맞춤 대화 피드백')
st.subheader('현재 상황과 보내고 싶은 메세지를 입력하세요.\n당신이 보낸 메세지에 대한 피드백이 제공됩니다')

#사이드바
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    process = st.button("Process")
    my_api_key = openai_api_key
    #버튼을 누르면 구동되는 부분
    if process:
        #키 미입력 시 제공되는 알람
        if not openai_api_key:
            st.info("계속하기 위해 API key를 입력하여 주십시오")
            st.stop()
        my_api_key = openai_api_key
        if openai_api_key != "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":
            st.info("올바르지 않은 API key 입니다. 유효한 API key를 .")

#opanai 불러오기
client = OpenAI(
  api_key = my_api_key
)

## 답변 요청 함수
def request_chat_completion(
        prompt,
        system_role='당신은 직장 내 갈등을 해결해주는 도우미입니다.',
        model='gpt-3.5-turbo',
        stream=False
):
    messages = [
        {'role':'system', 'content':system_role},
        {'role':'user','content':prompt}
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream
    )
    return completion

##스트리밍 함수
def print_streaming_response(completion):
     message=""
     placeholder = st.empty()
     for chunk in completion:
         if chunk.choices[0].delta.content is not None:
             message += chunk.choices[0].delta.content
             placeholder.markdown(message+'|')
     placeholder.markdown(message)
     return message
 #UI구현

##예시 데이터로 채워주는 기능
auto_complete = st.toggle('예시로 채우기')
##예시데이터 제공
example = {
    'company_position': '과장',
    'company_sit': '과장님이 20년도 서류 처리를 부탁하셨는데 나는 21년 입사라 관련 내용을 몰라 거절해야하는데 무책임해보일까봐 걱정이 되는 상황',
    'company_desc': '제가 21년에 입사를 하여서 어떻게 업무 처리를 해야할지 모르겠습니다',
    'keywords': ['죄송', '감사', '실례']
}
prompt_template = """
입력받은 청자에게 메세지를 보내기 위한 텍스트를 {num}개 생성해주세요.
청자에 맞는 말투를 사용하여 작성하여주세요.
예의 바르고 상대를 배려하며 공식적인 말투로 작성해주세요.
반드시 공적인 말투로 간결하게 작성해주세요.
업무용어도 적절히 섞어서 작성해주면 좋겠어요.
상황에 맞는 답을 할 수 있도록 작성해주세요.
반드시 {max_length} 단어 이내로 작성해주세요.
키워드가 주어질 경우 키워드 중 하나는 반드시 포함해주세요.
---
청자: {company_position}
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
        company_position = st.text_input(
            '대화 상대',
            value = example['company_position'] if auto_complete else ''
        )
    with col2:
        max_length = st.number_input(
            label='최대 단어 수',
            min_value=10,
            max_value=25,
            step=1,
            value=15
        )
    with col3:
        num = st.number_input(
            label='생성할 메세지 수',
            min_value=1,
            max_value=10,
            step=1,
            value=2
        )
    company_sit = st.text_input(
        '상황',
        value = example['company_sit'] if auto_complete else ''
    )
    company_desc = st.text_input(
        '메세지',
        value = example['company_desc'] if auto_complete else ''
    )

    st.text('반드시 하나는 포함해야 할 키워드가 있다면 최대 3개까지 입력해주세요')
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
    submit = st.form_submit_button(label='submit')

##제출시 예외상황 처리 및 출력
if submit:
    if not company_position:
        st.error('상대방의 직급을 추가해주세요')
    elif not company_sit:
        st.error('상황을 추가해주세요')
    elif not company_desc:
        st.error('메세지를 추가해주세요')
    else:
        keywords = [keyword_1, keyword_2, keyword_3]
        keywords = [x for x in keywords if x]
        prompt = prompt_template.format(
            company_position=company_position,
            company_sit=company_sit,
            company_desc=company_desc,
            max_length=max_length,
            num=num,
            keywords=keywords
        )
        system_role='당신은 나의 메세지를 피드백 해주는 도우미이자 상황에 알맞은 해결책을 제공해주는 솔루셔너입니다.'
        with st.spinner('피드백을 제공 중입니다'):
            response = request_chat_completion(
                prompt=prompt,
                system_role=system_role,
                stream=True
            )
        print_streaming_response(response)