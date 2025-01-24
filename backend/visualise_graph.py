import os
from langchain_core.runnables.graph import MermaidDrawMethod
import langchain_sql_agent

# Define the directory and file name
output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'agent_graph.png')

# Save the image to the specified file
with open(output_file, 'wb') as f:
    f.write(
        langchain_sql_agent.agent_executor.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
    )