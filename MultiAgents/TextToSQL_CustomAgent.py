
# Text To SQL Agent

from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain import hub
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import display, Image
from langgraph.checkpoint.memory import MemorySaver
import os

load_dotenv('.env')	


db = SQLDatabase.from_uri("sqlite:///C:/Users/rahul/Documents/Projects/AI_Agents_Langchain/TextToSQL/Chinook.db")
dialect = db.dialect
table_info = db.get_table_info()

# db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# print('Table Info'+ table_info)
# print('Table Dialect'+ dialect1)

# db.run("SELECT * FROM Album LIMIT 1")

# LLM Connection
base_url = "http://localhost:11434/"
llm = ChatOllama(model="qwen2.5:3b", base_url=base_url)
# llm.invoke("Hello, how are you?")


# Application State

class State(TypedDict):
    prompt: str
    query: str
    sqlOutput: str
    llmOutput: str


promptTemplate = hub.pull("langchain-ai/sql-query-system-prompt")


# promptTemplate.messages[0].pretty_print()

# Write, Execute & Generate SQL Response
# db.get_table_info()

class QueryOutput(TypedDict):
    """"Generate a SQL query"""
    query: Annotated[str, "Syntatically correct and valid SQL query"]

QueryOutput({"query": "SELECT * FROM Album LIMIT 5"})	
QueryOutput.__annotations__


# llm.with_structured_output(QueryOutput)


async def writeQuery(state: State):
    """Generate a MySQL query to fetch information from the database"""
    
    # print('write Query DB:' +table_info)
    prompt = promptTemplate.invoke({
        "dialect": dialect,
        "top_k": 5,
        "table_info": table_info,
        "input": state["prompt"]
    })
    # print('write Query')
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    print('write Query Output' + result["query"])
    return {"query": result["query"]}

# res = writeQuery({"prompt": "List all the albums title"})

# db.run("SELECT Title FROM Album")

# res = writeQuery({"prompt": "List all the albums title"})


def execute_query(state: State):
  """Execute SQL query and return the result"""
  query = state["query"]
  
  execute_query_tool = QuerySQLDataBaseTool(db=db)
  result = execute_query_tool.invoke({"query": query})
  return {"sqlOutput": result}


def generate_answer(state:State):
  """Generate answer using retrieved information as the context"""

  prompt = (
      "Given the following user question, corresponding SQL query, and SQL"
      " response, write a natural language answer of the question.\n\n"
      f'User Question: {state["prompt"]}\n'
      f'SQL Query: {state["query"]}\n'
      f'SQL Output: {state["sqlOutput"]}\n'
      "Answer: "
  )
  response = llm.invoke(prompt)
  return {"llmOutput": response.content}


# question = "How many employee are there?"
# query = writeQuery({"prompt": question})
# query

# query['query']

# db.run('SELECT COUNT(*) FROM Employee')

# sqlOutput = execute_query(query)

# state = {"prompt": question, **query, **sqlOutput}

# generate_answer(state)



def get_SQL_Output():
    memory = MemorySaver()
    graph_builder = StateGraph(State)

    graph_builder.add_node("write_query", writeQuery)
    graph_builder.add_node("execute_query", execute_query)
    graph_builder.add_node("generate_answer", generate_answer)

    graph_builder.add_edge(START, "write_query")
    graph_builder.add_edge("write_query", "execute_query")
    graph_builder.add_edge("execute_query", "generate_answer")
    graph_builder.add_edge("generate_answer", END)

    graph = graph_builder.compile(checkpointer=memory)
    return graph


# get_SQL_Output()


