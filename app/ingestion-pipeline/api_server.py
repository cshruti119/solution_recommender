from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from typing import List
from pathlib import Path
from retriever import Retriver, get_retriever
from ingestor import SolutionsEmbeddingPipeline, get_embeddings
from enum import Enum
import logging
import uvicorn

app = FastAPI(title="Solutions Search API",)
LOG = logging.getLogger(__name__)
LOG.info("API is starting up")
LOG.info(uvicorn.Config.asgi_version)

class SolutionResult(BaseModel):
    productDescription: str
    businessIncidentContext: str
    solutionType: str
    partner_id: str
    similarity: float
    field: str

class QueryField(Enum):
    PRODUCT_DESCRIPTION = "product_description"
    BUSINESS_CONTEXT = "business_context"
    ALL = "all"

class QueryResponse(BaseModel):
    query: str
    field: QueryField
    results: List[SolutionResult]

@app.get("/health", response_model=dict)
def health():
    LOG.debug("---- ok")
    return {"status": "ok"}

@app.post("/process")
def process(ingestor: SolutionsEmbeddingPipeline = Depends(get_embeddings)):
    ingestor.process_solutions()
    return {"status": "ok"}

@app.get("/search", response_model=QueryResponse)
def search_solutions(
        field: QueryField = Query(..., description="Field to search in"),
        query: str = Query(..., description="Query string"),
        n_results: int = Query(3, description="Number of results to return"),
        retriever: Retriver = Depends(get_retriever),
):
    """
    Search for similar solutions using the embedding pipeline.
    """
    field_name = field.name

    def get_results(query_text, field, n_results):
        print(f"{query_text}, {field}, {n_results}, {QueryField.PRODUCT_DESCRIPTION}")
        if field == QueryField.PRODUCT_DESCRIPTION.name:
            db_response = retriever.query_by_product_description(query_text,n_results)
        elif field == QueryField.BUSINESS_CONTEXT.name:
            db_response = retriever.query_by_business_context(query_text,n_results)
        else :
            db_response = retriever.query_by_all(query_text, n_results) # check this

        out = []
        for doc, metadata, distance in zip(
            db_response['documents'][0],
            db_response['metadatas'][0],
            db_response['distances'][0]
        ):
            print("meta:", metadata)
            out.append(SolutionResult(
                productDescription=metadata['productDescription'],
                businessIncidentContext=metadata['businessIncidentContext'],
                solutionType=metadata['solutionType'],
                partner_id=metadata['partner_id'],
                # createdAt=metadata['createdAt'],
                similarity=distance,
                field=field
            ))
        return out

    results = get_results(query, field_name, n_results)
    return QueryResponse(query=query, field=field, results=results)

if __name__ == '__main__':
    current_dir = Path(__file__).parent
    csv_path = current_dir / "csv_data" / "solutions.csv"
    chroma_persist_dir = current_dir / "chroma_db"

    # Check if CSV file exists
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        raise (FileNotFoundError)

    # Create embedding pipeline
    # pipeline = SolutionsEmbeddingPipeline(
    #     csv_path=str(csv_path),
    #     chroma_persist_directory=str(chroma_persist_dir))
    # pipeline.process_solutions()
    uvicorn.run("api_server:app", host="0.0.0.0", port=8083, reload=True)