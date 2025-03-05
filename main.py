from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph


from utils.state import State
from workflow import route_workflow

# Create LangGraph
graph_builder = StateGraph(State)

# Add workflows as nodes
graph_builder.add_node("router", route_workflow)

# Set entry and finish points
graph_builder.set_entry_point("router")
graph_builder.set_finish_point("router")

# Compile the graph
graph = graph_builder.compile()


def run_agent():
    """
    Run the agent

    """
    
    print("Welcome to the Movie Knowledge Assistant! Type 'quit' to exit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        state_input = {"query": user_input, "answer": "None"}
        # Process the query through LangGraph
        for event in graph.stream(state_input):
            if event.values() is not None:
                for value in event.values():
                    print("Assistant Response ->: ", value.get("answer", "No answer"))
            else:
                print("No values found in event.")

if __name__ == "__main__":
    run_agent()