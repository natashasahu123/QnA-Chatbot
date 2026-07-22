import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
prompt=ChatPromptTemplate.from_messages([('system','''You are an helpful ai assistant,
                                        Use the previous conversation to answer the user's question whenever it is relevant.Previous Conversation:Previous Conversation:{history}'''),
                                        ('human','Question:{question}')])
def generate(llm,temp,query):
    model=Ollama(model=llm,temperature=temp)
    parser=StrOutputParser()
    history = ""
    for user, assistant in st.session_state.chat_history:
        history += f"User: {user}\n"
        history += f"Assistant: {assistant}\n"
    chain=prompt|model|parser
    res=chain.invoke({ "history": history,'question':query})
    st.session_state.chat_history.append((query, res))
    return res
st.title("QnA Chatbot")
query=st.text_input("What is your query:")
st.sidebar.title("Settings")
temperature=st.sidebar.slider('Temperature:',min_value=0.0,max_value=2.0,value=1.0)
model_name=st.sidebar.selectbox('Model:',['llama3.2:3b','llama3.2:1b','gemma3:4b','gemma2:9b','gemma3:latest'])

if st.button("Answer"):
    if query:
        response=generate(model_name,temperature,query)
        st.write("### Assistant")
        st.write(response)
    else:
        st.warning("Hey! please enter something .")