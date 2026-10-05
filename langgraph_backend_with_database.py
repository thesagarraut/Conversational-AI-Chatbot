from typing import TypedDict, Annotated
import os
from langgraph.graph import StateGraph, START, END
#from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-120b",
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"),
    temperature=0.3
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
def chat_node(state: ChatState):
    #take user query from state
    messages = state['messages']
    #send to llm
    response=llm.invoke(messages)
    #store response to state
    return {'messages':[response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)

chekpointer=SqliteSaver(conn=conn)
graph= StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=chekpointer)

def retrieve_all_threads():
    all_threads=set()
    for checkpoint in chekpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    return list(all_threads)    