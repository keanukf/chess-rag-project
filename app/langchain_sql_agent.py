import getpass
import os
import sqlalchemy
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_vertexai import ChatVertexAI
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

SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct MySQL query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables."""

system_message = SystemMessage(content=SQL_PREFIX)

agent_executor = create_react_agent(llm, tools, state_modifier=system_message)

for s in agent_executor.stream(
    {"messages": [HumanMessage(content="How many times did Hikaru Nakamura win with white?")]}
):
    print(s)
    print("----")

