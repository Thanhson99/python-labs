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

# Khởi tạo model OpenAI
llm = ChatOpenAI(api_key=openai_key)

# Lấy template prompt từ LangChain Hub
prompt = hub.pull("hwchase17/openai-functions-agent")

# Khởi tạo Composio ToolSet với API Key
composio_toolset = ComposioToolSet(api_key=composio_api_key)

# Lấy công cụ tóm tắt văn bản
tools = composio_toolset.get_tools(actions=['TEXT_SUMMARIZATION'])

# Tạo agent
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Văn bản cần tóm tắt
text = """Composio là một nền tảng giúp tự động hóa các tác vụ bằng cách kết nối với nhiều API khác nhau. 
Nó hỗ trợ tích hợp với YouTube, OpenAI, Google Sheets và nhiều dịch vụ khác, giúp lập trình viên triển khai ứng dụng một cách nhanh chóng hơn."""

# Gửi task đến agent
result = agent_executor.invoke({"input": text})

# In kết quả
print("🔹 Văn bản gốc:", text)
print("\n🔹 Bản tóm tắt:", result)
