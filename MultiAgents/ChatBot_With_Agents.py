# %% [markdown]
# CHATBOT WITH TOOLS AND MEMORY - Bit Like an Agent

# %%
from dotenv import load_dotenv
load_dotenv('.env')	
import os

# %%
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display

# %%
from langchain.llms import OpenAI

# llm = {
#     "config_list": [{"model": "gemini-1.5-flash", "api_key": os.environ["GEMINI_API_KEY"]}],
# }

# %%
# pip install -U langchain-google-genai


base_url = "http://localhost:11434/"


llm= ChatOllama(
    base_url=base_url,
    model='qwen2.5:3b',
    temperature=0.9
)


# %%
# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.environ["GEMINI_API_KEY"])
# llm.invoke("Sing a ballad of LangChain.")

# %%
@tool
def webSearch(prompt: str) -> str:
    """
    Search the web for the realtime and latest information on the given prompt.
    for example, news, articles, blogs, stock market, etc.

    Args:
        prompt: The prompt to search for.
    """
    search = TavilySearchResults(
        max_results=3,
        search_depth='advanced',
        include_answer=True,
        include_raw_content=True,
    )
    response = search.invoke(prompt)
    
    return response

# print(webSearch('Who is the current president of the United States?'))
# search.invoke('Who is the president of the United States?')

# %%
@tool
def llmSearch(prompt: str) -> str:
    """
    Use the LLM model for general queries and basic information.
    """
    # message = HumanMessage(prompt)
    response = llm.invoke(prompt)
    return response

# %%
# webSearch

# %%
# llmSearch

# %%
tools = [webSearch, llmSearch]
# tools

# %%
llm_with_tools = llm.bind_tools(tools)
# llm_with_tools

# %%
class State(TypedDict):
    # {"messages" : []"your messagea"]}
    messages: Annotated[list, add_messages]

def chatBot(state: State) -> State:
    # message = state['message']
    response = llm_with_tools.invoke(state['messages'])
    return {'messages': [response]}

# %%
# graph = StateGraph(State)
def get_runnable():
    memory = MemorySaver()
    # memory = AsyncSqliteSaver.from_conn_string(":memory:")
    graph_builder = StateGraph(State)
    graph_builder.add_node('chatBot', chatBot)
    tool_node = ToolNode(tools=tools)

    graph_builder.add_node('tools', tool_node)
    graph_builder.add_conditional_edges('chatBot', tools_condition)

    graph_builder.add_edge("tools", 'chatBot')
    graph_builder.set_entry_point('chatBot')

    graph = graph_builder.compile(checkpointer=memory)
    return graph


# %%
# graph = get_runnable()
# display(Image(graph.get_graph().draw_mermaid_png()))

# %%
# graph.invoke({'messages': ['Tell me about earth in 3 points']})


# %%
# async def prompt_ai(messages):
#     config = {
#         "configurable": {
#             "thread_id": 1
#         }
#     }

#     async for event in graph.astream_events(
#             {"messages": messages}, config, version="v2"
#         ):
#             if event["event"] == "on_chat_model_stream":
#                 yield event["data"]["chunk"].content

# %%
# import asyncio
    
# async def main():
    
#     config = {"configurable": {"thread_id": 1}}
#     while True:
#         user_input = input("You: ")
#         if user_input in ['exit', "quit", "q"]:
#             print("Goodbye!")
#             break
#         response_content=''
#         async for chunk in prompt_ai(user_input):
#                 response_content += chunk
#                 print(response_content)
# asyncio.run(main())

    # output = graph.invoke({'messages': [user_input]}, config=config)
    # output['messages'][-1].pretty_print()
    # print("Bot:", response_content)

# %%



