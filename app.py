import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
prompt = ChatPromptTemplate.from_messages([
        ("system","""You are a helpful AI assistant.Use the previous conversation to answer the user's question whenever it is relevaPrevious Conversation:{history}"""),
        ("human", "Question: {question}")])
def generate(llm, temp, query):
    model = ChatGroq(model=llm,temperature=temp)
    parser = StrOutputParser()
    history = ""
    for user, assistant in st.session_state.chat_history:
        history += f"User: {user}\n"
        history += f"Assistant: {assistant}\n"
    chain = prompt | model | parser
    response = chain.invoke({"history": history,"question": query})
    st.session_state.chat_history.append((query, response))
    return response
st.title("QnA Chatbot")
query = st.text_input("What is your query:")
st.sidebar.title("Settings")
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=2.0,value=1.0)
model_name = st.sidebar.selectbox("Model",["llama-3.1-8b-instant","llama-3.3-70b-versatile","gemma2-9b-it","deepseek-r1-distill-llama-70b"])
if st.button("Answer"):
    if query:
        response = generate(model_name, temperature, query)
        st.write("### Assistant")
        st.write(response)

    else:
        st.warning("Hey! Please enter something.")