import chromadb
from chromadb.config import Settings
from pathlib import Path
from functools import lru_cache

current_dir = Path(__file__).parent
csv_path = current_dir / "csv_data" / "solutions.csv"
chroma_persist_dir = current_dir / "chroma_db"

class ChromaConfig:
    def __init__(self):
        self.file_path = csv_path
        self.chroma_persist_directory = chroma_persist_dir
        self.client = self.initialize_db
        self.collections = {}

    def initialize_db(self):
        """Initialize ChromaDB client and collections."""
        try:
            self.client = chromadb.HttpClient(host="0.0.0.0", port=8000)
        except Exception as e:
            print(f"Error initializing ChromaDB client: {str(e)}")
            raise


    def create_collections(self: str, configs: dict):
        """
        Create a new collection in ChromaDB.
        """
        self.initialize_db()
        if self.client is None:
            raise RuntimeError("ChromaDB client is not initialized. Call initialize_chroma() first.")

        for field, config in configs.items():
            try:
                self.collections[field] = self.client.get_collection(name=config["name"])
                print(f" Using existing collection: {self.collections[field]}")
            except:
                self.collections[field] = self.client.create_collection(
                    name=config["name"],
                    metadata={"description": config["description"]})
                print(f"Created new collection: {self.collections[field]}")

    def add_documents(self: str, field: str, data: list):
        collection = self.collections[field]
        print(f"==========> here")
        collection.add(
            documents=data['documents'],
            metadatas=data['metadatas'],
            ids=data['ids']
        )
        print(f"✅ Added to {field} collection: {len(data['documents'])} documents")


    def query_documents(self: str, query_text: str, field: str, n_results: int):
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
        self.create_collections(collection_configs)
        # self.initialize_db()
        print(f"==========> here in ")
        # print(f"getting collections : {self.client.get_collection(name=f"solutions_{field}")})")
        print(f"keys: {self.collections.keys()}")
        # print(f" Querying {field} collection: {n_results} documents")
        if field not in self.collections.keys():
            raise ValueError(f"Field {field} is not a valid collection.")

        try:
            if field and field in self.collections:
                collection = self.collections[field]
                results = collection.query(
                    query_texts=[query_text],
                    n_results=n_results,
                    include=['documents', 'metadatas', 'distances']
                )
                return results
            else:
                all_results = []
                for field_name, collection in self.collections.items():
                    results = collection.query(
                        query_texts=[query_text],
                        n_results=n_results,
                        include=['documents', 'metadatas', 'distances']
                    )
                    all_results.extend(list(zip(results['documents'][0], results['metadatas'][0], results['distances'][0], [field_name] * len(results['documents'][0]))))

                # Sort by distance and take top results
                all_results.sort(key=lambda x: x[2])
                return all_results[:n_results]
        except Exception as e:
            raise RuntimeError(f"Error querying documents: {str(e)}")

# chroma_config = ChromaConfig()
# if __name__ == "__main__":
#     chroma_config.get_data_for_field( "dress","product_description",3)