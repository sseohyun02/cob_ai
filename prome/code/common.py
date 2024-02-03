import streamlit as st

from openai import OpenAI

client = OpenAI(
  api_key ='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',
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
        # else:
        #  break
     placeholder.markdown(message)
     return message

##스트리밍 함수 - 콘솔
def print_streaming_response_console(completion):
     message=""
     for chunk in completion:
         if chunk.choices[0].delta.content is not None:
             message += chunk.choices[0].delta.content
             print(chunk.choices[0].delta.content, end="")
        # else:
        #  break
     return message