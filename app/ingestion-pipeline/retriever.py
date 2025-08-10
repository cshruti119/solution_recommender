from chroma_config import ChromaConfig
from fastapi import Depends

# @lru_cache()
def get_retriever():
    return Retriver()

class Retriver:
    def __init__(self):
        self.db_config = ChromaConfig()

    def query_by_product_description(self, query_text: str, n_results: int = 5):
        """Query specifically by product description."""
        print(f"Querying for {query_text}...")
        return self.db_config.query_documents(query_text, 'product_description', n_results)

    def query_by_business_context(self, query_text: str, n_results: int = 5):
        """Query specifically by business context (incident type + reason)."""
        print(f"Querying for {query_text}...")
        return self.db_config.query_documents(query_text, 'business_context', n_results)

    def query_by_all(self, query_text: str, n_results: int = 5):
        """Query specifically by business context (incident type + reason)."""
        print(f"Querying for all...")
        return self.db_config.query_documents(query_text, 'all', n_results)

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

if __name__ == "__main__":
    retriver = Retriver()
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
        result = retriver.query_by_product_description(query, n_results=2)
        retriver.print_results(result)
        print("\n")

    # Test business context queries
    print("\n" + "="*50)
    print("BUSINESS CONTEXT QUERIES")
    print("="*50)
    business_context_queries = ["PRODUCT_DEFECT: SCREEN_DEAD_PIXELS", "DELIVERY_ISSUE: LATE_DELIVERY", "FAULTY_PRODUCT: BATTERY_NOT_CHARGING"]
    for query in business_context_queries:
        result = retriver.query_by_business_context(query, n_results=2)
        retriver.print_results(result)
        print("\n")

    # Test partial business context queries
    print("\n" + "="*50)
    print("PARTIAL BUSINESS CONTEXT QUERIES")
    print("="*50)
    partial_context_queries = ["PRODUCT_DEFECT", "LATE_DELIVERY", "BATTERY_NOT_CHARGING"]
    for query in partial_context_queries:
        result = retriver.query_by_business_context(query, n_results=2)
        retriver.print_results(result)
        print("\n")

    # Test combined queries (all fields)
    print("\n" + "="*50)
    print("COMBINED QUERIES (ALL FIELDS)")
    print("="*50)
    combined_queries = ["TV screen issues", "audio problems", "battery issues"]
    for query in combined_queries:
        result = retriver.query_by_all(n_results=3)
        retriver.print_results(result)
        print("\n")