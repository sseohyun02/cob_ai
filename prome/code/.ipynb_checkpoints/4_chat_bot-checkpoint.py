#########################################################################

import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

st.set_page_config(
    page_title = 'chatGPT API 서비스 개발',
    page_icon= '🧠'
)
st.title('대화 연습 시뮬레이션')

#사용자의 입력을 받는 코드
def on_input_change():
    user_input = st.session_state.user_input  #사용자가 입력한 값이 저장되어있음
    st.session_state.past.append(user_input)  #기존 리스트에 추가
    st.session_state.generated.append("The messages from Bot\nWith new line")  #기존 기스트에 추가

def on_btn_click():  #버튼 클릭 시 호출되는 함수
    del st.session_state.past[:]  #사용자가 이전에 입력한 값들을 저장하는 리스트
    del st.session_state.generated[:]  #봇에서 생성된 메세지들을 저장

#구글 드라이브에 업로드된 오디오 파일의 링크
# audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
# 이미지 파일의 URL
# img_path = "https://www.groundzeroweb.com/wp-content/uploads/2017/05/Funny-Cat-Memes-11.jpg"
# 유튜브 비디오를 재생하기 위한 URL
# youtube_embed = '''
# <iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
# '''

markdown = """
### HTML in markdown is ~quite~ **unsafe**
<blockquote>
  However, if you are in a trusted environment (you trust the markdown). You can use allow_html props to enable support for html.
</blockquote>

* Lists
* [ ] todo
* [x] done

Math:

Lift($L$) can be determined by Lift Coefficient ($C_L$) like the following
equation.

$$
L = \\frac{1}{2} \\rho v^2 S C_L
$$

~~~py
import streamlit as st

st.write("Python code block")
~~~

~~~js
console.log("Here is some JavaScript code")
~~~

"""

table_markdown = '''
A Table:

| Feature     | Support              |
| ----------: | :------------------- |
| CommonMark  | 100%                 |
| GFM         | 100% w/ `remark-gfm` |
'''

st.session_state.setdefault(
    'past', 
    ['plan text with line break',
     'play the song "Dancing Vegetables"', 
     'show me image of cat', 
     'and video of it',
     'show me some markdown sample',
     'table in markdown']
)
st.session_state.setdefault(
    #세션 상태의 키 (세션 상태에서 생성된 메세지 저장)
    'generated',  
    #키의 초기값 설정 (메세지의 유형과 데이터 포함)
    [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'}, 
    #  {'type': 'normal', 'data': f'<audio controls src="{audio_path}"></audio>'}, 
    #  {'type': 'normal', 'data': f'<img width="100%" height="200" src="{img_path}"/>'}, 
    #  {'type': 'normal', 'data': f'{youtube_embed}'},
     {'type': 'normal', 'data': f'{markdown}'},
     {'type': 'table', 'data': f'{table_markdown}'}]
)

st.subheader("<업무 분담 요청>")

#비어있는 컨테이너 생성
chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user") #이전 메세지 표시 (key: 메세지 식별)
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )
    
    st.button("Clear message", on_click=on_btn_click)  #clear 버튼을 누르면 이전 메세지 삭제

with st.container():
    #텍스트 입력란 생성, on_input_change 함수 콜백
    st.text_input("User Input:", on_change=on_input_change, key="user_input")