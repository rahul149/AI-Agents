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

# st.set_page_config(
#     page_title=None,
# )


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

