import csv
import os
import uuid
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import numpy as np
from chroma_config import ChromaConfig

def get_embeddings():
    current_dir = Path(__file__).parent
    csv_path = current_dir / "csv_data" / "solutions.csv"
    chroma_persist_dir = current_dir / "chroma_db"
    return SolutionsEmbeddingPipeline(str(csv_path), str(chroma_persist_dir))

class SolutionsEmbeddingPipeline:
    """
    Pipeline to create embeddings for solutions data and store in ChromaDB.
    """
    
    def __init__(self, csv_path: str, chroma_persist_directory: str = "./chroma_db"):
        """
        Initialize the embedding pipeline.
        
        Args:
            csv_path: Path to the solutions.csv file
            chroma_persist_directory: Directory to persist ChromaDB data
        """
        self.csv_path = csv_path
        self.chroma_persist_directory = chroma_persist_directory
        self.client = None
        self.collection = None
        self.db_config = ChromaConfig()
        
    # def initialize_chroma(self):
    #     """Initialize ChromaDB client and collections."""
    #     try:
    #         # Create ChromaDB client with persistence
    #         self.client = chromadb.PersistentClient(
    #             path=self.chroma_persist_directory,
    #             settings=Settings(
    #                 anonymized_telemetry=False,
    #                 allow_reset=True
    #             )
    #         )
    #
    #         # Create or get collections for each embedding type
    #         self.collections = {}
    #         collection_configs = {
    #             "product_description": {
    #                 "name": "solutions_product_description",
    #                 "description": "Solutions data with embeddings for product descriptions"
    #             },
    #             "business_context": {
    #                 "name": "solutions_business_context",
    #                 "description": "Solutions data with embeddings for business incident context (type + reason)"
    #             }
    #         }
    #
    #         for field, config in collection_configs.items():
    #             try:
    #                 self.collections[field] = self.client.get_collection(name=config["name"])
    #                 print(f"Using existing collection: {config['name']}")
    #             except:
    #                 self.collections[field] = self.client.create_collection(
    #                     name=config["name"],
    #                     metadata={"description": config["description"]}
    #                 )
    #                 print(f"Created new collection: {config['name']}")
    #
    #     except Exception as e:
    #         print(f"Error initializing ChromaDB: {str(e)}")
    #         raise
    
    def read_solutions_data(self) -> List[Dict[str, Any]]:
        solutions = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    solutions.append(row)
            
            print(f"Successfully read {len(solutions)} solutions from CSV")
            return solutions
            
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            raise
    
    def create_separate_embeddings(self, record: Dict[str, Any]) -> Dict[str, str]:
        product_description = record.get('productDescription', '').strip()
        business_context = f"{record.get('businessIncidentReasonType', '').strip()}:{record.get('businessIncidentReason', '').strip()}"

        return {
            'product_description': product_description,
            'business_context': business_context
        }
    
    def create_metadata(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'productDescription': record.get('productDescription', ''),
            'solutionType': record.get('solutionType', ''),
            'businessIncidentContext': f"{record.get('businessIncidentReasonType', '')}: {record.get('businessIncidentReason', '')}",
            'partner_id': record.get('partner_id', ''),
        }
    
    def process_solutions(self):
        print("Starting solutions embedding pipeline...")
        
        collection_configs = {
            "product_description": {
                "name": "solutions_product_description",
                "description": "Solutions data with embeddings for product descriptions"
            },
            "business_context": {
                "name": "solutions_business_context",
                "description": "Solutions data with embeddings for business incident context (type + reason)"
            }
        }
        self.db_config.create_collections(collection_configs)

        solutions = self.read_solutions_data()
        
        if not solutions:
            print("No solutions data found!")
            return

        collection_data = {
            'product_description': {'documents': [], 'metadatas': [], 'ids': []},
            'business_context': {'documents': [], 'metadatas': [], 'ids': []}
        }
        
        print("Processing solutions and creating separate embeddings...")
        
        for i, solution in enumerate(solutions):
            solution_id = str(uuid.uuid4())
            field_texts = self.create_separate_embeddings(solution)
            metadata = self.create_metadata(solution)
            for field, text in field_texts.items():
                collection_data[field]['documents'].append(text)
                collection_data[field]['metadatas'].append(metadata)
                collection_data[field]['ids'].append(solution_id)
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(solutions)} solutions...")
        
        print(f"Adding {len(solutions)} documents to each ChromaDB collection...")
        
        try:
            for field, data in collection_data.items():
                self.db_config.add_documents(field,data)
            print("✅ Successfully added all solutions to all ChromaDB collections!")
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {str(e)}")
            raise

    # def query_by_product_description(self, query_text: str, n_results: int = 5):
    #     """Query specifically by product description."""
    #     print(f"Querying for {query_text}...")
    #     return self.db_config.query_documents(query_text, 'product_description', n_results)
    #
    # def query_by_business_context(self, query_text: str, n_results: int = 5):
    #     """Query specifically by business context (incident type + reason)."""
    #     print(f"Querying for {query_text}...")
    #     return self.db_config.query_documents(query_text, 'business_context', n_results)
    #
    # def query_by_all(self, n_results: int = 5):
    #     """Query specifically by business context (incident type + reason)."""
    #     print(f"Querying for all...")
    #     return self.db_config.query_documents("all", 'business_context', n_results)


def print_results(result):
    print(result)
    print("\n" + "="*50)

    for i in range(len(result['metadatas'][0])):
        print(f"Result: {i+1}")
        print(f"Product Description: {result['metadatas'][0][i]['productDescription']}")
        print(f"Business Incident Context: {result['metadatas'][0][i]['businessIncidentContext']}")
        print(f"Solution Type: {result['metadatas'][0][i]['solutionType']}")
        print(f"Partner ID: {result['metadatas'][0][i]['partner_id']}")
        print(f"Similarity Score: {result['distances'][0][i]}\n")


def main():
    current_dir = Path(__file__).parent
    csv_path = current_dir / "csv_data" / "solutions.csv"
    chroma_persist_dir = current_dir / "chroma_db"
    
    # Check if CSV file exists
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return
    
    # Create embedding pipeline
    pipeline = SolutionsEmbeddingPipeline(
        csv_path=str(csv_path),
        chroma_persist_directory=str(chroma_persist_dir)
    )
    
    # Process solutions
    pipeline.process_solutions()
    



if __name__ == "__main__":
    main() 