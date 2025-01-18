from typing import TypedDict, Annotated
from src.settings import llm
from langgraph.graph import add_messages, StateGraph


# todo
# da domanda identificare che tool chiamare
# tools: ingredienti, tecniche, distanza,


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

tools = [

]


from typing import Literal


# Define the function that determines whether to continue or not
def should_continue(state: State) -> Literal["end", "continue"]:
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no tool call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


# Define the function that calls the model
async def call_model(state: State):
    messages = state["messages"]
    response = await llm.ainvoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}



def chatbot(state: State):
    llm_with_tools = llm.bind_tools(tools)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}




graph_builder.add_node("chatbot", chatbot)

import os
from langchain_ibm import WatsonxLLM

###TEST CONNESSIONE
watsonx_llm = WatsonxLLM(
    model_id=os.environ["MODEL"],
    project_id=os.environ["PROJECT_ID"],
)
print(watsonx_llm.invoke("Come sono relazionate le trasformate di fourier con lo spettro delle ampiezze?"))

