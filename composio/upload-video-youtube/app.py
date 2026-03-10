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

# Khởi tạo model OpenAI
llm = ChatOpenAI(api_key=openai_key)

# Lấy template prompt từ LangChain Hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# Khởi tạo Composio ToolSet với API Key
composio_toolset = ComposioToolSet(api_key=composio_api_key)

# Lấy công cụ upload video YouTube
tools = composio_toolset.get_tools(actions=['YOUTUBE_UPLOAD_VIDEO'])

# Tạo agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Định nghĩa task upload video
task = {
    "title": "Demo Upload Video",
    "description": "Đây là một video demo upload lên YouTube bằng Composio",
    "tags": ["AI", "Composio", "LangChain"],
    "video_path": "videos/test.mp4"
}

# Gửi task đến agent
result = agent_executor.invoke({"input": task})

# In kết quả
print(result)
