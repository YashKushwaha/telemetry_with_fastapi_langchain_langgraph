# https://opentelemetry.io/docs/languages/python/instrumentation/

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from time import sleep
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

class State(TypedDict):
    input: str

@tracer.start_as_current_span("process_input")
async def process_input(state: State) -> State:
    # Process the input and return the next state
    processed_input = state["input"].upper()  # Example processing
    current_span = trace.get_current_span()
    attributes ={   'input.value': state["input"], 'output.value': processed_input,
                    'openinference.span.kind': 'LC_NODE', 'openinference.workflow.name': 'process_input',
                    }


    current_span.set_attributes(attributes)
    current_span.add_event("Inside process_input function")
    sleep(2)  # Simulate some delay
    return {"input": processed_input}


async def create_workflow() -> StateGraph[State]:
    graph = StateGraph[State](state_schema=State)

    graph.add_node('process_input', process_input)

    graph.add_edge(START, 'process_input')
    graph.add_edge('process_input', END)    
    return graph