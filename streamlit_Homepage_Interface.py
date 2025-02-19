from datetime import datetime
import streamlit as st
import asyncio
import json
import uuid
import os
from streamlit_option_menu import option_menu
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage   
import pages.websearch as websearch, pages.textToSql as textToSql, pages.browserUse as browserUse
from MultiAgents.ChatBot_With_Agents import get_runnable
from MultiAgents.TextToSQL_CustomAgent import get_SQL_Output

st.set_page_config(
    page_title="MultiAgent Setups",
)


# st.title("MultiAgent Setups")

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='MultiAgents',
                options=['WebSearch','Text To Sql','Browser Use'],
                icons=['house-fill','person-circle','trophy-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},}
                            
                )

        
        if app == "WebSearch":
            asyncio.run(websearch.main())
        if app == "Text To Sql":
            asyncio.run(textToSql.main())
        if app == "Browser Use":
            asyncio.run(browserUse.main())
          
             
    run()            


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
#     @st.cache_resource
#     def create_chatbot_instance():
#         return get_runnable()

#     # @st.cache_resource
#     # def create_SQLbot_instance():
#     #     return get_SQL_Output()

#     chatbot = create_chatbot_instance()
#     # SQLbot = create_SQLbot_instance()

#     @st.cache_resource
#     def get_thread_id():
#         return str(uuid.uuid4())

#     thread_id = get_thread_id()

#     system_message = f"""
#     You are a personal assistant who helps find relevant data from websites whenever needed usings tools. 
#     If user asks for latest information, you can use websearch tools to find the latest information or if not requiered you can anser on your own .
#     The current date is: {datetime.now().date()}
#     """

#     # system_message = 'You are a personal assistant who helps find relevant data from websites whenever needed usings tools.'
#     async def chat_prompt_ai(messages):
#         config = {
#             "configurable": {
#                 "thread_id": thread_id
#             }
#         }
#         async for event in chatbot.astream_events(
#                 {"messages": messages}, config, version="v2"
#             ):
#                 if event["event"] == "on_chat_model_stream":
#                     yield event["data"]["chunk"].content    
    
#     # ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
#     async def main():
#         st.header("Chatbot with LangGraph Agents")

#         # Initialize chat history
#         if "messages" not in st.session_state:
#             st.session_state.messages = [
#                 SystemMessage(content=system_message)
#             ]    

#         # Display chat messages from history on app rerun
#         for message in st.session_state.messages:
#             message_json = json.loads(message.json())
#             message_type = message_json["type"]
#             if message_type in ["human", "ai", "system"]:
#                 with st.chat_message(message_type):
#                     st.markdown(message_json["content"])        

#         # React to user input
#         if prompt := st.chat_input("What would you like to Know?"):
#             # Display user message in chat message container
#             st.chat_message("user").markdown(prompt)
#             # Add user message to chat history
#             st.session_state.messages.append(HumanMessage(content=prompt))

#             # Display assistant response in chat message container
#             response_content = ""
#             with st.chat_message("assistant"):
#                 message_placeholder = st.empty()  # Placeholder for updating the message
#                 # Run the async generator to fetch responses
#                 async for chunk in chat_prompt_ai(st.session_state.messages):
#                     response_content += chunk
#                     # Update the placeholder with the current response content
#                     message_placeholder.markdown(response_content)
            
#             st.session_state.messages.append(AIMessage(content=response_content))
#     asyncio.run(main())


         


# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# with st_textToSql:
    
    # @st.cache_resource
    # def create_SQLbot_instance():
    #     return get_SQL_Output()

    # # chatbot = create_chatbot_instance()
    # SQLbot = create_SQLbot_instance()

    # @st.cache_resource
    # def get_thread_id():
    #     return str(uuid.uuid4())

    # thread_id = get_thread_id()

    # sql_system_message = 'You are a personal assistant who is specialized in SQL queries and helps find relevant data from databases whenever needed usings tools.'
    # async def sql_prompt_ai(messages):
    #     config = {
    #         "configurable": {
    #             "thread_id": thread_id
    #         }
    #     }
    #     async for event in SQLbot.astream_events(
    #         {"prompt": messages}, config, version="v2"
    #     ):
    #         if event["event"] == "on_chat_model_stream":
    #             yield event["data"]["chunk"].content

    # # ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
    # async def main():
    #     st.header("Chatbot with LangGraph SQL Agent")

    #     # Initialize chat history
    #     if "messages" not in st.session_state:
    #         st.session_state.messages = [
    #             SystemMessage(content=sql_system_message)
    #         ]    

    #     # Display chat messages from history on app rerun
    #     for message in st.session_state.messages:
    #         message_json = json.loads(message.json())
    #         message_type = message_json["type"]
    #         if message_type in ["human", "ai", "system"]:
    #             with st.chat_message(message_type):
    #                 st.markdown(message_json["content"])        

    #     # React to user input
    #     if prompt := st.chat_input("What would you like to Know?"):
    #         # Display user message in chat message container
    #         st.chat_message("user").markdown(prompt)
    #         # Add user message to chat history
    #         st.session_state.messages.append(HumanMessage(content=prompt))

    #         # Display assistant response in chat message container
    #         response_content = ""
    #         with st.chat_message("assistant"):
    #             message_placeholder = st.empty()  # Placeholder for updating the message
    #             # Run the async generator to fetch responses
    #             async for chunk in sql_prompt_ai(st.session_state.messages):
    #                 response_content += chunk
    #                 # Update the placeholder with the current response content
                    
    #                 message_placeholder.markdown(response_content)
    #         # print(response_content)
    #         st.session_state.messages.append(AIMessage(content=response_content))

    
#     asyncio.run(main())



# # if __name__ == "__main__":
# #     asyncio.run(main())