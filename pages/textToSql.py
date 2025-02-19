from datetime import datetime
import streamlit as st
import asyncio
import json
import uuid
import os
# from streamlit_option_menu import option_menu
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage   
# import pages.websearch as websearch, pages.textToSql as textToSql, pages.browserUse as browserUse
# from MultiAgents.ChatBot_With_Agents import get_runnable
from MultiAgents.TextToSQL_CustomAgent import get_SQL_Output

@st.cache_resource
def create_SQLbot_instance():
    return get_SQL_Output()

# chatbot = create_chatbot_instance()
SQLbot = create_SQLbot_instance()

@st.cache_resource
def get_thread_id():
    return str(uuid.uuid4())

thread_id = get_thread_id()

sql_system_message = 'You are a personal assistant who is specialized in SQL queries and helps find relevant data from databases whenever needed usings tools.'
print(sql_system_message)
async def sql_prompt_ai(messages):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    async for event in SQLbot.astream_events(
        {"prompt": messages}, config, version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            yield event["data"]["chunk"].content

# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
async def main():
    st.header("Chatbot with LangGraph SQL Agent")
    st.session_state.clear()
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=sql_system_message)
        ]    

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        message_json = json.loads(message.model_dump_json())
        message_type = message_json["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message_json["content"])        

    # React to user input
    if prompt := st.chat_input("What would you like to Know?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display assistant response in chat message container
        response_content = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Placeholder for updating the message
            # Run the async generator to fetch responses
            async for chunk in sql_prompt_ai(st.session_state.messages):
                response_content += chunk
                # Update the placeholder with the current response content
                
                message_placeholder.markdown(response_content)
        # print(response_content)
        st.session_state.messages.append(AIMessage(content=response_content))