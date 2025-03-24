import os
from dotenv import load_dotenv
import logging
import sqlalchemy
import ast
import re
from langchain import hub
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_vertexai import ChatVertexAI
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from sqlalchemy import inspect
from google.cloud import aiplatform

# Load environment variables from .env file located in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Verify the environment variable
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set in .env file")

print(f"Using GCP credentials from: {credentials_path}")

# Initialize Vertex AI with your project ID and location
project_id = os.getenv("GCP_PROJECT_ID", "default_project_id")  # Use environment variable or default
location = os.getenv("GCP_LOCATION", "us-central1")  # Use environment variable or default

aiplatform.init(project=project_id, location=location)

# Use a relative path for the SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'data', 'chess_rag.db')
engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")

# Create a SQLDatabase instance using sqlite database
db = SQLDatabase(engine)

llm = ChatVertexAI(model="gemini-2.0-flash")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

time_classes = query_as_list(db, "SELECT time_class FROM super_gm_games_2024")
time_controls = query_as_list(db, "SELECT time_control FROM super_gm_games_2024")
rules = query_as_list(db, "SELECT rules FROM super_gm_games_2024")
white_results = query_as_list(db, "SELECT white_result FROM super_gm_games_2024")
white_realNames = query_as_list(db, "SELECT white_realName FROM super_gm_games_2024")
white_usernames = query_as_list(db, "SELECT white_username FROM super_gm_games_2024")
black_results = query_as_list(db, "SELECT black_result FROM super_gm_games_2024")
black_realNames = query_as_list(db, "SELECT black_realName FROM super_gm_games_2024")
black_usernames = query_as_list(db, "SELECT black_username FROM super_gm_games_2024")

# Concatenate all lists
all_texts = time_classes + time_controls + rules + white_results + white_realNames + white_usernames + black_results + black_realNames + black_usernames

# Filter out empty strings
filtered_texts = [text for text in all_texts if text.strip()]

# Remove duplicates
filtered_texts = list(set(filtered_texts))

# Check if filtered_texts is empty
if not filtered_texts:
    raise ValueError("No valid text data available for embedding.")

vector_db = FAISS.from_texts(filtered_texts, VertexAIEmbeddings(model_name="text-embedding-005"))
retriever = vector_db.as_retriever(search_kwargs={"k": 5})
description = """Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
valid proper nouns. Use the noun most similar to the search."""
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

# Use SQLAlchemy's reflection to get column names
inspector = inspect(engine)

# Fetch the column names from the super_gm_games_2024 table
column_names = [column['name'] for column in inspector.get_columns("super_gm_games_2024")]

system = """You are an agent designed to interact with a SQLite database.
Given an input question, create a syntactically correct SQL query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DDL statements (CREATE, ALTER, DROP etc.) to the database.

Follow these guidelines when constructing your query:
1. Determine the Question Intent: Identify the primary purpose of the question (e.g., seeking player performance, game statistics, comparison of players, or specific game details).
   - For example, if the user asks about the number of wins or performance in a given timeframe, focus on filtering the results based on game outcomes for the relevant player.
2. Identify the Player Role:
   - If the user specifies whether the player was white or black, query only the corresponding role (e.g., "white_realName" and "white_result" if the player was white).
   - If the user does not specify a role, consider both roles (i.e., check both "white_realName" and "black_realName") to ensure the player's performance is captured regardless of role. When filtering by player result (e.g., wins or losses), ensure you apply the filter to both "white_result" and "black_result" as appropriate.
3. Formulate the Query:
   - Retrieve only the columns relevant to answering the question.
   - Limit the number of results to at most 5 by default, unless a different limit is specified.
   - For proper nouns (such as player names), use the "search_proper_nouns" tool to accurately identify the relevant value before filtering.
4. Example Scenarios:
   - If the question asks for "Fabiano Caruana's wins in August," filter for games in August where "Fabiano Caruana" appears in either "white_realName" or "black_realName" and check for wins in the respective "white_result" or "black_result" columns.
   - If the question asks for "highest-rated opponents of Hikaru Nakamura," retrieve games where "Hikaru Nakamura" appears in either role and order results by the opponent's rating in the relevant column.

You have access to the following columns in the super_gm_games_2024 table: {column_names}

If you need to filter on a proper noun, you must ALWAYS first look up the filter value using the "search_proper_nouns" tool!
Do not try to guess at the proper name - use this function to find similar ones. When performing proper noun searches and the user asks for names, always prioritize "white_realName" and "black_realName" over "white_username" and "black_username".""".format(
    column_names=", ".join(column_names)
)

system_message = SystemMessage(content=system)

tools.append(retriever_tool)

agent_executor = create_react_agent(llm, tools, state_modifier=system_message)

def execute_query(query):
    """
    Execute a query using the agent and return the final answer.
    """
    try:
        # Create a HumanMessage with the query
        human_message = HumanMessage(content=query)
        
        # Use the invoke method to get the messages
        messages = agent_executor.invoke({"messages": [human_message]})
        
        # Access the last AIMessage content
        final_answer = messages["messages"][-1].content
        
        # Return the final answer
        return final_answer
    
    except Exception as e:
        # Handle exceptions and return an error message
        return f"Error executing query: {str(e)}"