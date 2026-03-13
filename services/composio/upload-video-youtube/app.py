from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_loader import get_composio_api_key, get_openai_key

composio_api_key = get_composio_api_key()
openai_key = get_openai_key()

# Initialize OpenAI model
llm = ChatOpenAI(api_key=openai_key)

# Load prompt template from LangChain Hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# Initialize Composio ToolSet with API key
composio_toolset = ComposioToolSet(api_key=composio_api_key)

# Load YouTube upload tool
tools = composio_toolset.get_tools(actions=['YOUTUBE_UPLOAD_VIDEO'])

# Create agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Define upload task
task = {
    "title": "Demo Upload Video",
    "description": "This is a demo video uploaded to YouTube using Composio",
    "tags": ["AI", "Composio", "LangChain"],
    "video_path": "videos/test.mp4"
}

# Send task to agent
result = agent_executor.invoke({"input": task})

# Print result
print(result)
