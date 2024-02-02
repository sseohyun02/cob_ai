import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

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
     'table in markdown']
)
st.session_state.setdefault(
    'generated', 
    [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'},
     {'type': 'table', 'data': f'{table_markdown}'}]
)

st.title("Chat placeholder")

chat_placeholder = st.empty()

with chat_placeholder.container():    
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
    st.text_input("User Input:", on_change=on_input_change, key="user_input")
