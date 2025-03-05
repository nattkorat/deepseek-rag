import os
import json
import uuid
import numpy as np
import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv


from nomic import generate_embeddings

load_dotenv()

# Qdrant connection setup
qdrant_client = QdrantClient(host="localhost", port=6333)
# Create or connect to collection in Qdrant
COLLECTION_NAME = "movie_embeddings"
VECTOR_SIZE = 768 #our embedding model dimension

# update vector database function
def update_vectordb(data: list):
    points = []

    # create the collection if not exist
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
    
    # loop through and add the data to the collection
    for item in data:
        insertion_string = item["title"] + " " + item["overview"] + " " + item["release_date"]

        vector_item = generate_embeddings(insertion_string)
        point_id = str(uuid.uuid4())
        metadata = {
            "title": item["title"],
            "overview": item["overview"] ,
            "release_date": item["release_date"],
        }
        point = PointStruct(
            id=point_id,
            vector=vector_item,
            payload=metadata
        )
        points.append(point)
    
    # insert points to the collection
    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"Successfully inserted {len(points)} embeddings into collection {COLLECTION_NAME}")
        
        return True

# query vector database function
def query_qdrant(query: str, k: int=5):

    query_vector = generate_embeddings(query)

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=k,
        with_vectors=False
    )

    return results.points

def generate_movie_context(query_result):
    context = "Based on your query, here are some relevant movies:\n\n"
   
    for i, result in enumerate(query_result):
        movie = result.payload
        title = movie.get('title', 'Unknown')
        year = movie.get('release_date', 'N/A')
        summary = movie.get('overview', 'No overview available.')
       
        context += f"Movie {i+1}:\n"
        context += f"Title: {title} ({year})\n"
        context += f"Summary: {summary}\n\n"
   
    return context


if __name__ == '__main__':
    # # load the data
    # with open("data/movies.json") as f:
    #     data = json.load(f)
    
    # # update the vector database
    # update_vectordb(data)

    # query the vector database
    query = "list me the latest movies"
    results = query_qdrant(query)

    # generate the context
    # context = generate_movie_context(results)
    # print(context)

    print(results)
