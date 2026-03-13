from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI
from composio_langchain import ComposioToolSet
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config_loader import get_composio_api_key, get_openai_key, get_composio_organization_api_key

composio_api_key = get_composio_api_key()
composio_organization_api_key = get_composio_organization_api_key()
openai_key = get_openai_key()

# Initialize OpenAI model
llm = ChatOpenAI(api_key=openai_key)

# Load prompt template from LangChain Hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# Initialize Composio ToolSet with API key
composio_toolset = ComposioToolSet(api_key=composio_api_key)

# Load text summarization tool
tools = composio_toolset.get_tools(actions=['TEXT_SUMMARIZATION'])

# Create agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Text to summarize
text = """Composio is a platform that automates tasks by connecting with many APIs.
It supports integrations with YouTube, OpenAI, Google Sheets, and other services, helping developers ship faster."""

# Send task to agent
result = agent_executor.invoke({"input": text})

# Print result
print("🔹 Original text:", text)
print("\n🔹 Summary:", result)
