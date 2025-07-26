import csv
import os
import uuid
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import numpy as np


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
        
    def initialize_chroma(self):
        """Initialize ChromaDB client and collections."""
        try:
            # Create ChromaDB client with persistence
            self.client = chromadb.PersistentClient(
                path=self.chroma_persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Create or get collections for each embedding type
            self.collections = {}
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
            
            for field, config in collection_configs.items():
                try:
                    self.collections[field] = self.client.get_collection(name=config["name"])
                    print(f"Using existing collection: {config['name']}")
                except:
                    self.collections[field] = self.client.create_collection(
                        name=config["name"],
                        metadata={"description": config["description"]}
                    )
                    print(f"Created new collection: {config['name']}")
                
        except Exception as e:
            print(f"Error initializing ChromaDB: {str(e)}")
            raise
    
    def read_solutions_data(self) -> List[Dict[str, Any]]:
        """
        Read solutions data from CSV file.
        
        Returns:
            List of dictionaries containing solution records
        """
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
        """
        Create separate text strings for each embedding type.
        
        Args:
            record: Dictionary containing solution record
            
        Returns:
            Dictionary with separate text strings for each embedding type
        """
        # Extract the fields we want to embed
        product_description = record.get('productDescription', '').strip()
        business_incident_reason_type = record.get('businessIncidentReasonType', '').strip()
        business_incident_reason = record.get('businessIncidentReason', '').strip()
        
        # Combine business incident reason type and reason
        business_context = f"{business_incident_reason_type}: {business_incident_reason}"
        
        return {
            'product_description': product_description,
            'business_context': business_context
        }
    
    def create_metadata(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create metadata dictionary for the record.
        
        Args:
            record: Dictionary containing solution record
            
        Returns:
            Metadata dictionary
        """
        return {
            'createdAt': record.get('createdAt', ''),
            'productId': record.get('productId', ''),
            'productDescription': record.get('productDescription', ''),
            'solutionType': record.get('solutionType', ''),
            'businessIncidentReasonType': record.get('businessIncidentReasonType', ''),
            'businessIncidentReason': record.get('businessIncidentReason', ''),
            'partner_id': record.get('partner_id', ''),
            'source_file': 'solutions.csv'
        }
    
    def process_solutions(self):
        """
        Main method to process solutions and create embeddings.
        """
        print("Starting solutions embedding pipeline...")
        
        # Initialize ChromaDB
        self.initialize_chroma()
        
        # Read solutions data
        solutions = self.read_solutions_data()
        
        if not solutions:
            print("No solutions data found!")
            return
        
        # Prepare data for each collection
        collection_data = {
            'product_description': {'documents': [], 'metadatas': [], 'ids': []},
            'business_context': {'documents': [], 'metadatas': [], 'ids': []}
        }
        
        print("Processing solutions and creating separate embeddings...")
        
        for i, solution in enumerate(solutions):
            # Create unique ID
            solution_id = str(uuid.uuid4())
            
            # Create separate embeddings for each field
            field_texts = self.create_separate_embeddings(solution)
            
            # Create metadata
            metadata = self.create_metadata(solution)
            
            # Add to each collection's data
            for field, text in field_texts.items():
                collection_data[field]['documents'].append(text)
                collection_data[field]['metadatas'].append(metadata)
                collection_data[field]['ids'].append(solution_id)
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(solutions)} solutions...")
        
        # Add documents to each ChromaDB collection
        print(f"Adding {len(solutions)} documents to each ChromaDB collection...")
        
        try:
            for field, data in collection_data.items():
                collection = self.collections[field]
                collection.add(
                    documents=data['documents'],
                    metadatas=data['metadatas'],
                    ids=data['ids']
                )
                print(f"✅ Added to {field} collection: {len(data['documents'])} documents")
            
            print("✅ Successfully added all solutions to all ChromaDB collections!")
            
            # Print collection info
            for field, collection in self.collections.items():
                collection_count = collection.count()
                print(f"Total documents in {field} collection: {collection_count}")
            
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {str(e)}")
            raise
    
    def query_similar_solutions(self, query_text: str, field: str = None, n_results: int = 5):
        """
        Query for similar solutions based on text similarity.
        
        Args:
            query_text: Text to search for similar solutions
            field: Specific field to search in ('product_description', 'business_context')
            n_results: Number of similar results to return
        """
        if not self.collections:
            print("ChromaDB collections not initialized!")
            return
        
        try:
            if field and field in self.collections:
                # Query specific field
                collection = self.collections[field]
                results = collection.query(
                    query_texts=[query_text],
                    n_results=n_results
                )
                field_name = field.replace('_', ' ').title()
                print(f"\n🔍 Query: '{query_text}' (Field: {field_name})")
            else:
                # Query all fields and combine results
                all_results = []
                for field_name, collection in self.collections.items():
                    results = collection.query(
                        query_texts=[query_text],
                        n_results=n_results
                    )
                    all_results.extend(list(zip(results['documents'][0], results['metadatas'][0], results['distances'][0], [field_name] * len(results['documents'][0]))))
                
                # Sort by distance and take top results
                all_results.sort(key=lambda x: x[2])
                all_results = all_results[:n_results]
                
                print(f"\n🔍 Query: '{query_text}' (All Fields)")
                print(f"Found {len(all_results)} similar solutions:\n")
                
                for i, (doc, metadata, distance, field_name) in enumerate(all_results):
                    print(f"{i+1}. Product: {metadata['productDescription']}")
                    print(f"   Issue Type: {metadata['businessIncidentReasonType']}")
                    print(f"   Issue: {metadata['businessIncidentReason']}")
                    print(f"   Solution Type: {metadata['solutionType']}")
                    print(f"   Partner ID: {metadata['partner_id']}")
                    print(f"   Created: {metadata['createdAt']}")
                    print(f"   Field: {field_name.replace('_', ' ').title()}")
                    print(f"   Similarity Score: {distance:.4f}")
                    print("-" * 80)
                return
            
            print(f"Found {len(results['documents'][0])} similar solutions:\n")
            
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                print(f"{i+1}. Product: {metadata['productDescription']}")
                print(f"   Issue Type: {metadata['businessIncidentReasonType']}")
                print(f"   Issue: {metadata['businessIncidentReason']}")
                print(f"   Solution Type: {metadata['solutionType']}")
                print(f"   Partner ID: {metadata['partner_id']}")
                print(f"   Created: {metadata['createdAt']}")
                print(f"   Similarity Score: {results['distances'][0][i]:.4f}")
                print("-" * 80)
                
        except Exception as e:
            print(f"Error querying ChromaDB: {str(e)}")
    
    def query_by_product_description(self, query_text: str, n_results: int = 5):
        """Query specifically by product description."""
        return self.query_similar_solutions(query_text, 'product_description', n_results)
    
    def query_by_business_context(self, query_text: str, n_results: int = 5):
        """Query specifically by business context (incident type + reason)."""
        return self.query_similar_solutions(query_text, 'business_context', n_results)


def main():
    """
    Main function to run the embedding pipeline.
    """
    # Define paths
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
    
    # Example queries to test the embeddings
    print("\n" + "="*80)
    print("TESTING EMBEDDINGS WITH FIELD-SPECIFIC QUERIES")
    print("="*80)
    
    # Test product description queries
    print("\n" + "="*50)
    print("PRODUCT DESCRIPTION QUERIES")
    print("="*50)
    product_queries = ["LG OLED TV", "Bose headphones", "Dyson vacuum"]
    for query in product_queries:
        pipeline.query_by_product_description(query, n_results=2)
        print("\n")
    
    # Test business context queries
    print("\n" + "="*50)
    print("BUSINESS CONTEXT QUERIES")
    print("="*50)
    business_context_queries = ["PRODUCT_DEFECT: SCREEN_DEAD_PIXELS", "DELIVERY_ISSUE: LATE_DELIVERY", "FAULTY_PRODUCT: BATTERY_NOT_CHARGING"]
    for query in business_context_queries:
        pipeline.query_by_business_context(query, n_results=2)
        print("\n")
    
    # Test partial business context queries
    print("\n" + "="*50)
    print("PARTIAL BUSINESS CONTEXT QUERIES")
    print("="*50)
    partial_context_queries = ["PRODUCT_DEFECT", "LATE_DELIVERY", "BATTERY_NOT_CHARGING"]
    for query in partial_context_queries:
        pipeline.query_by_business_context(query, n_results=2)
        print("\n")
    
    # Test combined queries (all fields)
    print("\n" + "="*50)
    print("COMBINED QUERIES (ALL FIELDS)")
    print("="*50)
    combined_queries = ["TV screen issues", "audio problems", "battery issues"]
    for query in combined_queries:
        pipeline.query_similar_solutions(query, n_results=3)
        print("\n")


if __name__ == "__main__":
    main() 