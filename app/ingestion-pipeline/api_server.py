from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List
from embedding_pipeline import SolutionsEmbeddingPipeline
from pathlib import Path

app = FastAPI()

# Initialize the embedding pipeline (reuse the CSV and ChromaDB locations)
current_dir = Path(__file__).parent
csv_path = current_dir / "csv_data" / "solutions.csv"
chroma_persist_dir = current_dir / "chroma_db"
pipeline = SolutionsEmbeddingPipeline(
    csv_path=str(csv_path),
    chroma_persist_directory=str(chroma_persist_dir)
)
# Ensure ChromaDB is initialized
pipeline.initialize_chroma()

class SolutionResult(BaseModel):
    productDescription: str
    businessIncidentReasonType: str
    businessIncidentReason: str
    solutionType: str
    partner_id: str
    createdAt: str
    similarity: float
    field: str

class QueryResponse(BaseModel):
    query: str
    field: str
    results: List[SolutionResult]

@app.get("/search", response_model=QueryResponse)
def search_solutions(
    field: str = Query(..., description="Field to search in: 'product_description', 'business_context', or 'all'"),
    query: str = Query(..., description="Query string (product name or business context)"),
    n_results: int = Query(3, description="Number of results to return")
):
    """
    Search for similar solutions using the embedding pipeline.
    """
    # Validate field
    valid_fields = {"product_description", "business_context", "all"}
    if field not in valid_fields:
        return {"query": query, "field": field, "results": []}

    # Run the query
    results = []
    if field == "product_description":
        chroma_field = "product_description"
    elif field == "business_context":
        chroma_field = "business_context"
    else:
        chroma_field = None  # all fields

    # Use the pipeline's query method, but capture results
    # We'll monkey-patch the query_similar_solutions to return results instead of printing
    def get_results(query_text, field, n_results):
        collection = None
        if field and field in pipeline.collections:
            collection = pipeline.collections[field]
            chroma_results = collection.query(query_texts=[query_text], n_results=n_results)
            out = []
            for doc, metadata, distance in zip(
                chroma_results['documents'][0],
                chroma_results['metadatas'][0],
                chroma_results['distances'][0]
            ):
                out.append(SolutionResult(
                    productDescription=metadata['productDescription'],
                    businessIncidentReasonType=metadata['businessIncidentReasonType'],
                    businessIncidentReason=metadata['businessIncidentReason'],
                    solutionType=metadata['solutionType'],
                    partner_id=metadata['partner_id'],
                    createdAt=metadata['createdAt'],
                    similarity=distance,
                    field=field
                ))
            return out
        else:
            # Query all fields and combine results
            all_results = []
            for field_name, collection in pipeline.collections.items():
                chroma_results = collection.query(query_texts=[query_text], n_results=n_results)
                for doc, metadata, distance in zip(
                    chroma_results['documents'][0],
                    chroma_results['metadatas'][0],
                    chroma_results['distances'][0]
                ):
                    all_results.append((metadata, distance, field_name))
            # Sort by distance and take top n_results
            all_results.sort(key=lambda x: x[1])
            out = []
            for metadata, distance, field_name in all_results[:n_results]:
                out.append(SolutionResult(
                    productDescription=metadata['productDescription'],
                    businessIncidentReasonType=metadata['businessIncidentReasonType'],
                    businessIncidentReason=metadata['businessIncidentReason'],
                    solutionType=metadata['solutionType'],
                    partner_id=metadata['partner_id'],
                    createdAt=metadata['createdAt'],
                    similarity=distance,
                    field=field_name
                ))
            return out

    results = get_results(query, chroma_field, n_results)
    return QueryResponse(query=query, field=field, results=results)

# To run: uvicorn api_server:app --reload 