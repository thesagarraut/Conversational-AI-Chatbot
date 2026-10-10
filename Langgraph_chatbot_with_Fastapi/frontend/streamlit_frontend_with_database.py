import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

#utility functions
def create_thread():
    response = requests.post(
        f"{API_URL}/threads",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["thread_id"]

def retrieve_all_threads():
    response = requests.get(
        f"{API_URL}/threads",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["threads"]

def reset_chat():
    thread_id = create_thread()
    st.session_state['thread_id']=thread_id
    add_thread(thread_id)
    st.session_state['message_history']=[]
    
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        
def load_conversation(thread_id):
    response = requests.get(
        f"{API_URL}/threads/{thread_id}",
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["messages"]

def send_message(thread_id, message):
    response = requests.post(
        f"{API_URL}/chat",
        json={
            "thread_id": thread_id,
            "message": message,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["answer"]


if'message_history' not in st.session_state:
    st.session_state['message_history']=[]
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=create_thread()
    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=retrieve_all_threads()
 
add_thread(st.session_state['thread_id'])

#Sidebarui

st.sidebar.title("Langgraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()
    
st.sidebar.header("My Conversations")
for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id), key=str(thread_id)):
        try:
            messages = load_conversation(thread_id)

            st.session_state["thread_id"] = thread_id
            st.session_state["message_history"] = messages

            st.rerun()

        except requests.HTTPError as exc:
            st.sidebar.error(
                f"API error ({exc.response.status_code}): "
                f"{exc.response.text}"
            )
        except requests.RequestException as exc:
            st.sidebar.error(f"Could not load conversation: {exc}")

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
            



user_input = st.chat_input("Type here")

if user_input:
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user"):
        st.write(user_input)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = send_message(
                    st.session_state["thread_id"],
                    user_input,
                )

            st.write(answer)

        st.session_state["message_history"].append({
            "role": "assistant",
            "content": answer,
        })

    except requests.HTTPError as exc:
        st.error(
            f"API error ({exc.response.status_code}): "
            f"{exc.response.text}"
        )

    except requests.RequestException as exc:
        st.error(f"Could not contact the chatbot API: {exc}")
