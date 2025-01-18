from typing import TypedDict, Annotated

from langgraph.prebuilt import ToolNode

from src.settings import llm
from langgraph.graph import add_messages, StateGraph
from src.tools.tecniche import tool_tecniche
from src.nodes import evaluator


# todo
# da domanda identificare che tool chiamare
# tools: ingredienti, tecniche, distanza,


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

tools = [
    tool_tecniche
]
tool_node = ToolNode(tools)


async def router(state: State):
    llm_with_tools = llm.bind_tools(tools)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", router)
graph_builder.add_node("evaluator", evaluator)

