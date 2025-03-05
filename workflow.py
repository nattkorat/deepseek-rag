
import argparse

from qdrant import query_qdrant, generate_movie_context
from utils.state import State
from llm import rag, generic



def workflow_with_rag(state: State, model="deepseek-r1:7b"):
    query = state["query"]
    result = query_qdrant(query)
    context = generate_movie_context(result)
   
    response = rag(context, query, model)

    if not response:
        return {"answer": "No response generated"}
   
    return {"answer": response}

def workflow_without_rag(state: State, model="deepseek-r1:7b"):
    query = state["query"]
    response = generic(query, model)
   
    if not response:
        return {"answer": "No response generated"}
   
    return {"answer": response}

# Router Node
def route_workflow(state: State):
    query = state["query"]
    query_result_score = query_qdrant(query)[0].score # Get the score of the first result for thresholding
   
    if query_result_score > 0.6:
        print("Node Chosen -----> RAG")
        response = workflow_with_rag(state, model="llama3.2")
    else:
        print("Node Chosen -----> GENERIC")
        response = workflow_without_rag(state, model="llama3.2")
   
    # Ensure state always has "answer"
    state["answer"] = response.get("answer", "No answer")
    return state