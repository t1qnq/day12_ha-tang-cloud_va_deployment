import logging
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from .config import settings
from .tools import tools_list

# 1. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Khởi tạo LLM (Cấu hình OpenRouter yêu cầu header định danh)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
    model=settings.MODEL_NAME,
    temperature=0.7,
    default_headers={
        "HTTP-Referer": "https://railway.app",
        "X-Title": "TravelBuddy-Production"
    }
)
llm_with_tools = llm.bind_tools(tools_list)

# 3. System Prompt
SYSTEM_PROMPT = """
Bạn là TravelBuddy - Trợ lý du lịch Việt Nam chuyên nghiệp.
Hãy giúp người dùng lên kế hoạch chuyến đi, tìm vé máy bay, khách sạn và quản lý ngân sách.
Bạn phải trả lời bằng tiếng Việt lịch sự và thân thiện.
"""

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

async def run_travel_agent(message: str, history: list):
    """Thực thi Agent với lịch sử hội thoại."""
    messages = []
    # Khôi phục lịch sử từ Redis/Storage
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    
    messages.append(HumanMessage(content=message))
    
    # Run Graph
    result = await graph.ainvoke({"messages": messages})
    final_msg = result["messages"][-1]
    
    return final_msg.content if hasattr(final_msg, "content") else str(final_msg)
