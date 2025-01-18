from typing import TypedDict, Annotated

from langgraph.constants import START
from langgraph.prebuilt import ToolNode, tools_condition

from src.settings import llm
from langgraph.graph import add_messages, StateGraph
from src.tools.tecniche import tool_tecniche
from src.nodes.evaluator import tool_evaluator


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


def router(state: State):
    llm_with_tools = llm.bind_tools(tools)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}



graph_builder.add_node("router", router)
graph_builder.add_node("tools", tool_node)
#graph_builder.add_node("evaluator", tool_evaluator)


graph_builder.add_edge(START, "router")
graph_builder.add_conditional_edges("router", tools_condition)
graph_builder.add_edge("tools", "router")

# todo fare end grafo

graph = graph_builder.compile()

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            try:
                print("Assistant:", value["messages"][-1].content)
            except:
                pass