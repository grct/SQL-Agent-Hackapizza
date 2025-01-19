import json
from pprint import pprint
from typing import TypedDict, Annotated, List, Dict

from langgraph.constants import START
from langgraph.prebuilt import ToolNode, tools_condition

from src.models import State
from src.nodes.merger import merger
from src.settings import llm,vn
from langgraph.graph import add_messages, StateGraph

from src.tools.ingredienti import tool_ingredienti
from src.tools.tecniche import tool_tecniche
from src.training import training


# todo
# da domanda identificare che tool chiamare
# tools: ingredienti, tecniche, distanza,



training(vn)


graph_builder = StateGraph(State)

tools = [
    tool_tecniche,
    tool_ingredienti
]
tool_node = ToolNode(tools)


def router(state: State):
    llm_with_tools = llm.bind_tools(tools)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("router", router)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("merger", merger)
#graph_builder.add_node("evaluator", tool_evaluator)


graph_builder.add_edge(START, "router")
graph_builder.add_conditional_edges("router", tools_condition)
graph_builder.add_edge("tools", "merger")

# todo fare end grafo

graph = graph_builder.compile()

q = "Quali piatti usano la Sferificazione Filamentare a Molecole Vibrazionali, ma evitano la Decostruzione Magnetica Risonante?"
r = graph.invoke({"messages": q})

print(r)