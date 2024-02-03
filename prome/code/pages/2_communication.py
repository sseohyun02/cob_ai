import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append(result)

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

st.session_state.setdefault(
    'past', 
    ['업무 분담 관련 상황에 대해 이야기를 시작해보세요',
     '안녕하세요']
)
st.session_state.setdefault(
    'generated', 
    [{'type': 'normal', 'data': '안녕하세요'},
     {'type': 'table', 'data': '좋은 아침이에요.\n업무 분담 관련 하고싶은 이야기가 있으시다고요'}]
)

st.title("대화 시뮬레이션")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    generated_messages = st.session_state.get('generated', [])
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear message", on_click=on_btn_click)

with st.container():
    user_input = st.text_input("User Input:", on_change=on_input_change, key="user_input")

#assistant 생성
from openai import OpenAI
client = OpenAI(api_key='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')

my_assistant = client.beta.assistants.create(
    instructions="""
    당신은 나의 직장 상사입니다. 
    나의 직장 상사는 차갑고 엄격한 원칙주의자입니다.
    당신과 업무 분담 관련 대화를 하고싶어요.
    제 말에 대한 답을 해주세요.
    """,
    name="superior",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)

assistant_id = my_assistant.id

#thread 생성
empty_thread = client.beta.threads.create()
thread_id = empty_thread.id

#메세지 생성
thread_message = client.beta.threads.messages.create(
  thread_id,
  role="user",
  content=user_input
)

#실행
run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id
)
run_id=run.id

# 실행이 완료될 때까지 대기
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    if run.status == "completed":
        break

# 출력
thread_messages = client.beta.threads.messages.list(thread_id)
result = thread_messages.data[0].content[0].text.value