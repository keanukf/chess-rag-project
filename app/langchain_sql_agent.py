import os
import sqlalchemy
import ast
import re
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_vertexai import ChatVertexAI
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from google.cloud.sql.connector import Connector

# Construct the connection URI for MySQL
instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")

connector = Connector()

def getconn():
    return connector.connect(
        instance_connection_name,
        "pymysql",
        user=db_user,
        password=db_pass,
        db=db_name,
    )

# SQLAlchemy connection string
engine = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn
)

# Create a SQLDatabase instance using the MySQL connection URI
db = SQLDatabase(engine)

llm = ChatVertexAI(model="gemini-1.5-flash")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

time_classes = query_as_list(db, "SELECT time_class FROM super_gm_games_2024")
rules = query_as_list(db, "SELECT rules FROM super_gm_games_2024")
white_results = query_as_list(db, "SELECT white_result FROM super_gm_games_2024")
black_results = query_as_list(db, "SELECT black_result FROM super_gm_games_2024")
white_realNames = query_as_list(db, "SELECT white_realName FROM super_gm_games_2024")
black_realNames = query_as_list(db, "SELECT black_realName FROM super_gm_games_2024")

# Concatenate all lists
all_texts = time_classes + rules + white_results + black_results + white_realNames + black_realNames

# Debugging: Print the concatenated list
print("All Texts:", all_texts)

# Filter out empty strings
filtered_texts = [text for text in all_texts if text.strip()]

# Debugging: Print the filtered list
print("Filtered Texts:", filtered_texts)

# Check if filtered_texts is empty
if not filtered_texts:
    raise ValueError("No valid text data available for embedding.")

vector_db = FAISS.from_texts(filtered_texts, VertexAIEmbeddings(model_name="text-embedding-004"))
retriever = vector_db.as_retriever(search_kwargs={"k": 5})
description = """Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
valid proper nouns. Use the noun most similar to the search."""
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

system = """You are an agent designed to interact with a MySQL database.
Given an input question, create a syntactically correct SQL query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

You have access to the following tables: {table_names}

If you need to filter on a proper noun, you must ALWAYS first look up the filter value using the "search_proper_nouns" tool!
Do not try to guess at the proper name - use this function to find similar ones. When performing proper noun searches and the user asks for names, alwaysprioritize "white_realName" and "black_realName" over "white_username" and "black_username".""".format(
    table_names=db.get_usable_table_names()
)

system_message = SystemMessage(content=system)

tools.append(retriever_tool)

agent_executor = create_react_agent(llm, tools, state_modifier=system_message)

for s in agent_executor.stream(
    {"messages": [HumanMessage(content="How often did Hikaru Nagamura play Magnus Carlson?")]}
):
    print(s)
    print("----")

