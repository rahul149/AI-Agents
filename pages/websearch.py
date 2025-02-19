from datetime import datetime
import streamlit as st
import asyncio
import json
import uuid
import os

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage   

from MultiAgents.ChatBot_With_Agents import get_runnable
# from MultiAgents.TextToSQL_CustomAgent import get_SQL_Output



# st.title("MultiAgent Setups")
# st_websearch, st_textToSql, st_browserUse = st.tabs(["WebSearch", "Text To SQL", "Browser Use"])


# if st.button("Home"):
#     st.switch_page("your_app.py")
# if st.button("Page 1"):
#     st.switch_page("pages/page_1.py")
# if st.button("Page 2"):
#     st.switch_page("pages/page_2.py")

    
# with st_browserUse:
#     st.header("Browser Use Agent")
#     st.text("Under Development")

# with st_websearch:
@st.cache_resource
def create_chatbot_instance():
    return get_runnable()

# @st.cache_resource
# def create_SQLbot_instance():
#     return get_SQL_Output()

chatbot = create_chatbot_instance()
# SQLbot = create_SQLbot_instance()

@st.cache_resource
def get_thread_id():
    return str(uuid.uuid4())

thread_id = get_thread_id()

system_message = f"""
You are a personal assistant who helps find relevant data from websites whenever needed usings tools. 
If user asks for latest information, you can use websearch tools to find the latest information or if not requiered you can anser on your own .
The current date is: {datetime.now().date()}
"""

# system_message = 'You are a personal assistant who helps find relevant data from websites whenever needed usings tools.'
async def chat_prompt_ai(messages):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    async for event in chatbot.astream_events(
            {"messages": messages}, config, version="v2"
        ):
            if event["event"] == "on_chat_model_stream":
                yield event["data"]["chunk"].content    

# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
async def main():
    st.header("Chatbot with LangGraph Agents")
    st.session_state.clear()
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=system_message)
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
            async for chunk in chat_prompt_ai(st.session_state.messages):
                response_content += chunk
                # Update the placeholder with the current response content
                message_placeholder.markdown(response_content)
        
        st.session_state.messages.append(AIMessage(content=response_content))
