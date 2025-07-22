import streamlit as st
from faq import ingest_faq_data, chain_faq
from pathlib import Path
from router import router
from sql import sql_chain

 






faqs_path = Path(__file__).parent / "Ressources/faq_data.csv"


def ask(query):
    result = router(query)
    print("Router result:", result)
    route = getattr(result, "name", None)
    if route == "faq":
        return chain_faq(query)
    elif route == "sql":
        return sql_chain(query)
    else:
        return f"Route '{route}' is not implemented yet."


ingest_faq_data(faqs_path)
def ask(query):
    route = router(query).name
    if route == "faq":
        return chain_faq(query)
    elif route == "sql":
        return sql_chain(query)
    else:
        return f"Route '{route}' is not implemented yet."

st.title("E-commerce Chatbot")

query = st.chat_input("Ask a question about our products or services:")


if "message" not in st.session_state:
    st.session_state["messages"] = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state["messages"].append({"role": "user", "content": query})
        
    response = ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)  
    st.session_state["messages"].append({"role": "assistant", "content": response}) 
