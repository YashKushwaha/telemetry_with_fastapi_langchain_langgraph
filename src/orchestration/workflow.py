from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class State(TypedDict):
    input: str

async def process_input(state: State) -> State:
    # Process the input and return the next state
    processed_input = state["input"].upper()  # Example processing
    return {"input": processed_input}


async def create_workflow() -> StateGraph[State]:
    graph = StateGraph[State](state_schema=State)

    graph.add_node('process_input', process_input)

    graph.add_edge(START, 'process_input')
    graph.add_edge('process_input', END)    
    return graph